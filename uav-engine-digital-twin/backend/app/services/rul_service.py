"""
RUL Estimation Service (Section 11.1 & 11.5).
Defendable Mode: Lubrication Degradation & Bearing Wear Trajectory.
"""

class RULService:
    def estimate_rul(self, sample: dict, degradation_rate: float) -> float:
        base_rul = 350.0
        oil_p = sample.get("oil_pressure_psi", 60.0)
        oil_t = sample.get("oil_temp_c", 90.0)
        vib = sample.get("vibration_g", 0.2)

        penalty = max(0, 60.0 - oil_p) * 4.0 + max(0, oil_t - 90.0) * 2.5 + max(0, vib - 0.2) * 120.0
        rul_hours = max(5.0, round(base_rul - penalty + (degradation_rate * 10), 1))
        return rul_hours
