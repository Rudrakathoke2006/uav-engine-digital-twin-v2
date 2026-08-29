"""
WebSocket Real-Time Stream Router (Section 16.2 & 16.3).
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.websocket.manager import ConnectionManager
from app.services.telemetry_service import TelemetryService
from app.services.twin_service import TwinService
from app.services.anomaly_service import AnomalyService
from app.services.fault_service import FaultService
from app.services.degradation_service import DegradationService
from app.services.rul_service import RULService
import asyncio

router = APIRouter(prefix="/ws", tags=["WebSocket Stream"])
manager = ConnectionManager()
telemetry_svc = TelemetryService()
twin_svc = TwinService()
anomaly_svc = AnomalyService()
fault_svc = FaultService()
deg_svc = DegradationService()
rul_svc = RULService()

@router.websocket("/missions/{mission_id}")
async def websocket_stream(websocket: WebSocket, mission_id: str):
    await manager.connect(mission_id, websocket)
    try:
        while True:
            sample = telemetry_svc.get_latest_sample(mission_id).model_dump()
            twin_state = twin_svc.evaluate_twin_state(sample).model_dump()
            anom = anomaly_svc.predict_anomaly(sample)
            fault = fault_svc.predict_fault(sample, anom["anomaly_score"])
            deg_rate = deg_svc.compute_degradation_rate(twin_state["health"]["overall"], fault["predicted_fault"])
            rul = rul_svc.estimate_rul(sample, deg_rate)

            payload = {
                "type": "LIVE_STATE",
                "mission_id": mission_id,
                "telemetry": sample,
                "twin": twin_state,
                "prediction": {
                    "anomaly_score": anom["anomaly_score"],
                    "is_anomaly": anom["is_anomaly"],
                    "predicted_fault": fault["predicted_fault"],
                    "fault_confidence": fault["fault_confidence"],
                    "fault_probabilities": fault["fault_probabilities"],
                    "degradation_rate_pct_per_hour": deg_rate,
                    "rul_hours": rul
                },
                "active_alerts": [
                    {
                        "severity": "WARNING" if anom["is_anomaly"] else "INFO",
                        "message": f"Engine status: {fault['predicted_fault']}"
                    }
                ]
            }

            await manager.broadcast(mission_id, payload)
            await asyncio.sleep(1.0)
    except WebSocketDisconnect:
        manager.disconnect(mission_id, websocket)
