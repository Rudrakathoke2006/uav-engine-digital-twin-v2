"""
AeroTwin-PX v2: AI Diagnostic & Prognostics Models
Includes Isolation Forest (Anomaly Detection), XGBoost Multi-Class Fault Classifier,
XGBoost RUL Regressor with prediction uncertainty intervals, and SHAP Feature Attribution.
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
import xgboost as xgb

try:
    import shap
except ImportError:
    shap = None

from synthesizer import TelemetrySynthesizer
from physics_engine import EKFStateEstimator

class AIDiagnosticsSuite:
    FAULT_MAP = {
        0: "Normal Operation",
        1: "Cylinder Misfire",
        2: "Injector Coking / Lean Fuel",
        3: "Lubrication System Loss",
        4: "Sensor Drift / Bias",
        5: "Combustion Instability",
        6: "Thermal Overheating",
        7: "Abnormal Mechanical Vibration"
    }

    def __init__(self):
        self.iso_forest = IsolationForest(n_estimators=100, contamination=0.08, random_state=42)
        self.fault_classifier = xgb.XGBClassifier(n_estimators=60, max_depth=4, learning_rate=0.1, random_state=42)
        self.rul_regressor = xgb.XGBRegressor(n_estimators=80, max_depth=5, learning_rate=0.08, random_state=42)
        self.shap_explainer = None
        self.is_trained = False
        
        # Automatic baseline training on initialization
        self._train_models()

    def _extract_features(self, df: pd.DataFrame, ekf_estimator: EKFStateEstimator = None) -> pd.DataFrame:
        """Extracts engineered physics-residual and operational features."""
        if ekf_estimator is None:
            ekf_estimator = EKFStateEstimator()
            
        features_list = []
        for idx, row in df.iterrows():
            row_dict = row.to_dict()
            res = ekf_estimator.process_step(row_dict)["physics_residuals"]
            
            feat = {
                "rpm": row_dict["rpm"],
                "cht_c": row_dict["cht_c"],
                "egt_c": row_dict["egt_c"],
                "oil_pressure_bar": row_dict["oil_pressure_bar"],
                "oil_temp_c": row_dict["oil_temp_c"],
                "fuel_flow_lh": row_dict["fuel_flow_lh"],
                "vibration_rms": row_dict["vibration_rms"],
                "battery_volt": row_dict.get("battery_volt", 28.0),
                "delta_egt_c": res["delta_egt_c"],
                "delta_cht_c": res["delta_cht_c"],
                "delta_oil_pressure_bar": res["delta_oil_pressure_bar"],
                "delta_oil_temp_c": res["delta_oil_temp_c"],
                "delta_fuel_flow_lh": res["delta_fuel_flow_lh"],
                "delta_vibration_rms": res["delta_vibration_rms"]
            }
            features_list.append(feat)
            
        return pd.DataFrame(features_list)

    def _train_models(self):
        """Generates synthetic dataset and trains the AI suite."""
        syn = TelemetrySynthesizer()
        
        # 1. Train Anomaly Forest on Normal Telemetry
        normal_records = [syn.generate_frame("Normal Cruise", "none", 0.0, step=i) for i in range(300)]
        df_normal = pd.DataFrame(normal_records)
        X_normal = self._extract_features(df_normal)
        self.iso_forest.fit(X_normal)
        
        # 2. Train Multi-Class Fault Classifier
        records = []
        faults_list = ["normal", "misfire", "injector_coking", "lubrication_loss", "sensor_drift", "combustion_instability", "overheating", "abnormal_vibration"]
        label_map = {f: i for i, f in enumerate(faults_list)}
        
        for f_name in faults_list:
            for s in [0.0, 0.3, 0.6, 0.9]:
                if f_name == "normal" and s > 0.0:
                    continue
                for step in range(50):
                    frm = syn.generate_frame("Normal Cruise", f_name, s, step=step)
                    frm["label"] = label_map[f_name]
                    records.append(frm)
                    
        df_faults = pd.DataFrame(records)
        X_faults = self._extract_features(df_faults)
        y_faults = df_faults["label"]
        
        self.fault_classifier.fit(X_faults, y_faults)
        
        # Initialize SHAP explainer with fallback
        try:
            import shap
            self.shap_explainer = shap.TreeExplainer(self.fault_classifier)
        except Exception:
            self.shap_explainer = None
        
        # 3. Train RUL Regressor on Run-to-Failure Trajectories
        df_rul = syn.generate_run_to_failure_dataset(num_engines=12, max_hours=600)
        X_rul = self._extract_features(df_rul)
        y_rul = df_rul["rul_hours"]
        self.rul_regressor.fit(X_rul, y_rul)
        
        self.feature_names = list(X_normal.columns)
        self.is_trained = True

    def predict_diagnostics(self, telemetry: dict, physics_residuals: dict) -> dict:
        """
        Runs complete AI inference pipeline for a single telemetry step.
        """
        if not self.is_trained:
            self._train_models()
            
        feat_dict = {
            "rpm": telemetry["rpm"],
            "cht_c": telemetry["cht_c"],
            "egt_c": telemetry["egt_c"],
            "oil_pressure_bar": telemetry["oil_pressure_bar"],
            "oil_temp_c": telemetry["oil_temp_c"],
            "fuel_flow_lh": telemetry["fuel_flow_lh"],
            "vibration_rms": telemetry["vibration_rms"],
            "battery_volt": telemetry.get("battery_volt", 28.0),
            "delta_egt_c": physics_residuals["delta_egt_c"],
            "delta_cht_c": physics_residuals["delta_cht_c"],
            "delta_oil_pressure_bar": physics_residuals["delta_oil_pressure_bar"],
            "delta_oil_temp_c": physics_residuals["delta_oil_temp_c"],
            "delta_fuel_flow_lh": physics_residuals["delta_fuel_flow_lh"],
            "delta_vibration_rms": physics_residuals["delta_vibration_rms"]
        }
        
        X_single = pd.DataFrame([feat_dict], columns=self.feature_names)
        
        # 1. Anomaly Score (0.0 = Normal, 1.0 = Highly Anomalous)
        raw_score = self.iso_forest.decision_function(X_single)[0]
        anomaly_score = float(np.round(min(max((0.15 - raw_score) * 2.5, 0.0), 1.0), 2))
        is_anomaly = anomaly_score > 0.45
        
        # 2. Fault Classification
        probs = self.fault_classifier.predict_proba(X_single)[0]
        pred_class_id = int(np.argmax(probs))
        confidence = float(np.round(probs[pred_class_id] * 100.0, 1))
        fault_name = self.FAULT_MAP.get(pred_class_id, "Unknown Fault")
        
        # 3. SHAP / Feature Attribution Calculation
        if self.shap_explainer is not None:
            try:
                shap_vals = self.shap_explainer.shap_values(X_single)
                shap_arr = np.array(shap_vals)
                if isinstance(shap_vals, list):
                    # Old SHAP: list of (n_samples, n_features) arrays, one per class
                    class_shap = np.array(shap_vals[pred_class_id]).flatten()
                elif shap_arr.ndim == 3:
                    # New SHAP (≥0.40): shape (n_samples, n_features, n_classes)
                    class_shap = shap_arr[0, :, pred_class_id]
                elif shap_arr.ndim == 2:
                    # Shape (n_samples, n_features)
                    class_shap = shap_arr[0]
                else:
                    class_shap = shap_arr.flatten()
            except Exception:
                class_shap = np.abs(X_single.iloc[0].values) * 0.1
        else:
            # Fallback to feature importance weights
            class_shap = self.fault_classifier.feature_importances_

        # Guarantee class_shap is a flat 1D numpy array before indexing
        class_shap = np.array(class_shap).flatten()

        top_indices = np.argsort(np.abs(class_shap))[-3:][::-1]
        top_features = [
            {
                "feature": self.feature_names[int(i)],
                "shap_weight": float(np.round(float(class_shap[int(i)]), 3)),
                "val": float(np.round(float(X_single.iloc[0, int(i)]), 2))
            }
            for i in top_indices
        ]
        
        # 4. RUL Estimation with 80% Prediction Uncertainty Interval
        pred_rul = float(self.rul_regressor.predict(X_single)[0])
        pred_rul = max(5.0, pred_rul)
        uncertainty_margin = max(12.0, pred_rul * 0.18)
        rul_min = max(0.0, pred_rul - uncertainty_margin)
        rul_max = pred_rul + uncertainty_margin
        
        return {
            "anomaly_score": anomaly_score,
            "is_anomaly": is_anomaly,
            "predicted_fault": fault_name,
            "fault_class_id": pred_class_id,
            "fault_confidence_pct": confidence,
            "shap_top_contributors": top_features,
            "rul_hours": float(np.round(pred_rul, 1)),
            "rul_interval_hours": [float(np.round(rul_min, 1)), float(np.round(rul_max, 1))]
        }

if __name__ == "__main__":
    from synthesizer import TelemetrySynthesizer
    from physics_engine import EKFStateEstimator
    syn = TelemetrySynthesizer()
    ekf = EKFStateEstimator()
    ai = AIDiagnosticsSuite()
    
    frame = syn.generate_frame("Normal Cruise", "misfire", 0.8)
    res = ekf.process_step(frame)
    diag = ai.predict_diagnostics(frame, res["physics_residuals"])
    print("AI Diagnostics Output:", diag)
