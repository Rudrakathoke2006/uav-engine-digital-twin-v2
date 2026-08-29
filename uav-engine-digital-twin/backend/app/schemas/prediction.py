from pydantic import BaseModel

class PredictionState(BaseModel):
    anomaly_score: float = 0.72
    is_anomaly: bool = True
    predicted_fault: str = "lubrication_degradation"
    fault_confidence: float = 0.87
    fault_probabilities: dict = {
        "normal": 0.04,
        "lubrication_degradation": 0.87,
        "overheating": 0.03,
        "injector_fault": 0.04,
        "abnormal_vibration": 0.02
    }
    degradation_rate_pct_per_hour: float = -1.3
    rul_hours: float = 27.4
