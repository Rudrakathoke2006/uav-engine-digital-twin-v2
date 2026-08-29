"""
Deterministic Mission Replay Service (Section 13.1 & 13.2).
"""

from sqlalchemy.orm import Session
from app.database.models import Telemetry, TwinStateModel, Prediction, MissionEvent
from datetime import datetime

class ReplayEventTypes:
    MISSION_STARTED = "MISSION_STARTED"
    FIRST_PARAMETER_DEVIATION = "FIRST_PARAMETER_DEVIATION"
    ANOMALY_DETECTED = "ANOMALY_DETECTED"
    FAULT_RISK_INCREASED = "FAULT_RISK_INCREASED"
    HEALTH_BELOW_80 = "HEALTH_BELOW_80"
    RUL_BELOW_THRESHOLD = "RUL_BELOW_THRESHOLD"
    MAINTENANCE_ADVISORY_CREATED = "MAINTENANCE_ADVISORY_CREATED"
    MISSION_STOPPED = "MISSION_STOPPED"

class ReplayService:
    def get_replay_frame(self, db: Session, mission_id: str, timestamp: datetime) -> dict:
        """Section 13.2: Synchronized playback frame at or before specified timestamp."""
        telemetry = db.query(Telemetry).filter(
            Telemetry.mission_id == mission_id,
            Telemetry.timestamp <= timestamp
        ).order_by(Telemetry.timestamp.desc()).first()

        twin = db.query(TwinStateModel).filter(
            TwinStateModel.mission_id == mission_id,
            TwinStateModel.timestamp <= timestamp
        ).order_by(TwinStateModel.timestamp.desc()).first()

        prediction = db.query(Prediction).filter(
            Prediction.mission_id == mission_id,
            Prediction.timestamp <= timestamp
        ).order_by(Prediction.timestamp.desc()).first()

        events = db.query(MissionEvent).filter(
            MissionEvent.mission_id == mission_id,
            MissionEvent.timestamp <= timestamp
        ).order_by(MissionEvent.timestamp.asc()).all()

        return {
            "mission_id": mission_id,
            "target_timestamp": timestamp.isoformat(),
            "telemetry": telemetry,
            "twin": twin,
            "prediction": prediction,
            "events": events
        }
