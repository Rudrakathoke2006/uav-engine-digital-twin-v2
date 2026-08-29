"""
Maintenance Advisory Rule Engine (Section 19.1 & 19.2).
"""

from pydantic import BaseModel

class PredictionModel(BaseModel):
    predicted_fault: str
    fault_confidence: float
    rul_hours: float
    anomaly_score: float

class TwinModel(BaseModel):
    lubrication_health: float
    thermal_health: float
    combustion_health: float
    mechanical_health: float

def build_maintenance_advisory(prediction: PredictionModel, twin: TwinModel) -> dict | None:
    """Section 19.2 Rule Engine function."""
    if (
        prediction.predicted_fault == "lubrication_degradation"
        and prediction.fault_confidence >= 0.75
        and twin.lubrication_health < 75
    ):
        return {
            "subsystem": "Lubrication",
            "priority": "HIGH" if prediction.rul_hours < 24 else "MEDIUM",
            "recommendation": (
                "Inspect lubrication system, oil level, oil pressure circuit "
                "and mechanical vibration before the next mission."
            )
        }

    if (
        prediction.predicted_fault == "overheating"
        and prediction.fault_confidence >= 0.70
        and twin.thermal_health < 75
    ):
        return {
            "subsystem": "Thermal",
            "priority": "HIGH" if prediction.rul_hours < 20 else "MEDIUM",
            "recommendation": (
                "Inspect liquid cooling shroud, radiator airflow, cylinder head "
                "thermocouple wiring, and oil cooler thermal valve."
            )
        }

    return None
