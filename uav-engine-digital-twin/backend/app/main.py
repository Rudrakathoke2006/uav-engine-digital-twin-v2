from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import gcs

app = FastAPI(title="AeroTwin-PX v2 Defense Avionics API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount GCS router under both /gcs and /api/gcs to guarantee Vercel path matching
app.include_router(gcs.router)
app.include_router(gcs.router, prefix="/api")

# Safely mount legacy routers if available
try:
    from app.api import auth, missions, telemetry, twin, analytics, alerts, maintenance, simulation, replay
    for r in [auth, missions, telemetry, twin, analytics, alerts, maintenance, simulation, replay]:
        app.include_router(r.router)
        app.include_router(r.router, prefix="/api")
except Exception as e:
    print(f"Notice: Optional legacy routers skipped: {e}")

@app.get("/")
@app.get("/api")
def root():
    return {"status": "ok", "message": "AeroTwin-PX v2 Defense Avionics API is live", "swagger_docs": "/docs"}

@app.get("/health")
@app.get("/api/health")
def health():
    return {"status": "ok"}
