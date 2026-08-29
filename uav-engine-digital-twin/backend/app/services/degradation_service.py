"""
Degradation Tracking Service (Section 11.1).
"""

class DegradationService:
    def compute_degradation_rate(self, ehi: float, fault: str) -> float:
        if fault == "normal" or ehi >= 95.0:
            return 0.0
        elif fault == "lubrication_degradation":
            return -1.8
        elif fault == "overheating":
            return -2.4
        else:
            return -0.8
