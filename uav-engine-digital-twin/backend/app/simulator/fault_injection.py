"""
Fault Injection Module for Perturbing Engine Telemetry Signals.
"""

class FaultInjector:
    FAULTS = {
        "cylinder_misfire": {"egt_c": -120.0, "vibration_g": 1.8},
        "injector_coking": {"fuel_flow_lph": -3.5, "egt_c": 65.0},
        "lubrication_degradation": {"oil_pressure_psi": -25.0, "oil_temp_c": 28.0},
        "overheating": {"cht_c": 42.0, "egt_c": 55.0},
        "abnormal_vibration": {"vibration_g": 2.5}
    }

    @classmethod
    def apply_fault(cls, sample: dict, fault_name: str) -> dict:
        if fault_name not in cls.FAULTS:
            return sample

        modified = sample.copy()
        deltas = cls.FAULTS[fault_name]
        for key, delta in deltas.items():
            if key in modified:
                modified[key] = round(modified[key] + delta, 2)
        return modified
