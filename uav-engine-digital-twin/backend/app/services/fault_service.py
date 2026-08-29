"""
Fault Classification Service (Section 11.1 & 11.4).
"""

class FaultService:
    def predict_fault(self, sample: dict, anomaly_score: float) -> dict:
        if anomaly_score <= 0.45:
            return {
                "predicted_fault": "normal",
                "fault_confidence": 0.95,
                "fault_probabilities": {
                    "normal": 0.95,
                    "lubrication_degradation": 0.02,
                    "overheating": 0.01,
                    "injector_fault": 0.01,
                    "abnormal_vibration": 0.01
                }
            }

        # Fault signature matching rules
        oil_p = sample.get("oil_pressure_psi", 60.0)
        egt = sample.get("egt_c", 700.0)
        vib = sample.get("vibration_g", 0.2)

        if oil_p < 45.0:
            fault = "lubrication_degradation"
            conf = 0.88
        elif egt > 760.0:
            fault = "overheating"
            conf = 0.85
        elif vib > 0.8:
            fault = "abnormal_vibration"
            conf = 0.82
        else:
            fault = "injector_fault"
            conf = 0.76

        probs = {"normal": 0.04, fault: conf}
        for f in ["lubrication_degradation", "overheating", "injector_fault", "abnormal_vibration"]:
            if f not in probs:
                probs[f] = round((1.0 - conf - 0.04) / 3, 2)

        return {
            "predicted_fault": fault,
            "fault_confidence": conf,
            "fault_probabilities": probs
        }
