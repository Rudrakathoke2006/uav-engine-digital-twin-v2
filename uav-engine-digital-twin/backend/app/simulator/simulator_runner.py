"""
Simulator Runner Pipeline (Section 9.4).
"""

from app.simulator.engine_model import EngineModel
from app.simulator.environment_model import EnvironmentModel
from app.simulator.mission_profile import MissionProfile
from app.simulator.fault_injection import FaultInjector
from dataclasses import asdict
from datetime import datetime

class SimulatorRunner:
    def __init__(self):
        self.engine = EngineModel()

    def run_pipeline_step(self, mission_id: str, profile_name: str = "normal_cruise", fault_name: str = "normal") -> dict:
        # 1. Mission profile
        profile = MissionProfile.get_profile(profile_name)
        
        # 2. EngineModel.step()
        state = self.engine.step(profile["throttle_pct"], profile["altitude_ft"], profile["ambient_temp_c"])
        sample = asdict(state)

        # 3. Environment adjustments
        air_density = EnvironmentModel.get_air_density_ratio(profile["altitude_ft"], profile["ambient_temp_c"])
        sample["egt_c"] = round(sample["egt_c"] * (1.0 / (air_density ** 0.3)), 1)

        # 4. FaultInjection.apply()
        sample = FaultInjector.apply_fault(sample, fault_name)

        # 5. Metadata
        sample.update({
            "mission_id": mission_id,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "altitude_ft": profile["altitude_ft"],
            "ambient_temp_c": profile["ambient_temp_c"],
            "throttle_pct": profile["throttle_pct"]
        })

        return sample
