"""
Digital Twin Service Layer.
"""

from app.twin.twin_engine import DigitalTwinEngine
from app.schemas.twin import TwinState

class TwinService:
    def __init__(self):
        self.twin_engine = DigitalTwinEngine()

    def evaluate_twin_state(self, telemetry_sample: dict) -> TwinState:
        result = self.twin_engine.process_telemetry_frame(telemetry_sample)
        return TwinState(**result)
