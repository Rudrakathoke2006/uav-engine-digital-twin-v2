from pydantic import BaseModel

class TwinState(BaseModel):
    mission_id: str = "ISR-2026-001"
    timestamp: str
    expected: dict = {
        "rpm": 4180,
        "cht_c": 181,
        "egt_c": 700,
        "oil_pressure_psi": 60
    }
    deviation_pct: dict = {
        "rpm": 0.48,
        "cht_c": 1.66,
        "egt_c": 1.43,
        "oil_pressure_psi": -3.33
    }
    health: dict = {
        "overall": 91.0,
        "combustion": 94.0,
        "lubrication": 88.0,
        "thermal": 92.0,
        "mechanical": 90.0,
        "electrical": 97.0
    }
