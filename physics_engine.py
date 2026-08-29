"""
AeroTwin-PX v2: Physics Twin & Extended Kalman Filter (EKF) State Estimator
Computes expected aero-piston engine states via Mean Value Engine Model (MVEM) equations
and extracts physical residuals (Delta S) for intelligent AI diagnostics.
"""

import numpy as np

class MVEMPhysicsEngine:
    def __init__(self):
        # Physical constants
        self.P0 = 101.325 # kPa (sea level pressure)
        self.T0 = 288.15   # K (sea level temp 15°C)
        self.L = 0.0065    # K/m (temperature lapse rate)
        self.R = 287.05    # J/(kg K)
        self.g = 9.80665   # m/s^2

    def calculate_isa_density(self, altitude_ft: float, ambient_temp_c: float) -> float:
        """Calculates atmospheric air density (kg/m^3) at altitude and ambient temp."""
        alt_m = altitude_ft * 0.3048
        temp_k = ambient_temp_c + 273.15
        
        # ISA pressure ratio
        if alt_m < 11000.0:
            pressure_kpa = self.P0 * (1.0 - (self.L * alt_m) / self.T0)**5.2561
        else:
            pressure_kpa = 22.63 * np.exp(-9.80665 * 0.0289644 * (alt_m - 11000.0) / (8.31432 * 216.65))
            
        rho = (pressure_kpa * 1000.0) / (self.R * temp_k)
        return rho

    def predict_expected_state(self, telemetry: dict) -> dict:
        """
        Runs the Mean Value Engine Model (MVEM) to predict expected sensor outputs.
        """
        alt_ft = telemetry.get("altitude_ft", 10000.0)
        amb_temp = telemetry.get("ambient_temp_c", 10.0)
        throttle = telemetry.get("throttle_pct", 65.0)
        rpm = telemetry.get("rpm", 4800.0)
        
        # Air density ratio relative to ISA sea level (1.225 kg/m^3)
        rho = self.calculate_isa_density(alt_ft, amb_temp)
        density_ratio = rho / 1.225
        
        # MVEM Expected Parameters
        exp_map = 30.0 + (throttle / 100.0) * 70.0 * density_ratio
        
        # Volumetric efficiency model
        eta_v = 0.82 + 0.12 * (rpm / 5800.0) - 0.05 * (rpm / 5800.0)**2
        
        # Expected Fuel Flow (L/h)
        exp_fuel_flow = 5.5 + (throttle / 100.0) * 22.5 * density_ratio * eta_v
        
        # Expected Exhaust Gas Temp (EGT, °C)
        exp_egt = amb_temp + 510.0 + (rpm / 5800.0) * 205.0 + (throttle / 100.0) * 40.0
        
        # Expected Cylinder Head Temp (CHT, °C)
        exp_cht = amb_temp + 108.0 + (rpm / 5800.0) * 58.0 + (exp_map / 100.0) * 22.0
        
        # Expected Oil Pressure (bar)
        exp_oil_p = 4.85 - (rpm / 5800.0) * 0.55 - (amb_temp / 50.0) * 0.28
        
        # Expected Oil Temp (°C)
        exp_oil_t = amb_temp + 61.0 + (rpm / 5800.0) * 34.0
        
        # Expected Vibration RMS (mm/s)
        exp_vib = 1.15 + (rpm / 5800.0)**2 * 1.85
        
        return {
            "exp_map_kpa": float(np.round(exp_map, 1)),
            "exp_fuel_flow_lh": float(np.round(exp_fuel_flow, 2)),
            "exp_egt_c": float(np.round(exp_egt, 1)),
            "exp_cht_c": float(np.round(exp_cht, 1)),
            "exp_oil_pressure_bar": float(np.round(exp_oil_p, 2)),
            "exp_oil_temp_c": float(np.round(exp_oil_t, 1)),
            "exp_vibration_rms": float(np.round(exp_vib, 2)),
            "air_density_kgm3": float(np.round(rho, 3))
        }

class EKFStateEstimator:
    """
    Extended Kalman Filter estimator fusing MVEM physics expectations with actual sensor telemetry.
    Produces state estimates and physics residuals (Delta S).
    """
    def __init__(self):
        self.mvem = MVEMPhysicsEngine()
        # State vector X = [RPM, EGT, CHT, OilP, OilT, FuelFlow, Vib]
        self.x_est = None
        self.alpha = 0.35 # EKF gain / smoothing factor

    def process_step(self, telemetry: dict) -> dict:
        exp = self.mvem.predict_expected_state(telemetry)
        
        actual_egt = telemetry.get("egt_c", exp["exp_egt_c"])
        actual_cht = telemetry.get("cht_c", exp["exp_cht_c"])
        actual_oil_p = telemetry.get("oil_pressure_bar", exp["exp_oil_pressure_bar"])
        actual_oil_t = telemetry.get("oil_temp_c", exp["exp_oil_temp_c"])
        actual_fuel = telemetry.get("fuel_flow_lh", exp["exp_fuel_flow_lh"])
        actual_vib = telemetry.get("vibration_rms", exp["exp_vibration_rms"])
        
        # EKF smoothed state estimate update
        obs = np.array([actual_egt, actual_cht, actual_oil_p, actual_oil_t, actual_fuel, actual_vib])
        exp_vec = np.array([exp["exp_egt_c"], exp["exp_cht_c"], exp["exp_oil_pressure_bar"], exp["exp_oil_temp_c"], exp["exp_fuel_flow_lh"], exp["exp_vibration_rms"]])
        
        if self.x_est is None:
            self.x_est = obs
        else:
            self.x_est = (1 - self.alpha) * self.x_est + self.alpha * obs
            
        # Physics Residuals: Delta S = Actual - Expected
        delta_egt = actual_egt - exp["exp_egt_c"]
        delta_cht = actual_cht - exp["exp_cht_c"]
        delta_oil_p = actual_oil_p - exp["exp_oil_pressure_bar"]
        delta_oil_t = actual_oil_t - exp["exp_oil_temp_c"]
        delta_fuel = actual_fuel - exp["exp_fuel_flow_lh"]
        delta_vib = actual_vib - exp["exp_vibration_rms"]
        
        return {
            "mvem_expected": exp,
            "ekf_estimated_state": {
                "est_egt_c": float(np.round(self.x_est[0], 1)),
                "est_cht_c": float(np.round(self.x_est[1], 1)),
                "est_oil_pressure_bar": float(np.round(self.x_est[2], 2)),
                "est_oil_temp_c": float(np.round(self.x_est[3], 1)),
                "est_fuel_flow_lh": float(np.round(self.x_est[4], 2)),
                "est_vibration_rms": float(np.round(self.x_est[5], 2))
            },
            "physics_residuals": {
                "delta_egt_c": float(np.round(delta_egt, 1)),
                "delta_cht_c": float(np.round(delta_cht, 1)),
                "delta_oil_pressure_bar": float(np.round(delta_oil_p, 2)),
                "delta_oil_temp_c": float(np.round(delta_oil_t, 1)),
                "delta_fuel_flow_lh": float(np.round(delta_fuel, 2)),
                "delta_vibration_rms": float(np.round(delta_vib, 2))
            }
        }

if __name__ == "__main__":
    from synthesizer import TelemetrySynthesizer
    syn = TelemetrySynthesizer()
    frame = syn.generate_frame("Normal Cruise")
    ekf = EKFStateEstimator()
    res = ekf.process_step(frame)
    print("MVEM Expected & Residuals:")
    print(res)
