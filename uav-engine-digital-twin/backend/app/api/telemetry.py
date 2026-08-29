"""
Telemetry Router: Sensor data endpoints.
"""

from fastapi import APIRouter
from app.services.telemetry_service import TelemetryService

router = APIRouter(prefix="/telemetry", tags=["Telemetry"])
service = TelemetryService()

@router.get("/{mission_id}/latest")
def get_latest_telemetry(mission_id: str):
    return service.get_latest_sample(mission_id)

@router.get("/{mission_id}/history")
def get_telemetry_history(mission_id: str):
    return [service.get_latest_sample(mission_id)]
