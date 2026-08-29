"""
Alerts Router: Operational alerts & acknowledgements.
"""

from fastapi import APIRouter

router = APIRouter(prefix="/alerts", tags=["Alerts"])

@router.get("/{mission_id}")
def get_alerts(mission_id: str):
    return [
        {
            "alert_id": 1,
            "mission_id": mission_id,
            "severity": "WARNING",
            "alert_type": "HIGH_EGT_DELTA",
            "message": "EGT residual delta exceeds +25.0 degC",
            "status": "ACTIVE"
        }
    ]

@router.post("/{alert_id}/ack")
def acknowledge_alert(alert_id: int):
    return {"alert_id": alert_id, "status": "ACKNOWLEDGED", "message": "Alert acknowledged by operator"}
