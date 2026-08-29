"""
Replay Router: Timeline and synchronized replay frames.
"""

from fastapi import APIRouter

router = APIRouter(prefix="/replay", tags=["Replay"])

@router.get("/{mission_id}/timeline")
def get_replay_timeline(mission_id: str):
    return {
        "mission_id": mission_id,
        "total_frames": 360,
        "events": [
            {"event_type": "MISSION_STARTED", "time": "2026-08-25T12:00:00Z"},
            {"event_type": "ANOMALY_DETECTED", "time": "2026-08-25T12:15:30Z"}
        ]
    }

@router.get("/{mission_id}/frame")
def get_replay_frame(mission_id: str, timestamp: str):
    return {
        "mission_id": mission_id,
        "timestamp": timestamp,
        "telemetry": {"rpm": 4200.0, "egt_c": 710.0, "oil_pressure_psi": 58.0},
        "twin": {"overall_health": 91.0},
        "prediction": {"anomaly_score": 0.72, "predicted_fault": "lubrication_degradation"}
    }
