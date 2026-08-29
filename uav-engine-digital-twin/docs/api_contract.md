# API Contract Specifications

## REST API Endpoints

### 1. Missions
- `POST /api/missions`: Create a new mission configuration.
- `POST /api/missions/{id}/start`: Start live simulation stream.
- `POST /api/missions/{id}/stop`: Stop simulation stream.
- `GET /api/missions`: List mission history.

### 2. Live Telemetry & Digital Twin
- `GET /api/telemetry/{id}/latest`: Fetch current telemetry frame.
- `GET /api/twin/{id}/latest`: Fetch current Digital Twin state ($\Delta S$, EHI, expected vs actual).
- `GET /api/analytics/{id}/latest`: Fetch AI predictions (anomaly score, fault class, SHAP, RUL).

### 3. Simulation & Replay
- `POST /api/simulation/{id}/inject-fault`: Inject synthetic fault scenario.
- `GET /api/replay/{id}/timeline`: Retrieve historical mission timeline markers.
- `GET /api/replay/{id}/frame`: Retrieve synchronized frame at specific replay timestamp.

## WebSocket Streaming

- `WS /ws/missions/{id}`: Real-time broadcast emitting integrated JSON payload every 1000ms.
