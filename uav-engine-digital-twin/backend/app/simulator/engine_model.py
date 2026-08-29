"""
Rotax 914 Turbo Aero-Piston Physics Engine Model (Section 9.3).
"""

from dataclasses import dataclass
import random

@dataclass
class EngineState:
    rpm: float
    cht_c: float
    egt_c: float
    oil_pressure_psi: float
    oil_temp_c: float
    fuel_flow_lph: float
    vibration_g: float
    battery_voltage_v: float
    alternator_voltage_v: float
    injection_timing_deg: float

class EngineModel:
    def step(self, throttle_pct: float, altitude_ft: float = 10000.0, ambient_temp_c: float = 15.0) -> EngineState:
        # Illustrative physics equations for aero-piston engine
        rpm = 900 + throttle_pct * 48 + random.gauss(0, 20)
        fuel_flow = 3.0 + throttle_pct * 0.22 + random.gauss(0, 0.2)
        egt = 470 + throttle_pct * 3.1 + altitude_ft * 0.001 + random.gauss(0, 3)
        cht = 110 + throttle_pct * 1.0 + max(ambient_temp_c, 0) * 0.15 + random.gauss(0, 2)
        oil_temp = 75 + throttle_pct * 0.22 + random.gauss(0, 1)
        oil_pressure = 63 - max(oil_temp - 90, 0) * 0.18 + random.gauss(0, 0.6)
        vibration = 0.15 + throttle_pct * 0.0025 + random.gauss(0, 0.01)

        return EngineState(
            rpm=round(rpm, 1),
            cht_c=round(cht, 1),
            egt_c=round(egt, 1),
            oil_pressure_psi=round(oil_pressure, 1),
            oil_temp_c=round(oil_temp, 1),
            fuel_flow_lph=round(fuel_flow, 2),
            vibration_g=round(vibration, 3),
            battery_voltage_v=27.8,
            alternator_voltage_v=28.1,
            injection_timing_deg=18.0,
        )
