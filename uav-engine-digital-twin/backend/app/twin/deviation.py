"""
Deviation & Delta Vector Calculation (Section 10.3).
"""

def percent_deviation(actual: float, expected: float) -> float:
    if expected == 0:
        return 0.0
    return round(((actual - expected) / expected) * 100.0, 2)

def compute_deviations(actual_state: dict, expected_state: dict) -> dict:
    deviations = {}
    for key, expected_val in expected_state.items():
        if key in actual_state:
            actual_val = actual_state[key]
            deviations[key] = percent_deviation(actual_val, expected_val)
    return deviations
