import React from 'react';

export default function AvionicsSidebar({
  profile,
  setProfile,
  faultChoice,
  setFaultChoice,
  faultSeverity,
  setFaultSeverity,
  autoStream,
  setAutoStream,
  onStep,
  onReset
}) {
  return (
    <div className="app-sidebar">
      <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '16px' }}>
        <img src="https://img.icons8.com/color/96/drone.png" width="48" alt="Drone Logo" />
        <div>
          <div style={{ fontSize: '13px', letterSpacing: '1.2px', fontWeight: 700, color: '#1a1a1a', textTransform: 'uppercase' }}>AERO-AVIONICS GCS</div>
          <div style={{ fontSize: '10px', color: '#9ca3af', letterSpacing: '0.8px', textTransform: 'uppercase' }}>DRDO / SIH PS 26054 Defense Suite</div>
        </div>
      </div>

      <hr style={{ border: 'none', borderTop: '1px solid #e5e5e5', margin: '12px 0 16px 0' }} />

      <div style={{ fontSize: '12px', fontWeight: 700, color: '#1a1a1a', marginBottom: '6px' }}>🕹️ Mission Flight Profile</div>
      <label style={{ fontSize: '11px', color: '#6b7280', display: 'block', marginBottom: '4px' }}>Operating Envelope</label>
      <select
        className="gcs-select"
        value={profile}
        onChange={(e) => setProfile(e.target.value)}
      >
        <option value="Normal Cruise">Normal Cruise</option>
        <option value="High Altitude (18,000 ft)">High Altitude (18,000 ft)</option>
        <option value="Hot Weather (42°C)">Hot Weather (42°C)</option>
        <option value="Rapid Throttle">Rapid Throttle</option>
        <option value="Long Endurance">Long Endurance</option>
      </select>

      <div style={{ fontSize: '12px', fontWeight: 700, color: '#1a1a1a', marginBottom: '6px' }}>⚠️ Fault Injector (Demonstration)</div>
      <label style={{ fontSize: '11px', color: '#6b7280', display: 'block', marginBottom: '4px' }}>Inject Synthetic Fault</label>
      <select
        className="gcs-select"
        value={faultChoice}
        onChange={(e) => {
          const val = e.target.value;
          setFaultChoice(val);
          if (val === 'None / Healthy') setFaultSeverity(0.0);
          else if (faultSeverity === 0) setFaultSeverity(0.7);
        }}
      >
        <option value="None / Healthy">None / Healthy</option>
        <option value="Cylinder Misfire">Cylinder Misfire</option>
        <option value="Injector Coking">Injector Coking</option>
        <option value="Lubrication Failure">Lubrication Failure</option>
        <option value="Sensor Drift">Sensor Drift</option>
        <option value="Combustion Instability">Combustion Instability</option>
        <option value="Thermal Overheating">Thermal Overheating</option>
        <option value="Abnormal Vibration">Abnormal Vibration</option>
      </select>

      <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '11px', color: '#6b7280', marginBottom: '4px' }}>
        <span>Fault Severity</span>
        <span style={{ fontWeight: 600, color: '#2563eb' }}>{faultSeverity.toFixed(1)}</span>
      </div>
      <input
        type="range"
        min="0.0"
        max="1.0"
        step="0.1"
        className="gcs-slider"
        value={faultSeverity}
        onChange={(e) => setFaultSeverity(parseFloat(e.target.value))}
      />

      <hr style={{ border: 'none', borderTop: '1px solid #e5e5e5', margin: '12px 0 16px 0' }} />

      <label style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '12px', color: '#1a1a1a', cursor: 'pointer', marginBottom: '14px' }}>
        <input
          type="checkbox"
          checked={autoStream}
          onChange={(e) => setAutoStream(e.target.checked)}
        />
        <span>Auto-Stream Telemetry (10 Hz)</span>
      </label>

      <button className="gcs-button" onClick={onStep}>
        Step Telemetry (+1 Tick)
      </button>

      <button
        className="gcs-button"
        style={{ borderColor: '#dc2626', color: '#dc2626', marginTop: '4px' }}
        onClick={onReset}
      >
        Reset Telemetry & Audit Log
      </button>
    </div>
  );
}
