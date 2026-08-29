"""
AeroTwin-PX: Digital Twin Visualization Adapter
Maps existing backend telemetry, physics residuals, subsystem health scores, AI diagnostics,
RUL bounds, and mission reliability into a single centralized TwinVisualizationState data contract.
"""

class TwinVisualizationAdapter:
    @staticmethod
    def extract_twin_state(
        telemetry: dict,
        mvem_exp: dict,
        ekf_est: dict,
        residuals: dict,
        sensor_health: dict,
        subsystem_health: dict,
        ai_res: dict,
        mission_reliability: dict = None
    ) -> dict:
        """
        Transforms existing data streams into a unified data contract for the 3D visualization.
        """
        # Pitch, Roll, Yaw attitude estimation derived from throttle/altitude if not explicit
        alt_ft = telemetry.get("altitude_ft", 10000.0)
        throttle = telemetry.get("throttle_pct", 65.0)
        rpm = telemetry.get("rpm", 4800.0)
        step = telemetry.get("timestamp", 0.0)
        
        pitch_deg = (throttle - 65.0) * 0.2 + np_sin(step * 0.1) * 1.5
        roll_deg = np_sin(step * 0.05) * 3.0
        yaw_deg = (step * 2.0) % 360.0
        
        # Lat/Lon flight trajectory route synthesis
        base_lat = 26.9124 + np_cos(step * 0.02) * 0.15
        base_lon = 75.7873 + np_sin(step * 0.02) * 0.15
        
        m_prob = mission_reliability.get("mission_completion_prob_pct", 95.0) if mission_reliability else 95.0
        r_level = mission_reliability.get("risk_level", "LOW RISK") if mission_reliability else "LOW RISK"
        
        # Extract per-sensor detailed data for 3D interactive markers & tooltips
        sens_scores = sensor_health.get("sensor_scores", {})
        
        sens_map = {
            "RPM": {
                "label": "Engine Speed (RPM)",
                "actual": float(rpm),
                "expected": float(mvem_exp.get("exp_rpm", rpm)),
                "residual": float(0.0),
                "unit": "RPM",
                "health": float(sens_scores.get("RPM", 98.0))
            },
            "CHT": {
                "label": "Cylinder Head Temp",
                "actual": float(telemetry.get("cht_c", 150.0)),
                "expected": float(mvem_exp.get("exp_cht_c", 150.0)),
                "residual": float(residuals.get("delta_cht_c", 0.0)),
                "unit": "°C",
                "health": float(sens_scores.get("CHT", 95.0))
            },
            "EGT": {
                "label": "Exhaust Gas Temp",
                "actual": float(telemetry.get("egt_c", 650.0)),
                "expected": float(mvem_exp.get("exp_egt_c", 650.0)),
                "residual": float(residuals.get("delta_egt_c", 0.0)),
                "unit": "°C",
                "health": float(sens_scores.get("EGT", 96.0))
            },
            "OilP": {
                "label": "Oil Pressure",
                "actual": float(telemetry.get("oil_pressure_bar", 4.2)),
                "expected": float(mvem_exp.get("exp_oil_pressure_bar", 4.2)),
                "residual": float(residuals.get("delta_oil_pressure_bar", 0.0)),
                "unit": "bar",
                "health": float(sens_scores.get("OilP", 97.0))
            },
            "OilT": {
                "label": "Oil Temperature",
                "actual": float(telemetry.get("oil_temp_c", 90.0)),
                "expected": float(mvem_exp.get("exp_oil_temp_c", 90.0)),
                "residual": float(residuals.get("delta_oil_temp_c", 0.0)),
                "unit": "°C",
                "health": float(sens_scores.get("OilT", 96.0))
            },
            "Fuel": {
                "label": "Fuel Flow Rate",
                "actual": float(telemetry.get("fuel_flow_lh", 15.0)),
                "expected": float(mvem_exp.get("exp_fuel_flow_lh", 15.0)),
                "residual": float(residuals.get("delta_fuel_flow_lh", 0.0)),
                "unit": "L/h",
                "health": float(sens_scores.get("Fuel", 94.0))
            },
            "Vib": {
                "label": "Vibration RMS",
                "actual": float(telemetry.get("vibration_rms", 2.0)),
                "expected": float(mvem_exp.get("exp_vibration_rms", 2.0)),
                "residual": float(residuals.get("delta_vibration_rms", 0.0)),
                "unit": "mm/s",
                "health": float(sens_scores.get("Vib", 95.0))
            },
            "Volt": {
                "label": "Battery Voltage",
                "actual": float(telemetry.get("battery_volt", 28.0)),
                "expected": 28.0,
                "residual": float(telemetry.get("battery_volt", 28.0) - 28.0),
                "unit": "V",
                "health": 99.0
            },
            "Alt": {
                "label": "Alternator Current",
                "actual": float(telemetry.get("alternator_curr", 35.0)),
                "expected": 35.0,
                "residual": float(telemetry.get("alternator_curr", 35.0) - 35.0),
                "unit": "A",
                "health": 99.0
            },
            "Inj": {
                "label": "Injection Timing",
                "actual": float(telemetry.get("injection_timing_deg", 18.0)),
                "expected": 18.0,
                "residual": float(telemetry.get("injection_timing_deg", 18.0) - 18.0),
                "unit": "°BTDC",
                "health": 97.0
            },
            "MAP": {
                "label": "Manifold Abs Pressure",
                "actual": float(telemetry.get("map_kpa", 80.0)),
                "expected": float(mvem_exp.get("exp_map_kpa", 80.0)),
                "residual": float(telemetry.get("map_kpa", 80.0) - mvem_exp.get("exp_map_kpa", 80.0)),
                "unit": "kPa",
                "health": 98.0
            }
        }
        
        return {
            "timestamp": float(step),
            "engine_id": "ENG-001",
            # Telemetry Parameters
            "rpm": float(rpm),
            "cht_c": float(telemetry.get("cht_c", 150.0)),
            "egt_c": float(telemetry.get("egt_c", 650.0)),
            "oil_pressure_bar": float(telemetry.get("oil_pressure_bar", 4.2)),
            "oil_temp_c": float(telemetry.get("oil_temp_c", 90.0)),
            "fuel_flow_lh": float(telemetry.get("fuel_flow_lh", 15.0)),
            "vibration_rms": float(telemetry.get("vibration_rms", 2.0)),
            "battery_volt": float(telemetry.get("battery_volt", 28.0)),
            "alternator_curr": float(telemetry.get("alternator_curr", 35.0)),
            "injection_timing_deg": float(telemetry.get("injection_timing_deg", 18.0)),
            "map_kpa": float(telemetry.get("map_kpa", 80.0)),
            "throttle_pct": float(throttle),
            "altitude_ft": float(alt_ft),
            "ambient_temp_c": float(telemetry.get("ambient_temp_c", 15.0)),
            # Aircraft Attitude & Position
            "pitch_deg": float(np_round(pitch_deg, 2)),
            "roll_deg": float(np_round(roll_deg, 2)),
            "yaw_deg": float(np_round(yaw_deg, 2)),
            "latitude": float(np_round(base_lat, 4)),
            "longitude": float(np_round(base_lon, 4)),
            # Physics Residuals (Delta S)
            "residuals": {
                "delta_egt_c": float(residuals.get("delta_egt_c", 0.0)),
                "delta_cht_c": float(residuals.get("delta_cht_c", 0.0)),
                "delta_oil_pressure_bar": float(residuals.get("delta_oil_pressure_bar", 0.0)),
                "delta_oil_temp_c": float(residuals.get("delta_oil_temp_c", 0.0)),
                "delta_fuel_flow_lh": float(residuals.get("delta_fuel_flow_lh", 0.0)),
                "delta_vibration_rms": float(residuals.get("delta_vibration_rms", 0.0))
            },
            # Sensor Details & Tooltips
            "sensor_details": sens_map,
            # Sensor Quality & Twin Confidence
            "digital_twin_confidence": float(sensor_health.get("digital_twin_confidence", 95.0)),
            "sensor_scores": sens_scores,
            # Engine Subsystem Health
            "overall_ehi": float(subsystem_health.get("engine_health_index", 95.0)),
            "health_status": subsystem_health.get("health_status", "HEALTHY"),
            "subsystem_health": subsystem_health.get("subsystems", {}),
            # AI Diagnostics & SHAP
            "predicted_fault": ai_res.get("predicted_fault", "Normal Operation"),
            "fault_class_id": int(ai_res.get("fault_class_id", 0)),
            "fault_confidence_pct": float(ai_res.get("fault_confidence_pct", 0.0)),
            "anomaly_score": float(ai_res.get("anomaly_score", 0.0)),
            "is_anomaly": bool(ai_res.get("is_anomaly", False)),
            "shap_top_contributors": ai_res.get("shap_top_contributors", []),
            # RUL & Prediction Bounds
            "rul_hours": float(ai_res.get("rul_hours", 350.0)),
            "rul_interval_hours": ai_res.get("rul_interval_hours", [300.0, 400.0]),
            # Mission Reliability
            "mission_completion_prob_pct": float(m_prob),
            "risk_level": str(r_level)
        }

def np_sin(x):
    import math
    return math.sin(x)

def np_cos(x):
    import math
    return math.cos(x)

def np_round(val, decimals):
    return round(val, decimals)

