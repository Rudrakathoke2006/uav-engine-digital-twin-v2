from pydantic import BaseModel

class TelemetrySample(BaseModel):
    mission_id: str = "ISR-2026-001"
    timestamp: str = "2026-08-25T12:00:01Z"
    rpm: float = 4200.0
    cht_c: float = 184.0
    egt_c: float = 710.0
    oil_pressure_psi: float = 58.0
    oil_temp_c: float = 92.0
    fuel_flow_lph: float = 18.2
    vibration_g: float = 0.34
    battery_voltage_v: float = 27.8
    alternator_voltage_v: float = 28.1
    injection_timing_deg: float = 18.0
    altitude_ft: float = 18000.0
    ambient_temp_c: float = -8.0
    throttle_pct: float = 72.0
