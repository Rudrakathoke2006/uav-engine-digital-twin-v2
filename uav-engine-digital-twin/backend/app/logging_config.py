"""
Structured Logging & Audit Configuration (Section 25).
Logs mission start/stop, fault injections, schema rejections, and ML model exceptions.
"""

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s"
)

logger = logging.getLogger("uav_engine_digital_twin")

def log_mission_event(mission_id: str, action: str, details: str = ""):
    logger.info(f"MISSION [{mission_id}] - Action: {action} | Details: {details}")

def log_fault_injection(mission_id: str, fault_name: str):
    logger.warning(f"FAULT INJECTION [{mission_id}] - Injected Fault: {fault_name}")

def log_schema_rejection(mission_id: str, field_name: str, value: float):
    logger.error(f"SCHEMA REJECTION [{mission_id}] - Impossible value for '{field_name}': {value}")

def log_ml_failure(model_name: str, err: Exception):
    logger.error(f"ML MODEL EXCEPTION [{model_name}] - {str(err)} (Prediction marked UNAVAILABLE)")
