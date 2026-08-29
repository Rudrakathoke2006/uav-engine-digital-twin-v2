"""
AeroTwin-PX v2: SQLAlchemy ORM Models mirroring Section 8.1 PostgreSQL DDL Schema.
"""

from sqlalchemy import Column, Integer, BigInteger, String, Float, Boolean, DateTime, JSON, Text
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    role = Column(String(20), default="operator")
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Mission(Base):
    __tablename__ = "missions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    mission_id = Column(String(64), unique=True, nullable=False)
    mission_name = Column(String(120), nullable=False)
    status = Column(String(20), nullable=False, default="CREATED")
    start_time = Column(DateTime, nullable=True)
    end_time = Column(DateTime, nullable=True)
    planned_duration_minutes = Column(Integer, nullable=True)
    altitude_ft = Column(Float, nullable=True)
    ambient_temp_c = Column(Float, nullable=True)
    throttle_profile = Column(String(50), nullable=True)
    scenario = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Telemetry(Base):
    __tablename__ = "telemetry"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    mission_id = Column(String(64), nullable=False, index=True)
    timestamp = Column(DateTime, nullable=False, index=True)
    rpm = Column(Float)
    cht_c = Column(Float)
    egt_c = Column(Float)
    oil_pressure_psi = Column(Float)
    oil_temp_c = Column(Float)
    fuel_flow_lph = Column(Float)
    vibration_g = Column(Float)
    battery_voltage_v = Column(Float)
    alternator_voltage_v = Column(Float)
    injection_timing_deg = Column(Float)
    altitude_ft = Column(Float)
    ambient_temp_c = Column(Float)
    throttle_pct = Column(Float)

class TwinStateModel(Base):
    __tablename__ = "twin_states"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    mission_id = Column(String(64), nullable=False)
    timestamp = Column(DateTime, nullable=False)
    overall_health = Column(Float)
    combustion_health = Column(Float)
    lubrication_health = Column(Float)
    thermal_health = Column(Float)
    fuel_health = Column(Float)
    mechanical_health = Column(Float)
    electrical_health = Column(Float)
    expected_state = Column(JSON)
    deviation_pct = Column(JSON)

class Prediction(Base):
    __tablename__ = "predictions"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    mission_id = Column(String(64), nullable=False)
    timestamp = Column(DateTime, nullable=False)
    anomaly_score = Column(Float)
    is_anomaly = Column(Boolean)
    predicted_fault = Column(String(80))
    fault_confidence = Column(Float)
    fault_probabilities = Column(JSON)
    degradation_rate = Column(Float)
    rul_hours = Column(Float)

class Alert(Base):
    __tablename__ = "alerts"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    mission_id = Column(String(64), nullable=False)
    timestamp = Column(DateTime, nullable=False)
    alert_type = Column(String(80))
    severity = Column(String(20))
    message = Column(Text)
    status = Column(String(20), default="ACTIVE")
    source = Column(String(40))

class MaintenanceAdvisory(Base):
    __tablename__ = "maintenance_advisories"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    mission_id = Column(String(64), nullable=False)
    timestamp = Column(DateTime, nullable=False)
    fault = Column(String(80))
    priority = Column(String(20))
    recommendation = Column(Text)
    predicted_rul_hours = Column(Float)

class MissionEvent(Base):
    __tablename__ = "mission_events"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    mission_id = Column(String(64), nullable=False)
    timestamp = Column(DateTime, nullable=False)
    event_type = Column(String(80))
    event_label = Column(String(160))
    details = Column(JSON)
