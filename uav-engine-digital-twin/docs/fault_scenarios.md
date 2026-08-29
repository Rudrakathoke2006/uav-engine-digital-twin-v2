# Synthetic Fault Injection Scenarios

## Fault Profiles & Telemetry Perturbations

### 1. Cylinder Misfire
- **Primary Perturbations**: EGT drops abruptly; vibration RMS spikes; RPM instability increases.
- **Affected Subsystem**: Combustion & Mechanical.
- **3D Mesh Localization**: Cylinder Head #1 highlighted in RED.

### 2. Injector Coking / Abnormality
- **Primary Perturbations**: Fuel flow drops below MVEM expectation ($\Delta \text{Fuel} < 0$); EGT increases; AFR deviates.
- **Affected Subsystem**: Combustion & Fuel.
- **3D Mesh Localization**: Fuel Injector Rail highlighted in RED.

### 3. Lubrication Failure
- **Primary Perturbations**: Oil pressure drops below normal operating range ($\Delta \text{OilP} < -0.8\text{ bar}$); oil temperature and mechanical vibration steadily rise.
- **Affected Subsystem**: Lubrication & Mechanical.
- **3D Mesh Localization**: Oil Reservoir Sump highlighted in RED.

### 4. Thermal Overheating
- **Primary Perturbations**: CHT and EGT exceed critical limits ($>190^\circ\text{C}$ and $>780^\circ\text{C}$).
- **Affected Subsystem**: Thermal.
- **3D Mesh Localization**: Cylinder Heads and Exhaust Manifold highlighted in AMBER/RED.

### 5. Sensor Drift
- **Primary Perturbations**: Single sensor output diverges smoothly while surrounding physical parameters remain normal.
- **Affected Subsystem**: Sensor Integrity.
- **3D Mesh Localization**: Target 3D Sensor Marker highlighted in RED.
