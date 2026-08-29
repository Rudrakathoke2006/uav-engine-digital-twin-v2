# System Architecture & Technical Specifications

## SIH26054 / DRDO iDEX MALE-UAV Aero Piston Digital Twin

### End-to-End Pipeline

```text
[Engine Telemetry / CAN Bus]
           │
           ▼
[Edge Layer: B-Spline Signal Reconstruction & SocketCAN]
           │
           ▼
[FastAPI Backend / Streamlit Core]
   ├── MVEM Physics Model & EKF State Estimator
   ├── Subsystem Health Engine (EHI)
   ├── AI Diagnostics Suite (Isolation Forest + XGBoost + SHAP)
   └── Rolling Degradation RUL Estimator
           │
           ▼
[Persistence & Security: SQLite 14-Table DB & HMAC-SHA256 Merkle Ledger]
           │
           ▼
[Ground Control Station HMI: Three.js 3D WebGL Canvas & Raycaster Tooltips]
```

### Core Subsystem Descriptions

1. **Digital Twin Core**: Integrates an atmospheric ISA air density model and Mean Value Engine Model (MVEM) equations to generate thermodynamic expected values ($\text{EGT}_{\text{exp}}$, $\text{CHT}_{\text{exp}}$, $\text{OilP}_{\text{exp}}$, $\text{Fuel}_{\text{exp}}$, $\text{Vib}_{\text{exp}}$). Extended Kalman Filter (EKF) state estimation derives physics residual vectors ($\Delta S = \text{Actual} - \text{Expected}$).
2. **Subsystem Health Engine**: Fuses 8 parameters across 11 channels to evaluate Combustion, Thermal, Lubrication, Mechanical, and Electrical health scores, yielding a composite **Engine Health Index (EHI)** (0–100%).
3. **AI Diagnostics & XAI**: Multi-class XGBoost classifier identifies 7 fault taxonomies (*Cylinder Misfire*, *Injector Coking*, *Lubrication Failure*, *Sensor Drift*, *Combustion Instability*, *Thermal Overheating*, *Abnormal Vibration*). SHAP calculates top-3 feature attribution weights.
4. **3D WebGL Visualization**: Three.js canvas featuring 5 camera view buttons (`[UAV VIEW]`, `[ENGINE VIEW]`, `[CUTAWAY]`, `[DIAGNOSTIC VIEW]`, `[RESET]`), 11 mouseover Raycaster sensor tooltips, and mesh fault localization.

---

## 23. Exact Runtime Sequence (Steps 41–72)

1. **Step 41**: Operator opens Mission Simulator page.
2. **Step 42**: Operator configures mission duration, altitude, ambient temperature, throttle profile, and scenario.
3. **Step 43**: Frontend sends `POST /api/missions` to create a mission.
4. **Step 44**: Backend writes the mission row to PostgreSQL.
5. **Step 45**: Operator clicks Start Mission.
6. **Step 46**: Frontend calls `POST /api/missions/{id}/start`.
7. **Step 47**: Backend starts `SimulatorRunner` in an asynchronous/background task.
8. **Step 48**: `SimulatorRunner` asks `MissionProfile` for current throttle/load.
9. **Step 49**: `EngineModel` calculates nominal telemetry.
10. **Step 50**: `EnvironmentModel` modifies the nominal response for altitude/temperature/scenario.
11. **Step 51**: `FaultInjection` modifies telemetry only if a configured fault is active.
12. **Step 52**: Pydantic `TelemetrySample` validates the sample.
13. **Step 53**: `TelemetryService` stores the raw sample.
14. **Step 54**: `TwinEngine` computes expected state.
15. **Step 55**: `Deviation` module computes actual-vs-expected percentage deviations.
16. **Step 56**: `HealthIndices` computes subsystem and overall health.
17. **Step 57**: `TwinService` stores the twin state.
18. **Step 58**: `FeatureBuilder` updates the rolling sensor window.
19. **Step 59**: Anomaly predictor returns anomaly score/status.
20. **Step 60**: Fault predictor returns class probabilities.
21. **Step 61**: Degradation service updates health slope and degradation trend.
22. **Step 62**: RUL predictor estimates remaining useful life for supported degradation mode.
23. **Step 63**: `PredictionService` stores prediction outputs.
24. **Step 64**: `AlertService` evaluates thresholds/rules and creates new alert only if state transition requires it.
25. **Step 65**: `MaintenanceService` creates or updates recommendation.
26. **Step 66**: `MissionEventService` records important replay markers.
27. **Step 67**: WebSocket manager broadcasts the integrated state.
28. **Step 68**: React receives the JSON and updates cards/charts without page reload.
29. **Step 69**: The loop waits for the configured telemetry interval (1000ms) and repeats.
30. **Step 70**: When mission stops, final summaries are calculated and mission status becomes `COMPLETED`.
31. **Step 71**: Mission History displays the completed mission.
32. **Step 72**: Mission Replay reads the same stored timeline and replays it deterministically.

---

## 27. Deployment Progression Roadmap

```text
Local Laptop Demo (FastAPI + Streamlit + WebGL)
       │
       ▼
Docker Compose (Containerized Multi-Service Deployment)
       │
       ▼
Cloud VM / College Server (Remote GCS Access)
       │
       ▼
Future Engine Test Rig
       │
       ▼
CAN / ECU / FADEC Adapter (SocketCAN Ingestion)
       │
       ▼
Edge / GCS Operational Deployment
```

