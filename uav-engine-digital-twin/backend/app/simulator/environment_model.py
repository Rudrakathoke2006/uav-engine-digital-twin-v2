"""
International Standard Atmosphere (ISA) Model.
"""

import math

class EnvironmentModel:
    @staticmethod
    def get_air_density_ratio(altitude_ft: float, ambient_temp_c: float) -> float:
        """Calculates air density ratio relative to sea-level ISA standard (1.225 kg/m^3)."""
        alt_m = altitude_ft * 0.3048
        temp_k = ambient_temp_c + 273.15
        p_ratio = math.exp(-alt_m / 8400.0)
        density_ratio = p_ratio * (288.15 / temp_k)
        return max(0.4, min(1.2, density_ratio))
