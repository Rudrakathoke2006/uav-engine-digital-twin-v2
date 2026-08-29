"""
Database Repository helper operations for telemetry, twin states, and predictions.
"""

from sqlalchemy.orm import Session
from app.database.models import Mission, Telemetry, TwinStateModel, Prediction, Alert

def create_mission(db: Session, mission_id: str, name: str):
    mission = Mission(id=mission_id, name=name)
    db.add(mission)
    db.commit()
    db.refresh(mission)
    return mission

def get_latest_telemetry(db: Session, mission_id: str):
    return db.query(Telemetry).filter(Telemetry.mission_id == mission_id).order_by(Telemetry.timestamp.desc()).first()

def get_mission_alerts(db: Session, mission_id: str):
    return db.query(Alert).filter(Alert.mission_id == mission_id).order_by(Alert.timestamp.desc()).all()
