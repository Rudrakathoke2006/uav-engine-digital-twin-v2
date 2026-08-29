"""
Maintenance Router: Inspection advisories.
"""

from fastapi import APIRouter

router = APIRouter(prefix="/maintenance", tags=["Maintenance"])

@router.get("/{mission_id}")
def get_maintenance_advisories(mission_id: str):
    return [
        {
            "advisory_id": 101,
            "subsystem": "Lubrication",
            "recommended_action": "Inspect oil filter circuit and check oil pump pressure relief valve",
            "urgency": "HIGH"
        }
    ]
