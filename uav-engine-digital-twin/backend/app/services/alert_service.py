"""
Alert Rule Engine (Section 19.1).
Inputs: Anomaly score, predicted fault, fault confidence, subsystem health, degradation rate, RUL, parameter deviations.
"""

def evaluate_alert_rules(sample: dict, twin_state: dict, prediction: dict) -> list[dict]:
    alerts = []
    anomaly_score = prediction.get("anomaly_score", 0.0)
    predicted_fault = prediction.get("predicted_fault", "normal")
    fault_confidence = prediction.get("fault_confidence", 0.0)
    overall_health = twin_state.get("health", {}).get("overall", 100.0)
    rul_hours = prediction.get("rul_hours", 300.0)

    # 1. Anomaly threshold rule
    if anomaly_score > 0.65:
        alerts.append({
            "severity": "CRITICAL",
            "alert_type": "HIGH_ANOMALY_SCORE",
            "message": f"Critical engine anomaly score ({anomaly_score}) detected by Isolation Forest."
        })
    elif anomaly_score > 0.45:
        alerts.append({
            "severity": "WARNING",
            "alert_type": "MODERATE_ANOMALY_SCORE",
            "message": f"Moderate engine anomaly score ({anomaly_score}) detected."
        })

    # 2. Fault classification rule
    if predicted_fault != "normal" and fault_confidence >= 0.70:
        alerts.append({
            "severity": "WARNING" if fault_confidence < 0.85 else "CRITICAL",
            "alert_type": "FAULT_DETECTED",
            "message": f"Predicted fault: {predicted_fault} (Confidence: {int(fault_confidence * 100)}%)."
        })

    # 3. Low RUL rule
    if rul_hours < 24.0:
        alerts.append({
            "severity": "CRITICAL",
            "alert_type": "CRITICAL_RUL_LOW",
            "message": f"Remaining Useful Life is low ({rul_hours} hours remaining)."
        })

    return alerts
