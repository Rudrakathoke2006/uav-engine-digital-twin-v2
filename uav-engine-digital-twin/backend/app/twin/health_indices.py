"""
Subsystem Health Indices & Weighted Multi-Signal Composition (Section 10.4 & 10.5).
"""

def health_from_deviation(abs_deviation_pct: float, warning_pct: float, critical_pct: float) -> float:
    if abs_deviation_pct <= warning_pct:
        return 100.0
    if abs_deviation_pct >= critical_pct:
        return 0.0

    span = critical_pct - warning_pct
    penalty_fraction = (abs_deviation_pct - warning_pct) / span
    return max(0.0, 100.0 * (1.0 - penalty_fraction))

def compute_subsystem_health(deviations: dict) -> dict:
    dev_oil_p = abs(deviations.get("oil_pressure_psi", 0.0))
    dev_oil_t = abs(deviations.get("oil_temp_c", 0.0))
    dev_vib = abs(deviations.get("vibration_g", 0.0))
    dev_cht = abs(deviations.get("cht_c", 0.0))
    dev_egt = abs(deviations.get("egt_c", 0.0))
    dev_fuel = abs(deviations.get("fuel_flow_lph", 0.0))
    dev_rpm = abs(deviations.get("rpm", 0.0))
    dev_volt = abs(deviations.get("battery_voltage_v", 0.0))

    # Signal health scores
    h_oil_p = health_from_deviation(dev_oil_p, 5.0, 25.0)
    h_oil_t = health_from_deviation(dev_oil_t, 5.0, 20.0)
    h_vib = health_from_deviation(dev_vib, 10.0, 50.0)
    h_cht = health_from_deviation(dev_cht, 4.0, 18.0)
    h_egt = health_from_deviation(dev_egt, 3.0, 15.0)
    h_fuel = health_from_deviation(dev_fuel, 5.0, 25.0)
    h_rpm = health_from_deviation(dev_rpm, 2.0, 10.0)
    h_volt = health_from_deviation(dev_volt, 3.0, 12.0)

    # Subsystem Compositions (Section 10.5)
    lubrication = 0.50 * h_oil_p + 0.30 * h_oil_t + 0.20 * h_vib
    thermal = 0.50 * h_cht + 0.50 * h_egt
    combustion = 0.40 * h_egt + 0.30 * h_fuel + 0.30 * h_rpm
    mechanical = 0.70 * h_vib + 0.30 * h_rpm
    electrical = h_volt
    fuel = h_fuel

    overall = (lubrication * 0.25 + thermal * 0.25 + combustion * 0.20 + mechanical * 0.15 + electrical * 0.15)

    return {
        "overall": round(overall, 1),
        "lubrication": round(lubrication, 1),
        "thermal": round(thermal, 1),
        "combustion": round(combustion, 1),
        "mechanical": round(mechanical, 1),
        "electrical": round(electrical, 1),
        "fuel": round(fuel, 1)
    }
