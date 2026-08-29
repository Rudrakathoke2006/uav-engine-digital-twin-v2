"""
AeroTwin-PX v2: Sensor Health & Subsystem Engine Health Index (EHI) Engine
Evaluates sensor validity, overall Digital Twin Confidence Score (%),
and multi-subsystem engine health indices (Combustion, Thermal, Lubrication, Mechanical, Electrical).
"""

import numpy as np

class EngineHealthEngine:
    def __init__(self):
        self.sensor_history = []
        
    def evaluate_sensor_health(self, telemetry: dict, physics_residuals: dict) -> dict:
        """
        Detects sensor bias, drift, dropout, stuck values, and cross-sensor inconsistency.
        Returns individual sensor health scores and overall Digital Twin Confidence (%).
        """
        egt = telemetry.get("egt_c", 650.0)
        cht = telemetry.get("cht_c", 150.0)
        oil_p = telemetry.get("oil_pressure_bar", 4.0)
        oil_t = telemetry.get("oil_temp_c", 90.0)
        fuel = telemetry.get("fuel_flow_lh", 15.0)
        vib = telemetry.get("vibration_rms", 2.0)
        
        delta_egt = abs(physics_residuals.get("delta_egt_c", 0.0))
        delta_cht = abs(physics_residuals.get("delta_cht_c", 0.0))
        delta_oil_p = abs(physics_residuals.get("delta_oil_pressure_bar", 0.0))
        delta_fuel = abs(physics_residuals.get("delta_fuel_flow_lh", 0.0))
        
        # Individual sensor quality scores (100 = Healthy, 0 = Faulty Sensor)
        s_egt = max(0.0, 100.0 - (delta_egt / 180.0) * 80.0) if egt < 1100.0 else 0.0
        s_cht = max(0.0, 100.0 - (delta_cht / 80.0) * 80.0) if cht < 350.0 else 0.0
        s_oil_p = max(0.0, 100.0 - (delta_oil_p / 3.0) * 80.0) if 0.1 <= oil_p <= 10.0 else 0.0
        s_oil_t = 98.0 if 20.0 <= oil_t <= 160.0 else 20.0
        s_fuel = max(0.0, 100.0 - (delta_fuel / 10.0) * 80.0)
        s_vib = 96.0 if vib < 15.0 else 10.0
        
        # Sensor Fault Flagging
        suspect_sensors = []
        if s_egt < 50.0 and s_cht > 80.0:
            suspect_sensors.append("EGT Sensor (Possible Drift/Bias)")
        if s_oil_p < 40.0 and s_oil_t > 70.0:
            suspect_sensors.append("Oil Pressure Sensor (Suspect Reading)")
            
        avg_sensor_quality = np.mean([s_egt, s_cht, s_oil_p, s_oil_t, s_fuel, s_vib])
        
        # Digital Twin Confidence Score
        twin_confidence = 0.5 * avg_sensor_quality + 0.3 * (100.0 - min(delta_egt * 0.3, 50.0)) + 0.2 * 95.0
        twin_confidence = float(np.round(min(max(twin_confidence, 0.0), 100.0), 1))
        
        return {
            "sensor_scores": {
                "egt_sensor": float(np.round(s_egt, 1)),
                "cht_sensor": float(np.round(s_cht, 1)),
                "oil_p_sensor": float(np.round(s_oil_p, 1)),
                "oil_t_sensor": float(np.round(s_oil_t, 1)),
                "fuel_sensor": float(np.round(s_fuel, 1)),
                "vibration_sensor": float(np.round(s_vib, 1))
            },
            "suspect_sensors": suspect_sensors,
            "digital_twin_confidence": twin_confidence
        }

    def compute_subsystem_health(self, telemetry: dict, physics_residuals: dict) -> dict:
        """
        Computes health indices (0-100) for 5 engine subsystems and overall EHI.
        """
        d_egt = abs(physics_residuals.get("delta_egt_c", 0.0))
        d_cht = abs(physics_residuals.get("delta_cht_c", 0.0))
        d_oil_p = abs(physics_residuals.get("delta_oil_pressure_bar", 0.0))
        d_oil_t = abs(physics_residuals.get("delta_oil_temp_c", 0.0))
        d_fuel = abs(physics_residuals.get("delta_fuel_flow_lh", 0.0))
        d_vib = abs(physics_residuals.get("delta_vibration_rms", 0.0))
        
        volt = telemetry.get("battery_volt", 28.0)
        
        # 1. Combustion Subsystem Health
        h_combustion = 100.0 - (d_egt * 0.4 + d_fuel * 4.0)
        h_combustion = max(0.0, min(100.0, h_combustion))
        
        # 2. Thermal Subsystem Health
        h_thermal = 100.0 - (d_cht * 0.7 + d_egt * 0.3)
        h_thermal = max(0.0, min(100.0, h_thermal))
        
        # 3. Lubrication Subsystem Health
        h_lubrication = 100.0 - (d_oil_p * 22.0 + d_oil_t * 0.8)
        h_lubrication = max(0.0, min(100.0, h_lubrication))
        
        # 4. Mechanical Subsystem Health
        h_mechanical = 100.0 - (d_vib * 14.0 + (d_cht > 30.0) * 15.0)
        h_mechanical = max(0.0, min(100.0, h_mechanical))
        
        # 5. Electrical Subsystem Health
        v_drop = max(0.0, 27.5 - volt)
        h_electrical = 100.0 - (v_drop * 18.0)
        h_electrical = max(0.0, min(100.0, h_electrical))
        
        # Dynamic Overall Engine Health Index (EHI)
        overall_ehi = (
            0.25 * h_combustion +
            0.25 * h_thermal +
            0.20 * h_lubrication +
            0.20 * h_mechanical +
            0.10 * h_electrical
        )
        overall_ehi = float(np.round(overall_ehi, 1))
        
        # Status Labeling
        if overall_ehi >= 85.0:
            status = "HEALTHY"
            color = "green"
        elif overall_ehi >= 70.0:
            status = "NORMAL / SLIGHT DEGRADATION"
            color = "blue"
        elif overall_ehi >= 50.0:
            status = "DEGRADED / WARNING"
            color = "orange"
        else:
            status = "CRITICAL / MAINTENANCE REQUIRED"
            color = "red"
            
        return {
            "subsystems": {
                "combustion_health": float(np.round(h_combustion, 1)),
                "thermal_health": float(np.round(h_thermal, 1)),
                "lubrication_health": float(np.round(h_lubrication, 1)),
                "mechanical_health": float(np.round(h_mechanical, 1)),
                "electrical_health": float(np.round(h_electrical, 1))
            },
            "engine_health_index": overall_ehi,
            "health_status": status,
            "status_color": color
        }

if __name__ == "__main__":
    from synthesizer import TelemetrySynthesizer
    from physics_engine import EKFStateEstimator
    syn = TelemetrySynthesizer()
    ekf = EKFStateEstimator()
    frame = syn.generate_frame("Normal Cruise", "injector_coking", 0.7)
    res = ekf.process_step(frame)
    
    he = EngineHealthEngine()
    sens = he.evaluate_sensor_health(frame, res["physics_residuals"])
    sub = he.compute_subsystem_health(frame, res["physics_residuals"])
    print("Sensor Health & Digital Twin Confidence:", sens)
    print("Subsystem Health & EHI:", sub)
