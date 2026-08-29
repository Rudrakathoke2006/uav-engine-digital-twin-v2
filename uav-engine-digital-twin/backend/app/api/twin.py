"""
Digital Twin Router: Twin state endpoints.
"""

from fastapi import APIRouter
from app.services.twin_service import TwinService
from app.services.telemetry_service import TelemetryService
from dataclasses import asdict

router = APIRouter(prefix="/twin", tags=["Digital Twin"])
twin_service = TwinService()
telemetry_service = TelemetryService()

@router.get("/{mission_id}/latest")
def get_latest_twin_state(mission_id: str):
    sample = telemetry_service.get_latest_sample(mission_id)
    return twin_service.evaluate_twin_state(sample.model_dump())
