"""
Analytics Router: AI/ML predictive outputs.
"""

from fastapi import APIRouter
from app.services.anomaly_service import AnomalyService
from app.services.fault_service import FaultService
from app.services.degradation_service import DegradationService
from app.services.rul_service import RULService
from app.services.telemetry_service import TelemetryService

router = APIRouter(prefix="/analytics", tags=["Analytics"])
anomaly_svc = AnomalyService()
fault_svc = FaultService()
deg_svc = DegradationService()
rul_svc = RULService()
telemetry_svc = TelemetryService()

@router.get("/{mission_id}/latest")
def get_analytics(mission_id: str):
    sample = telemetry_svc.get_latest_sample(mission_id).model_dump()
    anom = anomaly_svc.predict_anomaly(sample)
    fault = fault_svc.predict_fault(sample, anom["anomaly_score"])
    deg_rate = deg_svc.compute_degradation_rate(95.0, fault["predicted_fault"])
    rul = rul_svc.estimate_rul(sample, deg_rate)

    return {
        "anomaly_score": anom["anomaly_score"],
        "is_anomaly": anom["is_anomaly"],
        "predicted_fault": fault["predicted_fault"],
        "fault_confidence": fault["fault_confidence"],
        "fault_probabilities": fault["fault_probabilities"],
        "degradation_rate_pct_per_hour": deg_rate,
        "rul_hours": rul
    }
