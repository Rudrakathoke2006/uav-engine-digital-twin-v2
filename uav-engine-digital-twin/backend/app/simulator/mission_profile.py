"""
Mission Configuration & Scenario Modifiers (Section 12.1, 12.2 & 12.3).
"""

def throttle_at(minute: float, segments: list[dict]) -> float:
    """Calculates active throttle percentage at a specific mission minute."""
    if not segments:
        return 65.0
    for segment in segments:
        if segment["start_min"] <= minute < segment["end_min"]:
            return float(segment["throttle_pct"])
    return float(segments[-1]["throttle_pct"])

class MissionProfile:
    DEFAULT_MISSION_CONFIG = {
        "mission_name": "Long Endurance ISR",
        "planned_duration_minutes": 360,
        "altitude_ft": 18000,
        "ambient_temp_c": -8,
        "scenario": "LONG_ENDURANCE",
        "throttle_profile": [
            {"start_min": 0, "end_min": 10, "throttle_pct": 90},
            {"start_min": 10, "end_min": 300, "throttle_pct": 65},
            {"start_min": 300, "end_min": 330, "throttle_pct": 80},
            {"start_min": 330, "end_min": 360, "throttle_pct": 55}
        ]
    }

    @staticmethod
    def apply_scenario_modifiers(sample: dict, scenario: str, elapsed_minute: float) -> dict:
        """Applies Section 12.3 scenario environmental & degradation modifiers."""
        mod = sample.copy()

        if scenario == "HIGH_ALTITUDE":
            # Modify expected combustion/performance response with altitude
            mod["egt_c"] = round(mod.get("egt_c", 700.0) + 25.0, 1)
            mod["fuel_flow_lph"] = round(mod.get("fuel_flow_lph", 18.0) * 0.92, 2)

        elif scenario == "HOT_WEATHER":
            # Raise thermal loading and cooling challenge
            mod["cht_c"] = round(mod.get("cht_c", 180.0) + 18.0, 1)
            mod["oil_temp_c"] = round(mod.get("oil_temp_c", 90.0) + 12.0, 1)

        elif scenario == "LONG_ENDURANCE":
            # Accumulate thermal and degradation effects over time
            thermal_buildup = min(15.0, (elapsed_minute / 360.0) * 15.0)
            mod["oil_temp_c"] = round(mod.get("oil_temp_c", 90.0) + thermal_buildup, 1)

        elif scenario == "RAPID_THROTTLE":
            # Create repeated transient response instead of steady cruise
            transient_vib = 0.15 * (1.0 if int(elapsed_minute) % 2 == 0 else -0.5)
            mod["vibration_g"] = round(max(0.05, mod.get("vibration_g", 0.2) + transient_vib), 3)

        return mod
