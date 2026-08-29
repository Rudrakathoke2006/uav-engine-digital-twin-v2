"""
Feature Builder for AI/ML Analytics (Section 11.2).
"""

import pandas as pd
import numpy as np

FEATURES = [
    "rpm",
    "cht_c",
    "egt_c",
    "oil_pressure_psi",
    "oil_temp_c",
    "fuel_flow_lph",
    "vibration_g",
    "battery_voltage_v",
    "throttle_pct",
    "rpm_mean_10",
    "oil_pressure_slope_30",
    "oil_temp_slope_30",
    "vibration_mean_10"
]

def build_features_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df_out = df.copy()
    
    # 10-step rolling means
    df_out["rpm_mean_10"] = df_out["rpm"].rolling(window=10, min_periods=1).mean()
    df_out["vibration_mean_10"] = df_out["vibration_g"].rolling(window=10, min_periods=1).mean()
    
    # 30-step trend slopes
    df_out["oil_pressure_slope_30"] = df_out["oil_pressure_psi"].diff(periods=5).fillna(0.0) / 5.0
    df_out["oil_temp_slope_30"] = df_out["oil_temp_c"].diff(periods=5).fillna(0.0) / 5.0
    
    return df_out[FEATURES]
