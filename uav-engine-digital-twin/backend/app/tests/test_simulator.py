"""
Test Simulator Suite (Section 26).
"""

from app.simulator.engine_model import EngineModel

def test_engine_model_throttle_response():
    engine = EngineModel()
    low_state = engine.step(throttle_pct=20.0)
    high_state = engine.step(throttle_pct=90.0)

    assert high_state.rpm > low_state.rpm
    assert high_state.egt_c > low_state.egt_c
    assert high_state.fuel_flow_lph > low_state.fuel_flow_lph
    assert 2500 <= high_state.rpm <= 5800
