"""
AeroTwin-PX v2: Monte Carlo Mission Reliability & What-If Engine
Simulates mission completion probability and failure risk under varying flight envelopes.
"""

import numpy as np

class MissionReliabilityEngine:
    def __init__(self, num_simulations: int = 500):
        self.num_sims = num_simulations

    def evaluate_mission_reliability(
        self,
        current_ehi: float,
        subsystem_health: dict,
        rul_hours: float,
        predicted_fault: str,
        planned_duration_hrs: float = 6.0,
        target_altitude_ft: float = 15000.0,
        ambient_temp_c: float = 30.0,
        cruise_throttle_pct: float = 75.0
    ) -> dict:
        """
        Runs Monte Carlo simulations of the proposed mission to compute completion probability.
        """
        # Environmental Stress Multipliers
        alt_stress = 1.0 + max(0.0, (target_altitude_ft - 10000.0) / 20000.0)
        temp_stress = 1.0 + max(0.0, (ambient_temp_c - 20.0) / 50.0)
        throttle_stress = 1.0 + max(0.0, (cruise_throttle_pct - 65.0) / 70.0)
        
        combined_stress = alt_stress * temp_stress * throttle_stress
        
        # Subsystem bottleneck factor
        min_sub_health = min(subsystem_health.values()) if subsystem_health else current_ehi
        base_failure_rate_per_hr = 0.0005 * (100.0 / max(min_sub_health, 10.0))**1.8 * combined_stress
        
        if "Normal" not in predicted_fault:
            base_failure_rate_per_hr *= 2.8
            
        success_count = 0
        end_health_list = []
        
        for sim in range(self.num_sims):
            # Stochastic degradation step
            sim_ehi = current_ehi
            failed = False
            
            for step_hr in range(int(planned_duration_hrs)):
                # Hazard rate check
                hourly_p_fail = 1.0 - np.exp(-base_failure_rate_per_hr * (1.0 + 0.05 * step_hr))
                if np.random.rand() < hourly_p_fail:
                    failed = True
                    break
                    
                # EHI decay during flight
                decay = np.random.normal(0.4 * combined_stress, 0.1)
                sim_ehi = max(0.0, sim_ehi - decay)
                if sim_ehi < 30.0:
                    failed = True
                    break
                    
            if not failed:
                success_count += 1
                end_health_list.append(sim_ehi)
                
        completion_prob_pct = float(np.round((success_count / self.num_sims) * 100.0, 1))
        failure_prob_pct = float(np.round(100.0 - completion_prob_pct, 1))
        projected_end_ehi = float(np.round(np.mean(end_health_list) if end_health_list else 20.0, 1))
        
        # Risk Categorization
        if completion_prob_pct >= 94.0:
            risk_level = "LOW RISK"
            color = "green"
            advice = "Engine health is optimal. Proceed with standard mission profile."
        elif completion_prob_pct >= 82.0:
            risk_level = "MODERATE RISK"
            color = "blue"
            advice = "Mission feasible. Consider reducing cruise throttle by 5% or lowering altitude by 3,000 ft to conserve life."
        elif completion_prob_pct >= 65.0:
            risk_level = "HIGH RISK"
            color = "orange"
            advice = "High probability of operational degradation. Inspect fuel/cooling system prior to takeoff."
        else:
            risk_level = "CRITICAL RISK"
            color = "red"
            advice = "MISSION ABORT ADVISORY: High failure probability under target environmental envelope. Perform maintenance immediately."
            
        return {
            "mission_completion_prob_pct": completion_prob_pct,
            "failure_prob_pct": failure_prob_pct,
            "projected_end_health_index": projected_end_ehi,
            "risk_level": risk_level,
            "risk_color": color,
            "environmental_stress_factor": float(np.round(combined_stress, 2)),
            "maintenance_advisory": advice
        }

    def simulate_mission_reliability(
        self,
        mission_duration_min: float = 180,
        current_health: float = 95.0,
        current_rul: float = 250.0,
        fault_active: bool = False,
        n_runs: int = 500
    ) -> dict:
        """
        Wrapper method matching app.py tab4 Monte Carlo simulation call signature.
        """
        planned_hrs = max(0.5, mission_duration_min / 60.0)
        subsystem_dict = {
            "combustion_health": current_health,
            "thermal_health": current_health,
            "lubrication_health": current_health,
            "mechanical_health": current_health,
            "electrical_health": current_health
        }
        fault_str = "Cylinder Misfire" if fault_active else "Normal Operation"
        
        res = self.evaluate_mission_reliability(
            current_ehi=current_health,
            subsystem_health=subsystem_dict,
            rul_hours=current_rul,
            predicted_fault=fault_str,
            planned_duration_hrs=planned_hrs
        )
        
        # Distribution array for histogram
        dist = np.random.normal(res["projected_end_health_index"], 4.5, size=n_runs)
        dist = np.clip(dist, 0.0, 100.0)
        
        deg_rate = float(np.round(max(0.1, (current_health - res["projected_end_health_index"]) / planned_hrs), 2))
        
        return {
            "success_probability_pct": res["mission_completion_prob_pct"],
            "predicted_end_health_pct": res["projected_end_ehi" if "projected_end_ehi" in res else "projected_end_health_index"],
            "degradation_rate_per_hr": deg_rate,
            "end_health_distribution": dist,
            "risk_level": res["risk_level"],
            "maintenance_advisory": res["maintenance_advisory"]
        }

if __name__ == "__main__":
    mre = MissionReliabilityEngine()
    subs = {"combustion_health": 82.0, "thermal_health": 74.0, "lubrication_health": 90.0, "mechanical_health": 88.0, "electrical_health": 95.0}
    res = mre.evaluate_mission_reliability(current_ehi=81.8, subsystem_health=subs, rul_hours=140.0, predicted_fault="Injector Coking", planned_duration_hrs=8.0, target_altitude_ft=16000.0, ambient_temp_c=35.0)
    print("Mission Reliability Assessment:", res)
