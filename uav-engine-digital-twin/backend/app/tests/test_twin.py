"""
Test Digital Twin Suite (Section 26).
"""

from app.twin.expected_state import expected_oil_pressure
from app.twin.deviation import percent_deviation
from app.twin.health_indices import health_from_deviation

def test_expected_state_and_deviation():
    exp_oil_p = expected_oil_pressure(oil_temp_c=90.0, rpm=4000.0)
    assert exp_oil_p == 62.0

    dev = percent_deviation(actual=55.8, expected=62.0)
    assert dev == -10.0

    health = health_from_deviation(abs_deviation_pct=10.0, warning_pct=5.0, critical_pct=25.0)
    assert 0.0 < health < 100.0
