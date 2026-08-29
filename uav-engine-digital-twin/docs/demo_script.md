# SIH / iDEX Final Presentation Demo Script

## 3-Minute Live Demonstration Flow

```text
[0:00 - 0:30]  INTRO & PROBLEM STATEMENT
               Open GCS Dashboard at http://localhost:8501. Explain DRDO/iDEX PS 26054: Small aero-piston engines on MALE UAVs lack real-time digital twins.

[0:30 - 1:15]  TAB 0: 3D DIGITAL TWIN & LIVE VISUALIZATION
               Demonstrate Three.js 3D WebGL twin. Click camera buttons ([UAV VIEW], [ENGINE VIEW], [CUTAWAY], [DIAGNOSTIC VIEW]).
               Hover over 3D Raycaster sensor spheres showing Actual vs. MVEM Expected vs. Residual (ΔS) values.

[1:15 - 2:00]  SYNTHETIC FAULT INJECTION & AI DIAGNOSTICS
               Select "Cylinder Misfire" or "Injector Coking" in sidebar.
               Show affected 3D engine mesh highlight in red/amber.
               Navigate to Tab 2: Show Anomaly Score, XGBoost Fault Alert, and SHAP XAI Feature Importance plots.

[2:00 - 2:30]  RUL & WHAT-IF MISSION SIMULATOR
               Tab 3: Show rolling degradation trajectory with 80% CI prediction bounds.
               Tab 4: Run 500-iteration Monte Carlo environmental simulator under 18,000 ft altitude & 42°C ambient heat. Show Mission Success Probability (%).

[2:30 - 3:00]  MISSION REPLAY & CRYPTOGRAPHIC AUDIT LOG
               Tab 5: Scrub historical mission timeline.
               Demonstrate HMAC-SHA256 Merkle chain audit log verification and data tampering detection test button.
```
