"""
Test Fault Injection Suite (Section 26).
"""

from app.simulator.fault_injection import FaultInjector

def test_lubrication_degradation_fault():
    sample = {"oil_pressure_psi": 60.0, "oil_temp_c": 90.0, "vibration_g": 0.2}
    faulty = FaultInjector.apply_fault(sample, "lubrication_degradation")

    assert faulty["oil_pressure_psi"] < sample["oil_pressure_psi"]
    assert faulty["oil_temp_c"] > sample["oil_temp_c"]
