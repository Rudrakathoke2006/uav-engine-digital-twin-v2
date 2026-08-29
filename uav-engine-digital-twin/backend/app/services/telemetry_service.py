"""
Telemetry Service Layer: Ingests raw telemetry and coordinates storage and broadcast.
"""

from app.simulator.simulator_runner import SimulatorRunner
from app.schemas.telemetry import TelemetrySample

class TelemetryService:
    def __init__(self):
        self.runner = SimulatorRunner()

    def get_latest_sample(self, mission_id: str, profile: str = "normal_cruise", fault: str = "normal") -> TelemetrySample:
        sample_dict = self.runner.generate_step(mission_id, profile, fault)
        return TelemetrySample(**sample_dict)
