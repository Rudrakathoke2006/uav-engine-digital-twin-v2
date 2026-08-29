"""
Missions Router: Mission lifecycle endpoints.
"""

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/missions", tags=["Missions"])

class MissionCreate(BaseModel):
    mission_name: str = "ISR-2026-001"
    scenario: str = "LONG_ENDURANCE"
    planned_duration_minutes: int = 360

@router.post("")
def create_mission(req: MissionCreate):
    return {"mission_id": "ISR-2026-001", "status": "CREATED", "name": req.mission_name}

@router.post("/{mission_id}/start")
def start_mission(mission_id: str):
    return {"mission_id": mission_id, "status": "RUNNING", "message": "Telemetry simulation started"}

@router.post("/{mission_id}/stop")
def stop_mission(mission_id: str):
    return {"mission_id": mission_id, "status": "STOPPED", "message": "Telemetry simulation stopped"}

@router.get("")
def list_missions():
    return [{"mission_id": "ISR-2026-001", "name": "Long Endurance ISR", "status": "ACTIVE"}]

@router.get("/{mission_id}")
def get_mission(mission_id: str):
    return {"mission_id": mission_id, "name": "Long Endurance ISR", "status": "ACTIVE", "duration": 360}
