"""
Runtime Feature Builder (Section 11.2).
"""

FEATURES = [
    "rpm",
    "cht_c",
    "egt_c",
    "oil_pressure_psi",
    "oil_temp_c",
    "fuel_flow_lph",
    "vibration_g",
    "battery_voltage_v",
    "throttle_pct",
    "rpm_mean_10",
    "oil_pressure_slope_30",
    "oil_temp_slope_30",
    "vibration_mean_10"
]

def extract_features_single_sample(sample: dict) -> list:
    rpm = sample.get("rpm", 4200.0)
    oil_p = sample.get("oil_pressure_psi", 60.0)
    oil_t = sample.get("oil_temp_c", 90.0)
    vib = sample.get("vibration_g", 0.2)

    return [
        rpm,
        sample.get("cht_c", 180.0),
        sample.get("egt_c", 700.0),
        oil_p,
        oil_t,
        sample.get("fuel_flow_lph", 18.0),
        vib,
        sample.get("battery_voltage_v", 27.8),
        sample.get("throttle_pct", 65.0),
        rpm,     # rpm_mean_10
        0.0,     # oil_pressure_slope_30
        0.0,     # oil_temp_slope_30
        vib      # vibration_mean_10
    ]
