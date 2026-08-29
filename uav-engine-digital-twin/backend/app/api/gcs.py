import sys
import os
from typing import Optional, List, Dict, Any
import numpy as np
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# Resolve path to project root for core engines
current_file = os.path.abspath(__file__)
app_dir = os.path.dirname(os.path.dirname(current_file))
backend_dir = os.path.dirname(app_dir)
uav_dir = os.path.dirname(backend_dir)
root_dir = os.path.dirname(uav_dir)

for path in [root_dir, backend_dir]:
    if path not in sys.path:
        sys.path.insert(0, path)

from synthesizer import TelemetrySynthesizer
from physics_engine import EKFStateEstimator
from health_engine import EngineHealthEngine
from models import AIDiagnosticsSuite
from reliability_engine import MissionReliabilityEngine
from audit_log import CryptographicAuditLog
from database import AeroTwinDatabase
from twin_adapter import TwinVisualizationAdapter

router = APIRouter(prefix="/gcs", tags=["Ground Control Station"])

class GcsStateStore:
    def __init__(self):
        self.db = AeroTwinDatabase()
        self.synthesizer = TelemetrySynthesizer()
        self.ekf = EKFStateEstimator()
        self.health_engine = EngineHealthEngine()
        self.ai_suite = AIDiagnosticsSuite()
        self.reliability_engine = MissionReliabilityEngine()
        self.audit_log = CryptographicAuditLog()
        self.step = 0
        self.telemetry_history: List[Dict[str, Any]] = []
        self.current_profile = "Normal Cruise"
        self.current_fault_choice = "None / Healthy"
        self.current_fault_severity = 0.0

    def generate_and_process_step(
        self,
        profile: Optional[str] = None,
        fault_choice: Optional[str] = None,
        severity: Optional[float] = None,
        increment: bool = True
    ) -> Dict[str, Any]:
        if profile is not None:
            self.current_profile = profile
        if fault_choice is not None:
            self.current_fault_choice = fault_choice
        if severity is not None:
            self.current_fault_severity = severity

        if increment:
            self.step += 1

        fault_map_str = {
            "None / Healthy": "none",
            "Cylinder Misfire": "misfire",
            "Injector Coking": "injector_coking",
            "Lubrication Failure": "lubrication_loss",
            "Sensor Drift": "sensor_drift",
            "Combustion Instability": "combustion_instability",
            "Thermal Overheating": "overheating",
            "Abnormal Vibration": "abnormal_vibration"
        }
        fault_key = fault_map_str.get(self.current_fault_choice, "none")

        frame = self.synthesizer.generate_frame(
            profile=self.current_profile,
            fault_type=fault_key,
            severity=self.current_fault_severity,
            step=self.step
        )

        ekf_res = self.ekf.process_step(frame)
        residuals = ekf_res["physics_residuals"]
        mvem_exp = ekf_res["mvem_expected"]

        sensor_health = self.health_engine.evaluate_sensor_health(frame, residuals)
        subsystem_health = self.health_engine.compute_subsystem_health(frame, residuals)
        ai_res = self.ai_suite.predict_diagnostics(frame, residuals)

        twin_state = TwinVisualizationAdapter.extract_twin_state(
            telemetry=frame,
            mvem_exp=mvem_exp,
            ekf_est=ekf_res["ekf_estimated_state"],
            residuals=residuals,
            sensor_health=sensor_health,
            subsystem_health=subsystem_health,
            ai_res=ai_res
        )

        # Persist Frame to Database
        try:
            self.db.record_telemetry_step(
                engine_id="ENG-001",
                session_id="SESS_ISR-042",
                telemetry=frame,
                mvem_exp=mvem_exp,
                ekf_est=ekf_res["ekf_estimated_state"],
                residuals=residuals,
                health_info=subsystem_health,
                ai_info=ai_res
            )
        except Exception:
            pass

        # Log to Audit Ledger
        self.audit_log.append_record("TELEMETRY_FRAME", frame)
        if ai_res["is_anomaly"] or ai_res["fault_class_id"] != 0:
            self.audit_log.append_record("AI_DIAGNOSTIC_ALERT", {
                "fault": ai_res["predicted_fault"],
                "confidence": ai_res["fault_confidence_pct"],
                "anomaly_score": ai_res["anomaly_score"]
            })

        hist_entry = {
            **frame,
            **subsystem_health["subsystems"],
            "ehi": subsystem_health["engine_health_index"],
            "anomaly_score": ai_res["anomaly_score"]
        }
        self.telemetry_history.append(hist_entry)

        return {
            "step": self.step,
            "profile": self.current_profile,
            "fault_choice": self.current_fault_choice,
            "fault_severity": self.current_fault_severity,
            "frame": frame,
            "ekf_residuals": residuals,
            "mvem_expected": mvem_exp,
            "sensor_health": sensor_health,
            "subsystem_health": subsystem_health,
            "ai_res": ai_res,
            "twin_state": twin_state,
            "telemetry_history_count": len(self.telemetry_history)
        }

    def reset(self):
        self.step = 0
        self.telemetry_history = []
        self.audit_log = CryptographicAuditLog()
        return self.generate_and_process_step(increment=False)

gcs_store = GcsStateStore()

class StepControlRequest(BaseModel):
    profile: Optional[str] = "Normal Cruise"
    fault_choice: Optional[str] = "None / Healthy"
    fault_severity: Optional[float] = 0.0

class MonteCarloRequest(BaseModel):
    mission_duration_min: int = 180

@router.get("/state")
def get_current_state():
    if gcs_store.step == 0:
        return gcs_store.generate_and_process_step(increment=False)
    return gcs_store.generate_and_process_step(increment=False)

@router.post("/step")
def step_telemetry(req: StepControlRequest):
    return gcs_store.generate_and_process_step(
        profile=req.profile,
        fault_choice=req.fault_choice,
        severity=req.fault_severity,
        increment=True
    )

@router.post("/reset")
def reset_telemetry():
    return gcs_store.reset()

@router.post("/monte-carlo")
def run_monte_carlo(req: MonteCarloRequest):
    current = gcs_store.generate_and_process_step(increment=False)
    ehi = current["subsystem_health"]["engine_health_index"]
    rul_hrs = current["ai_res"]["rul_hours"]
    fault_active = (current["ai_res"]["fault_class_id"] != 0)

    sim_res = gcs_store.reliability_engine.simulate_mission_reliability(
        mission_duration_min=req.mission_duration_min,
        current_health=ehi,
        current_rul=rul_hrs,
        fault_active=fault_active,
        n_runs=500
    )
    return sim_res

@router.get("/audit/verify")
def verify_audit_ledger():
    return gcs_store.audit_log.verify_integrity()

@router.get("/audit/replay/{session_id}")
def replay_session(session_id: str):
    records = gcs_store.db.fetch_session_telemetry(session_id)
    return {"session_id": session_id, "count": len(records), "records": records}
