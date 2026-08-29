-- AeroTwin-PX v2: PostgreSQL / TimescaleDB Core DDL Schema (Section 8.1)

CREATE TABLE IF NOT EXISTS missions (
    id SERIAL PRIMARY KEY,
    mission_id VARCHAR(64) UNIQUE NOT NULL,
    mission_name VARCHAR(120) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'CREATED',
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    planned_duration_minutes INTEGER,
    altitude_ft DOUBLE PRECISION,
    ambient_temp_c DOUBLE PRECISION,
    throttle_profile VARCHAR(50),
    scenario VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS telemetry (
    id BIGSERIAL PRIMARY KEY,
    mission_id VARCHAR(64) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    rpm DOUBLE PRECISION,
    cht_c DOUBLE PRECISION,
    egt_c DOUBLE PRECISION,
    oil_pressure_psi DOUBLE PRECISION,
    oil_temp_c DOUBLE PRECISION,
    fuel_flow_lph DOUBLE PRECISION,
    vibration_g DOUBLE PRECISION,
    battery_voltage_v DOUBLE PRECISION,
    alternator_voltage_v DOUBLE PRECISION,
    injection_timing_deg DOUBLE PRECISION,
    altitude_ft DOUBLE PRECISION,
    ambient_temp_c DOUBLE PRECISION,
    throttle_pct DOUBLE PRECISION
);

CREATE INDEX IF NOT EXISTS idx_telemetry_mission_time
ON telemetry(mission_id, timestamp);

CREATE TABLE IF NOT EXISTS twin_states (
    id BIGSERIAL PRIMARY KEY,
    mission_id VARCHAR(64) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    overall_health DOUBLE PRECISION,
    combustion_health DOUBLE PRECISION,
    lubrication_health DOUBLE PRECISION,
    thermal_health DOUBLE PRECISION,
    fuel_health DOUBLE PRECISION,
    mechanical_health DOUBLE PRECISION,
    electrical_health DOUBLE PRECISION,
    expected_state JSONB,
    deviation_pct JSONB
);

CREATE TABLE IF NOT EXISTS predictions (
    id BIGSERIAL PRIMARY KEY,
    mission_id VARCHAR(64) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    anomaly_score DOUBLE PRECISION,
    is_anomaly BOOLEAN,
    predicted_fault VARCHAR(80),
    fault_confidence DOUBLE PRECISION,
    fault_probabilities JSONB,
    degradation_rate DOUBLE PRECISION,
    rul_hours DOUBLE PRECISION
);

CREATE TABLE IF NOT EXISTS alerts (
    id BIGSERIAL PRIMARY KEY,
    mission_id VARCHAR(64) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    alert_type VARCHAR(80),
    severity VARCHAR(20),
    message TEXT,
    status VARCHAR(20) DEFAULT 'ACTIVE',
    source VARCHAR(40)
);

CREATE TABLE IF NOT EXISTS maintenance_advisories (
    id BIGSERIAL PRIMARY KEY,
    mission_id VARCHAR(64) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    fault VARCHAR(80),
    priority VARCHAR(20),
    recommendation TEXT,
    predicted_rul_hours DOUBLE PRECISION
);

CREATE TABLE IF NOT EXISTS mission_events (
    id BIGSERIAL PRIMARY KEY,
    mission_id VARCHAR(64) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    event_type VARCHAR(80),
    event_label VARCHAR(160),
    details JSONB
);
