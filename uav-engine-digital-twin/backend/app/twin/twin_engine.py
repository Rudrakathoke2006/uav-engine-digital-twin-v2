"""
Digital Twin Core Engine: Combines expected state, deviation %, and health indices.
"""

from app.twin.expected_state import compute_all_expected_states
from app.twin.deviation import compute_deviations
from app.twin.health_indices import compute_subsystem_health

class DigitalTwinEngine:
    def process_telemetry_frame(self, telemetry: dict) -> dict:
        expected = compute_all_expected_states(telemetry)
        deviations = compute_deviations(telemetry, expected)
        health = compute_subsystem_health(deviations)

        return {
            "mission_id": telemetry.get("mission_id", "ISR-2026-001"),
            "timestamp": telemetry.get("timestamp"),
            "expected": expected,
            "deviation_pct": deviations,
            "health": health
        }
