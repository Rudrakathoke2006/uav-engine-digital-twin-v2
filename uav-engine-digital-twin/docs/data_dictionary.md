# Telemetry & Physics Data Dictionary

## 1. Engine Sensors & Parameters

| Parameter Key | Parameter Name | Unit | Nominal Range | Sensor ID | Description |
| :--- | :--- | :---: | :---: | :---: | :--- |
| `rpm` | Engine Speed | RPM | 2500 - 5200 | `SENS_RPM` | Rotax 914 crankshaft rotation speed |
| `cht_c` | Cylinder Head Temperature | °C | 120 - 210 | `SENS_CHT` | Thermal cylinder loading |
| `egt_c` | Exhaust Gas Temperature | °C | 500 - 780 | `SENS_EGT` | Exhaust manifold combustion temperature |
| `oil_pressure_psi` / `bar` | Oil Pressure | bar | 2.5 - 5.5 | `SENS_OILP` | Lubrication circuit pressure |
| `oil_temp_c` | Oil Temperature | °C | 70 - 115 | `SENS_OILT` | Sump oil thermal state |
| `fuel_flow_lph` / `lh` | Fuel Flow Rate | L/h | 5.5 - 28.0 | `SENS_FUEL` | Metered fuel consumption |
| `vibration_g` / `rms` | Vibration RMS | mm/s | 0.05 - 3.5 | `SENS_VIB` | Crankcase accelerometer vibration |
| `battery_voltage_v` | Battery Voltage | V | 24.0 - 28.5 | `SENS_VOLT` | DC bus electrical potential |
| `alternator_voltage_v` | Alternator Current | A | 15.0 - 45.0 | `SENS_ALT` | Electrical generation load |
| `injection_timing_deg` | Injection Timing | °BTDC | 14.0 - 22.0 | `SENS_INJ` | Electronic fuel injection timing |
| `map_kpa` | Manifold Absolute Pressure | kPa | 30.0 - 115.0 | `SENS_MAP` | Turbocharger manifold pressure |

## 2. Calculated Subsystem Health Metrics

- **Combustion Health (%)**: Derived from EGT residual, MAP, and injection timing.
- **Thermal Health (%)**: Derived from CHT residual and oil temperature.
- **Lubrication Health (%)**: Derived from oil pressure residual and oil temperature.
- **Mechanical Health (%)**: Derived from vibration RMS residual and RPM stability.
- **Electrical Health (%)**: Derived from battery voltage and alternator current.
- **Engine Health Index (EHI, %)**: Composite weighted average across all 5 subsystems.
