from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, missions, telemetry, twin, analytics, alerts, maintenance, simulation, replay
from app.websocket import stream

app = FastAPI(title="UAV Engine Digital Twin API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://localhost:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(missions.router, prefix="/api")
app.include_router(telemetry.router, prefix="/api")
app.include_router(twin.router, prefix="/api")
app.include_router(analytics.router, prefix="/api")
app.include_router(alerts.router, prefix="/api")
app.include_router(maintenance.router, prefix="/api")
app.include_router(simulation.router, prefix="/api")
app.include_router(replay.router, prefix="/api")
app.include_router(stream.router)

@app.get("/health")
def health():
    return {"status": "ok"}
