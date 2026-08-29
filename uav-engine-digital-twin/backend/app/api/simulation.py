"""
Simulation Router: Synthetic fault injection.
"""

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/simulation", tags=["Simulation"])

class FaultInjectionRequest(BaseModel):
    fault_name: str = "lubrication_degradation"

@router.post("/{mission_id}/inject-fault")
def inject_fault(mission_id: str, req: FaultInjectionRequest):
    return {
        "mission_id": mission_id,
        "injected_fault": req.fault_name,
        "status": "ACTIVE",
        "message": f"Synthetic fault '{req.fault_name}' injected into telemetry stream"
    }
