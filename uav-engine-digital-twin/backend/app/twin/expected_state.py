"""
Expected State Physics Equations (Section 10.2).
"""

def expected_oil_pressure(oil_temp_c: float, rpm: float) -> float:
    base = 62.0
    temp_penalty = max(oil_temp_c - 90.0, 0) * 0.18
    rpm_adjustment = (rpm - 4000.0) * 0.0008
    return round(base - temp_penalty + rpm_adjustment, 2)

def expected_egt(throttle_pct: float, altitude_ft: float) -> float:
    return round(470.0 + throttle_pct * 3.0 + altitude_ft * 0.001, 2)

def expected_cht(throttle_pct: float, ambient_temp_c: float) -> float:
    return round(110.0 + throttle_pct * 1.0 + max(ambient_temp_c, 0) * 0.15, 2)

def expected_fuel_flow(throttle_pct: float) -> float:
    return round(3.0 + throttle_pct * 0.22, 2)

def compute_all_expected_states(sample: dict) -> dict:
    throttle = sample.get("throttle_pct", 65.0)
    altitude = sample.get("altitude_ft", 10000.0)
    ambient = sample.get("ambient_temp_c", 15.0)
    oil_temp = sample.get("oil_temp_c", 90.0)
    rpm = sample.get("rpm", 4200.0)

    return {
        "rpm": round(900 + throttle * 48, 1),
        "cht_c": expected_cht(throttle, ambient),
        "egt_c": expected_egt(throttle, altitude),
        "oil_pressure_psi": expected_oil_pressure(oil_temp, rpm),
        "oil_temp_c": round(75 + throttle * 0.22, 1),
        "fuel_flow_lph": expected_fuel_flow(throttle),
        "vibration_g": round(0.15 + throttle * 0.0025, 3)
    }
