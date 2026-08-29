-- ============================================================================
-- AeroTwin-PX: Hackathon MVP Database Schema (14 Essential Tables)
-- High-Performance SQLite / PostgreSQL Compatible Schema
-- ============================================================================

-- 1. ENGINE MASTER
CREATE TABLE IF NOT EXISTS engine (
    engine_id TEXT PRIMARY KEY,
    engine_serial_number TEXT UNIQUE NOT NULL,
    model_name TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'ACTIVE',
    total_operating_hours REAL DEFAULT 0.0,
    current_health_score REAL DEFAULT 100.0,
    current_rul_hours REAL DEFAULT 350.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. SENSOR MASTER
CREATE TABLE IF NOT EXISTS sensor (
    sensor_id TEXT PRIMARY KEY,
    engine_id TEXT NOT NULL,
    sensor_name TEXT NOT NULL,
    parameter_name TEXT NOT NULL,
    unit TEXT NOT NULL,
    status TEXT DEFAULT 'ACTIVE',
    FOREIGN KEY(engine_id) REFERENCES engine(engine_id)
);

-- 3. TELEMETRY SESSION
CREATE TABLE IF NOT EXISTS telemetry_session (
    session_id TEXT PRIMARY KEY,
    engine_id TEXT NOT NULL,
    mission_code TEXT NOT NULL,
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'ACTIVE',
    FOREIGN KEY(engine_id) REFERENCES engine(engine_id)
);

-- 4. WIDE ENGINE TELEMETRY (High-Frequency Analytics Stream)
CREATE TABLE IF NOT EXISTS engine_telemetry (
    telemetry_id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp REAL NOT NULL,
    session_id TEXT NOT NULL,
    engine_id TEXT NOT NULL,
    altitude_ft REAL NOT NULL,
    ambient_temp_c REAL NOT NULL,
    throttle_pct REAL NOT NULL,
    map_kpa REAL NOT NULL,
    rpm REAL NOT NULL,
    cht_c REAL NOT NULL,
    egt_c REAL NOT NULL,
    oil_pressure_bar REAL NOT NULL,
    oil_temp_c REAL NOT NULL,
    fuel_flow_lh REAL NOT NULL,
    vibration_rms REAL NOT NULL,
    battery_volt REAL NOT NULL,
    alternator_curr REAL NOT NULL,
    injection_timing_deg REAL NOT NULL,
    FOREIGN KEY(session_id) REFERENCES telemetry_session(session_id),
    FOREIGN KEY(engine_id) REFERENCES engine(engine_id)
);

-- 5. PHYSICS RESIDUALS (Key Digital Twin Differentiator: Delta S)
CREATE TABLE IF NOT EXISTS physics_residual (
    residual_id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp REAL NOT NULL,
    engine_id TEXT NOT NULL,
    delta_egt_c REAL NOT NULL,
    delta_cht_c REAL NOT NULL,
    delta_oil_pressure_bar REAL NOT NULL,
    delta_oil_temp_c REAL NOT NULL,
    delta_fuel_flow_lh REAL NOT NULL,
    delta_vibration_rms REAL NOT NULL,
    FOREIGN KEY(engine_id) REFERENCES engine(engine_id)
);

-- 6. ENGINE HEALTH INDICATORS (Subsystems + Overall EHI)
CREATE TABLE IF NOT EXISTS health_indicator (
    health_id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp REAL NOT NULL,
    engine_id TEXT NOT NULL,
    combustion_health REAL NOT NULL,
    thermal_health REAL NOT NULL,
    lubrication_health REAL NOT NULL,
    mechanical_health REAL NOT NULL,
    electrical_health REAL NOT NULL,
    overall_ehi REAL NOT NULL,
    digital_twin_confidence REAL NOT NULL,
    FOREIGN KEY(engine_id) REFERENCES engine(engine_id)
);

-- 7. ANOMALY EVENTS (Isolation Forest Output)
CREATE TABLE IF NOT EXISTS anomaly_event (
    anomaly_id INTEGER PRIMARY KEY AUTOINCREMENT,
    engine_id TEXT NOT NULL,
    timestamp REAL NOT NULL,
    anomaly_score REAL NOT NULL,
    is_anomaly INTEGER NOT NULL,
    FOREIGN KEY(engine_id) REFERENCES engine(engine_id)
);

-- 8. FAULT EVENTS (XGBoost Diagnostic Alert)
CREATE TABLE IF NOT EXISTS fault_event (
    fault_event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    engine_id TEXT NOT NULL,
    timestamp REAL NOT NULL,
    fault_name TEXT NOT NULL,
    severity REAL NOT NULL,
    confidence_pct REAL NOT NULL,
    status TEXT DEFAULT 'ACTIVE',
    FOREIGN KEY(engine_id) REFERENCES engine(engine_id)
);

-- 9. FAULT EVIDENCE (SHAP Feature Attribution Drivers)
CREATE TABLE IF NOT EXISTS fault_evidence (
    evidence_id INTEGER PRIMARY KEY AUTOINCREMENT,
    fault_event_id INTEGER NOT NULL,
    timestamp REAL NOT NULL,
    feature_name TEXT NOT NULL,
    feature_value REAL NOT NULL,
    contribution_score REAL NOT NULL,
    FOREIGN KEY(fault_event_id) REFERENCES fault_event(fault_event_id)
);

-- 10. RUL PREDICTIONS (Expected Hours + 80% CI Bounds)
CREATE TABLE IF NOT EXISTS rul_prediction (
    rul_id INTEGER PRIMARY KEY AUTOINCREMENT,
    engine_id TEXT NOT NULL,
    timestamp REAL NOT NULL,
    predicted_rul_hours REAL NOT NULL,
    lower_bound_hours REAL NOT NULL,
    upper_bound_hours REAL NOT NULL,
    FOREIGN KEY(engine_id) REFERENCES engine(engine_id)
);

-- 11. MISSION WHAT-IF SIMULATIONS
CREATE TABLE IF NOT EXISTS simulation_run (
    simulation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    engine_id TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    planned_duration_hrs REAL NOT NULL,
    target_altitude_ft REAL NOT NULL,
    ambient_temp_c REAL NOT NULL,
    cruise_throttle_pct REAL NOT NULL,
    FOREIGN KEY(engine_id) REFERENCES engine(engine_id)
);

-- 12. MISSION RELIABILITY (Monte Carlo Aggregates)
CREATE TABLE IF NOT EXISTS mission_reliability (
    reliability_id INTEGER PRIMARY KEY AUTOINCREMENT,
    simulation_id INTEGER NOT NULL,
    engine_id TEXT NOT NULL,
    completion_probability_pct REAL NOT NULL,
    failure_probability_pct REAL NOT NULL,
    projected_end_ehi REAL NOT NULL,
    risk_level TEXT NOT NULL,
    environmental_stress_factor REAL NOT NULL,
    maintenance_advisory TEXT NOT NULL,
    FOREIGN KEY(simulation_id) REFERENCES simulation_run(simulation_id),
    FOREIGN KEY(engine_id) REFERENCES engine(engine_id)
);

-- 13. CRYPTOGRAPHIC AUDIT LOG (HMAC-SHA256 Hash Chain)
CREATE TABLE IF NOT EXISTS audit_record (
    audit_id INTEGER PRIMARY KEY AUTOINCREMENT,
    record_index INTEGER NOT NULL,
    record_type TEXT NOT NULL,
    timestamp REAL NOT NULL,
    previous_hash TEXT NOT NULL,
    record_hash TEXT NOT NULL,
    payload_json TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 14. FAST MATERIALIZED CURRENT STATE VIEW (Sub-5ms UI Queries)
CREATE TABLE IF NOT EXISTS engine_current_state (
    engine_id TEXT PRIMARY KEY,
    timestamp REAL NOT NULL,
    rpm REAL NOT NULL,
    cht_c REAL NOT NULL,
    egt_c REAL NOT NULL,
    oil_pressure_bar REAL NOT NULL,
    oil_temp_c REAL NOT NULL,
    fuel_flow_lh REAL NOT NULL,
    vibration_rms REAL NOT NULL,
    battery_volt REAL NOT NULL,
    overall_ehi REAL NOT NULL,
    digital_twin_confidence REAL NOT NULL,
    health_status TEXT NOT NULL,
    predicted_fault TEXT NOT NULL,
    fault_confidence_pct REAL NOT NULL,
    anomaly_score REAL NOT NULL,
    rul_hours REAL NOT NULL,
    rul_min_hours REAL NOT NULL,
    rul_max_hours REAL NOT NULL,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- INDEXES FOR FAST QUERY PERFORMANCE
CREATE INDEX IF NOT EXISTS idx_telemetry_engine_ts ON engine_telemetry(engine_id, timestamp);
CREATE INDEX IF NOT EXISTS idx_residual_engine_ts ON physics_residual(engine_id, timestamp);
CREATE INDEX IF NOT EXISTS idx_health_engine_ts ON health_indicator(engine_id, timestamp);
CREATE INDEX IF NOT EXISTS idx_audit_index ON audit_record(record_index);
