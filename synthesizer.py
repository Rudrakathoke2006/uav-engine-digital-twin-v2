"""
AeroTwin-PX v2: Causal Physics Telemetry Synthesizer
Generates realistic multi-sensor telemetry for 4-stroke aero-piston UAV engines.
Supports 5 mission profiles, synthetic fault injection, and run-to-failure degradation trajectory generation.
"""

import numpy as np
import pandas as pd

class TelemetrySynthesizer:
    def __init__(self, seed: int = 42):
        np.random.seed(seed)
        
    def get_mission_parameters(self, profile: str, step: int = 0):
        """Returns baseline operational parameters for a given mission profile."""
        profile = profile.lower()
        if "high altitude" in profile:
            altitude_ft = 18000.0 + np.sin(step * 0.05) * 500.0
            ambient_temp_c = -15.0
            throttle_pct = 78.0
        elif "hot weather" in profile:
            altitude_ft = 5000.0 + np.sin(step * 0.02) * 200.0
            ambient_temp_c = 42.0
            throttle_pct = 68.0
        elif "rapid throttle" in profile:
            altitude_ft = 7500.0
            ambient_temp_c = 25.0
            throttle_pct = 50.0 + 35.0 * np.abs(np.sin(step * 0.2))
        elif "long endurance" in profile:
            altitude_ft = 12000.0
            ambient_temp_c = 5.0
            throttle_pct = 62.0
        else: # Normal Cruise
            altitude_ft = 10000.0 + np.sin(step * 0.01) * 300.0
            ambient_temp_c = 10.0
            throttle_pct = 65.0
            
        return altitude_ft, ambient_temp_c, throttle_pct

    def generate_frame(self, profile: str = "Normal Cruise", fault_type: str = "none", severity: float = 0.0, step: int = 0):
        """
        Generates a single 10Hz synchronized multi-sensor telemetry frame with physics correlations and fault effects.
        """
        altitude_ft, ambient_temp_c, throttle_pct = self.get_mission_parameters(profile, step)
        
        # Physics atmosphere (ISA density ratio)
        air_density_ratio = np.exp(-altitude_ft / 28000.0)
        
        # Base RPM linked to throttle and air density
        base_rpm = 2200.0 + (throttle_pct / 100.0) * 3400.0 * (0.85 + 0.15 * air_density_ratio)
        rpm = base_rpm + np.random.normal(0, 8.0)
        
        # Manifold Absolute Pressure (MAP, kPa)
        map_kpa = 30.0 + (throttle_pct / 100.0) * 70.0 * air_density_ratio + np.random.normal(0, 0.5)
        
        # Baseline expected temperatures and pressures
        base_cht = ambient_temp_c + 110.0 + (rpm / 5800.0) * 55.0 + (map_kpa / 100.0) * 20.0
        base_egt = ambient_temp_c + 500.0 + (rpm / 5800.0) * 210.0 + (throttle_pct / 100.0) * 45.0
        base_oil_p = 4.8 - (base_rpm / 5800.0) * 0.6 - (ambient_temp_c / 50.0) * 0.3
        base_oil_t = ambient_temp_c + 60.0 + (base_rpm / 5800.0) * 35.0
        base_fuel_flow = 6.0 + (throttle_pct / 100.0) * 22.0 * air_density_ratio
        base_vib = 1.2 + (rpm / 5800.0)**2 * 1.8
        base_volt = 28.2 - (rpm / 5800.0) * 0.2
        base_alt_curr = 12.0 + (throttle_pct / 100.0) * 18.0
        base_inj_timing = 22.0 + (rpm / 5800.0) * 4.0 # deg BTDC
        
        # Apply Fault Effects
        cht = base_cht + np.random.normal(0, 1.2)
        egt = base_egt + np.random.normal(0, 3.0)
        oil_p = base_oil_p + np.random.normal(0, 0.05)
        oil_t = base_oil_t + np.random.normal(0, 0.8)
        fuel_flow = base_fuel_flow + np.random.normal(0, 0.2)
        vib = base_vib + np.random.normal(0, 0.08)
        volt = base_volt + np.random.normal(0, 0.1)
        alt_curr = base_alt_curr + np.random.normal(0, 0.3)
        inj_timing = base_inj_timing + np.random.normal(0, 0.1)
        
        s = min(max(severity, 0.0), 1.0)
        fault_type = fault_type.lower()
        
        if fault_type == "misfire":
            rpm -= s * 350.0 + np.random.normal(0, 40.0 * s)
            egt -= s * 120.0 # Unburnt fuel drops exhaust temp
            vib += s * 4.5 + np.random.normal(0, 0.5 * s)
            fuel_flow += s * 2.5 # Excess unburnt fuel
        elif fault_type == "injector_coking":
            fuel_flow -= s * 4.5 # Lean mixture / clogged nozzle
            egt += s * 95.0 # Lean combustion increases EGT
            cht += s * 25.0
            rpm -= s * 120.0
        elif fault_type == "lubrication_loss":
            oil_p -= s * 2.4 # Severe pressure loss
            oil_t += s * 38.0 # Friction heat rise
            vib += s * 2.1
            cht += s * 18.0
        elif fault_type == "sensor_drift":
            egt += s * 150.0 # Sensor drifts upward independently of physics
        elif fault_type == "combustion_instability":
            egt += np.random.normal(0, 45.0 * s)
            rpm += np.random.normal(0, 90.0 * s)
            vib += s * 2.8
            inj_timing += np.random.normal(0, 2.0 * s)
        elif fault_type == "overheating":
            cht += s * 55.0 # Exceeds 200°C limit
            egt += s * 85.0 # Exceeds 800°C limit
            oil_t += s * 28.0
            oil_p -= s * 0.8
        elif fault_type == "abnormal_vibration":
            vib += s * 5.8 + np.random.normal(0, 0.4 * s) # Exceeds 6 mm/s limit
            rpm += np.random.normal(0, 25.0 * s)
        elif fault_type == "electrical_failure":
            volt -= s * 6.5 # Voltage drops below 24V
            alt_curr -= s * 10.0
            
        return {
            "timestamp": step * 0.1,
            "altitude_ft": float(np.round(altitude_ft, 1)),
            "ambient_temp_c": float(np.round(ambient_temp_c, 1)),
            "throttle_pct": float(np.round(throttle_pct, 1)),
            "map_kpa": float(np.round(map_kpa, 1)),
            "rpm": float(np.round(rpm, 1)),
            "cht_c": float(np.round(cht, 1)),
            "egt_c": float(np.round(egt, 1)),
            "oil_pressure_bar": float(np.round(oil_p, 2)),
            "oil_temp_c": float(np.round(oil_t, 1)),
            "fuel_flow_lh": float(np.round(fuel_flow, 2)),
            "vibration_rms": float(np.round(vib, 2)),
            "battery_volt": float(np.round(volt, 2)),
            "alternator_curr": float(np.round(alt_curr, 1)),
            "injection_timing_deg": float(np.round(inj_timing, 2)),
            "active_fault": fault_type if severity > 0.1 else "normal",
            "fault_severity": float(s)
        }

    def generate_run_to_failure_dataset(self, num_engines: int = 10, max_hours: int = 800) -> pd.DataFrame:
        """
        Generates synthetic historical degradation trajectories for ML RUL model training.
        """
        records = []
        fault_modes = ["normal", "misfire", "injector_coking", "lubrication_loss", "combustion_instability", "overheating", "abnormal_vibration"]
        
        for eng_id in range(1, num_engines + 1):
            life_hours = np.random.randint(400, max_hours)
            primary_fault = np.random.choice(fault_modes[1:])
            fault_onset_hr = int(life_hours * np.random.uniform(0.5, 0.75))
            
            for hr in range(0, life_hours, 5):
                rul_hours = life_hours - hr
                health_fraction = max(0.0, 1.0 - (hr / life_hours)**1.8)
                
                if hr >= fault_onset_hr:
                    severity = min(1.0, (hr - fault_onset_hr) / (life_hours - fault_onset_hr))
                    current_fault = primary_fault
                else:
                    severity = 0.0
                    current_fault = "normal"
                    
                frame = self.generate_frame(
                    profile="Normal Cruise",
                    fault_type=current_fault,
                    severity=severity,
                    step=hr
                )
                frame["engine_id"] = eng_id
                frame["operating_hours"] = hr
                frame["rul_hours"] = float(rul_hours)
                frame["true_health_fraction"] = float(health_fraction)
                records.append(frame)
                
        return pd.DataFrame(records)

if __name__ == "__main__":
    syn = TelemetrySynthesizer()
    df = syn.generate_run_to_failure_dataset(num_engines=3, max_hours=200)
    print(f"Generated synthetic training set: {df.shape} rows")
    print(df.head())
