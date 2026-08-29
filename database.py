"""
AeroTwin-PX v2: Streamlined Database Manager (Hackathon MVP Schema)
Provides high-performance SQLite persistence across 14 core tables,
master data seeding, and sub-5ms current state queries.
"""

import sqlite3
import os
import json
import pandas as pd

class AeroTwinDatabase:
    def __init__(self, db_path: str = "aerotwin_mvp.db", schema_path: str = "schema.sql"):
        self.db_path = db_path
        self.schema_path = schema_path
        self.init_database()

    def get_connection(self):
        conn = sqlite3.connect(self.db_path, timeout=10.0)
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA synchronous=NORMAL;")
        conn.row_factory = sqlite3.Row
        return conn

    def init_database(self):
        """Executes DDL schema script and seeds master engine data."""
        try:
            if os.path.exists(self.schema_path):
                with open(self.schema_path, "r") as f:
                    schema_sql = f.read()
                with self.get_connection() as conn:
                    conn.executescript(schema_sql)
                    conn.commit()
            self.seed_master_data()
        except sqlite3.OperationalError:
            # Schema already initialized or database locked by active stream connection
            try:
                self.seed_master_data()
            except Exception:
                pass

    def seed_master_data(self):
        """Seeds default master data for Rotax 914 class aero-piston UAV engine."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Seed Engine Instance
            cursor.execute("SELECT COUNT(*) FROM engine")
            if cursor.fetchone()[0] == 0:
                cursor.execute("""
                    INSERT INTO engine (engine_id, engine_serial_number, model_name, status, total_operating_hours, current_health_score, current_rul_hours)
                    VALUES ('ENG-001', 'SN-ROTAX-914-8842', 'Rotax 914 Turbo (Flat-4)', 'ACTIVE', 142.5, 95.0, 350.0)
                """)

            # Seed Sensors
            cursor.execute("SELECT COUNT(*) FROM sensor")
            if cursor.fetchone()[0] == 0:
                sensors = [
                    ('SENS_RPM', 'ENG-001', 'Engine Speed', 'rpm', 'RPM'),
                    ('SENS_CHT', 'ENG-001', 'Cylinder Head Temp', 'cht_c', '°C'),
                    ('SENS_EGT', 'ENG-001', 'Exhaust Gas Temp', 'egt_c', '°C'),
                    ('SENS_OILP', 'ENG-001', 'Oil Pressure', 'oil_pressure_bar', 'bar'),
                    ('SENS_OILT', 'ENG-001', 'Oil Temperature', 'oil_temp_c', '°C'),
                    ('SENS_FUEL', 'ENG-001', 'Fuel Flow', 'fuel_flow_lh', 'L/h'),
                    ('SENS_VIB', 'ENG-001', 'Vibration RMS', 'vibration_rms', 'mm/s'),
                    ('SENS_VOLT', 'ENG-001', 'Battery Voltage', 'battery_volt', 'V')
                ]
                cursor.executemany("""
                    INSERT INTO sensor (sensor_id, engine_id, sensor_name, parameter_name, unit)
                    VALUES (?, ?, ?, ?, ?)
                """, sensors)

            conn.commit()

    def record_telemetry_step(
        self,
        engine_id: str,
        session_id: str,
        telemetry: dict,
        mvem_exp: dict,
        ekf_est: dict,
        residuals: dict,
        health_info: dict,
        ai_info: dict
    ):
        """
        Persists a synchronized live telemetry step across Wide Telemetry, Physics Residuals, EHI, and fast-view tables.
        """
        ts = telemetry["timestamp"]
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # 1. Insert Telemetry
            cursor.execute("""
                INSERT INTO engine_telemetry (
                    timestamp, session_id, engine_id, altitude_ft, ambient_temp_c, throttle_pct, map_kpa,
                    rpm, cht_c, egt_c, oil_pressure_bar, oil_temp_c, fuel_flow_lh, vibration_rms,
                    battery_volt, alternator_curr, injection_timing_deg
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                ts, session_id, engine_id, telemetry["altitude_ft"], telemetry["ambient_temp_c"], telemetry["throttle_pct"],
                telemetry["map_kpa"], telemetry["rpm"], telemetry["cht_c"], telemetry["egt_c"], telemetry["oil_pressure_bar"],
                telemetry["oil_temp_c"], telemetry["fuel_flow_lh"], telemetry["vibration_rms"], telemetry["battery_volt"],
                telemetry["alternator_curr"], telemetry["injection_timing_deg"]
            ))
            
            # 2. Insert Physics Residuals (Delta S)
            cursor.execute("""
                INSERT INTO physics_residual (
                    timestamp, engine_id, delta_egt_c, delta_cht_c, delta_oil_pressure_bar,
                    delta_oil_temp_c, delta_fuel_flow_lh, delta_vibration_rms
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                ts, engine_id, residuals["delta_egt_c"], residuals["delta_cht_c"], residuals["delta_oil_pressure_bar"],
                residuals["delta_oil_temp_c"], residuals["delta_fuel_flow_lh"], residuals["delta_vibration_rms"]
            ))
            
            # 3. Insert Health Indicators
            subs = health_info["subsystems"]
            cursor.execute("""
                INSERT INTO health_indicator (
                    timestamp, engine_id, combustion_health, thermal_health, lubrication_health,
                    mechanical_health, electrical_health, overall_ehi, digital_twin_confidence
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                ts, engine_id, subs["combustion_health"], subs["thermal_health"], subs["lubrication_health"],
                subs["mechanical_health"], subs["electrical_health"], health_info["engine_health_index"], ai_info.get("twin_confidence", 95.0)
            ))
            
            # 4. Insert Anomaly Event
            cursor.execute("""
                INSERT INTO anomaly_event (engine_id, timestamp, anomaly_score, is_anomaly)
                VALUES (?, ?, ?, ?)
            """, (engine_id, ts, ai_info["anomaly_score"], 1 if ai_info["is_anomaly"] else 0))
            
            # 5. Insert RUL Prediction
            rul_b = ai_info["rul_interval_hours"]
            cursor.execute("""
                INSERT INTO rul_prediction (engine_id, timestamp, predicted_rul_hours, lower_bound_hours, upper_bound_hours)
                VALUES (?, ?, ?, ?, ?)
            """, (engine_id, ts, ai_info["rul_hours"], rul_b[0], rul_b[1]))
            
            # 6. Update Fast-Query Current State View
            cursor.execute("""
                INSERT INTO engine_current_state (
                    engine_id, timestamp, rpm, cht_c, egt_c, oil_pressure_bar, oil_temp_c, fuel_flow_lh,
                    vibration_rms, battery_volt, overall_ehi, digital_twin_confidence, health_status,
                    predicted_fault, fault_confidence_pct, anomaly_score, rul_hours, rul_min_hours, rul_max_hours
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(engine_id) DO UPDATE SET
                    timestamp=excluded.timestamp, rpm=excluded.rpm, cht_c=excluded.cht_c, egt_c=excluded.egt_c,
                    oil_pressure_bar=excluded.oil_pressure_bar, oil_temp_c=excluded.oil_temp_c, fuel_flow_lh=excluded.fuel_flow_lh,
                    vibration_rms=excluded.vibration_rms, battery_volt=excluded.battery_volt, overall_ehi=excluded.overall_ehi,
                    digital_twin_confidence=excluded.digital_twin_confidence, health_status=excluded.health_status,
                    predicted_fault=excluded.predicted_fault, fault_confidence_pct=excluded.fault_confidence_pct,
                    anomaly_score=excluded.anomaly_score, rul_hours=excluded.rul_hours, rul_min_hours=excluded.rul_min_hours,
                    rul_max_hours=excluded.rul_max_hours, last_updated=CURRENT_TIMESTAMP
            """, (
                engine_id, ts, telemetry["rpm"], telemetry["cht_c"], telemetry["egt_c"], telemetry["oil_pressure_bar"],
                telemetry["oil_temp_c"], telemetry["fuel_flow_lh"], telemetry["vibration_rms"], telemetry["battery_volt"],
                health_info["engine_health_index"], ai_info.get("twin_confidence", 95.0), health_info["health_status"],
                ai_info["predicted_fault"], ai_info["fault_confidence_pct"], ai_info["anomaly_score"],
                ai_info["rul_hours"], rul_b[0], rul_b[1]
            ))
            
            # 7. Record Fault Events & SHAP Evidence
            if ai_info["fault_class_id"] != 0:
                cursor.execute("""
                    INSERT INTO fault_event (engine_id, timestamp, fault_name, severity, confidence_pct)
                    VALUES (?, ?, ?, ?, ?)
                """, (engine_id, ts, ai_info["predicted_fault"], ai_info["anomaly_score"], ai_info["fault_confidence_pct"]))
                
                f_id = cursor.lastrowid
                for top in ai_info.get("shap_top_contributors", []):
                    cursor.execute("""
                        INSERT INTO fault_evidence (fault_event_id, timestamp, feature_name, feature_value, contribution_score)
                        VALUES (?, ?, ?, ?, ?)
                    """, (f_id, ts, top["feature"], top["val"], top["shap_weight"]))

            conn.commit()

    def record_mission_reliability_run(self, engine_id: str, planned_params: dict, reliability_output: dict):
        """Persists Monte Carlo mission simulation results."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO simulation_run (engine_id, planned_duration_hrs, target_altitude_ft, ambient_temp_c, cruise_throttle_pct)
                VALUES (?, ?, ?, ?, ?)
            """, (
                engine_id, planned_params["duration"], planned_params["altitude"], planned_params["temp"], planned_params["throttle"]
            ))
            sim_id = cursor.lastrowid
            
            cursor.execute("""
                INSERT INTO mission_reliability (
                    simulation_id, engine_id, completion_probability_pct, failure_probability_pct,
                    projected_end_ehi, risk_level, environmental_stress_factor, maintenance_advisory
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                sim_id, engine_id, reliability_output["mission_completion_prob_pct"], reliability_output["failure_prob_pct"],
                reliability_output["projected_end_health_index"], reliability_output["risk_level"],
                reliability_output["environmental_stress_factor"], reliability_output["maintenance_advisory"]
            ))
            conn.commit()

    def get_current_state(self, engine_id: str = "ENG-001") -> dict:
        """Sub-5ms query fetching latest engine current state."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM engine_current_state WHERE engine_id = ?", (engine_id,))
            row = cursor.fetchone()
            if row:
                return dict(row)
            return {}

    def fetch_session_telemetry(self, session_id: str = "SESS_ISR-042") -> list:
        """Queries historical telemetry frames recorded for a specific session ID."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM engine_telemetry WHERE session_id = ? ORDER BY telemetry_id ASC
            """, (session_id,))
            rows = cursor.fetchall()
            return [dict(r) for r in rows]

if __name__ == "__main__":
    db = AeroTwinDatabase()
    print("AeroTwinDatabase initialized with 14-table Hackathon MVP schema!")
    print("Current State:", db.get_current_state())
