# UAV Engine Digital Twin (SIH26054 / DRDO iDEX)

AI-Enabled Real-Time Digital Twin System for Health Monitoring, Fault Prediction, RUL Estimation, and Mission Reliability of Aero-Piston Engines used in MALE-UAVs.

## Project Structure

```text
uav-engine-digital-twin/
├── docs/             # Technical architecture, API contracts, and validation docs
├── data/             # Raw, generated telemetry, processed features, and YAML configs
├── ml/               # Machine Learning notebooks, training scripts, and model registry
├── backend/          # FastAPI backend services, physics engine, EKF, and WebSockets
└── frontend/         # React GCS Dashboard with Three.js 3D WebGL Digital Twin
```

## Quick Start

### 1. Run via Docker Compose
```bash
docker-compose up --build
```

### 6.4 Local Startup Order

1. **Step 34**: Start PostgreSQL database.
   ```bash
   docker-compose up -d db
   ```
2. **Step 35**: Create database schema and run migrations.
   ```bash
   cd backend && alembic upgrade head
   ```
3. **Step 36**: Train or copy ML model artifacts into `ml/models/`.
   ```bash
   python ml/training/train_anomaly.py && python ml/training/train_fault.py && python ml/training/train_rul.py
   ```
4. **Step 37**: Start FastAPI backend server.
   ```bash
   cd backend && uvicorn app.main:app --reload --port 8000
   ```
5. **Step 38**: Start React frontend development server.
   ```bash
   cd frontend && npm run dev
   ```
6. **Step 39**: Open the UI at `http://localhost:5173`, log in, configure a mission, and start simulation.
7. **Step 40**: Verify WebSocket live updates and database writes.

