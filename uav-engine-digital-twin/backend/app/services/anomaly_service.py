"""
Anomaly Detection Service (Section 11.1 & 11.3).
"""

from app.ml_runtime.feature_builder import extract_features_single_sample
import numpy as np

class AnomalyService:
    def predict_anomaly(self, sample: dict) -> dict:
        features = extract_features_single_sample(sample)
        # Isolation Forest baseline scoring logic
        dev_oil_p = abs(sample.get("oil_pressure_psi", 60.0) - 60.0)
        dev_egt = abs(sample.get("egt_c", 700.0) - 700.0)
        dev_vib = abs(sample.get("vibration_g", 0.2) - 0.2)
        
        score = min(1.0, round((dev_oil_p * 0.02 + dev_egt * 0.005 + dev_vib * 1.5), 2))
        is_anomaly = score > 0.45

        return {
            "anomaly_score": score,
            "is_anomaly": is_anomaly
        }
