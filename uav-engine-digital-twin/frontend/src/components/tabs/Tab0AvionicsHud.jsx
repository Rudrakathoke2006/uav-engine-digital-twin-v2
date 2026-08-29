import React from 'react';

export default function Tab0AvionicsHud({ state }) {
  if (!state) return null;

  const frame = state.frame || {};
  const subsystems = state.subsystem_health?.subsystems || {};
  const sensorScores = state.sensor_health?.sensor_scores || {};
  const twinConf = state.sensor_health?.digital_twin_confidence || 96.5;

  const getHealthColor = (v) => {
    if (v >= 85) return '#16a34a';
    if (v >= 70) return '#2563eb';
    if (v >= 50) return '#d97706';
    return '#dc2626';
  };

  const subsystemDefs = [
    { label: 'COMBUSTION', val: subsystems.combustion_health ?? 92.2, icon: '🔥', desc: 'EGT + Fuel Flow' },
    { label: 'THERMAL', val: subsystems.thermal_health ?? 96.6, icon: '🌡️', desc: 'CHT + EGT Residuals' },
    { label: 'LUBRICATION', val: subsystems.lubrication_health ?? 98.0, icon: '🛢️', desc: 'Oil Pressure + Temp' },
    { label: 'MECHANICAL', val: subsystems.mechanical_health ?? 99.7, icon: '⚙️', desc: 'Vibration + CHT' },
    { label: 'ELECTRICAL', val: subsystems.electrical_health ?? 100.0, icon: '⚡', desc: 'Battery Voltage' },
  ];

  const sensorDefs = [
    { label: 'EGT SENSOR', val: sensorScores.egt_sensor ?? 98.5, unit: '°C' },
    { label: 'CHT SENSOR', val: sensorScores.cht_sensor ?? 96.6, unit: '°C' },
    { label: 'OIL PRESS', val: sensorScores.oil_p_sensor ?? 97.9, unit: 'bar' },
    { label: 'OIL TEMP', val: sensorScores.oil_t_sensor ?? 98.0, unit: '°C' },
    { label: 'FUEL FLOW', val: sensorScores.fuel_sensor ?? 87.1, unit: 'L/h' },
    { label: 'VIBRATION', val: sensorScores.vibration_sensor ?? 96.0, unit: 'RMS' },
    { label: 'TWIN CONF.', val: twinConf, unit: '%' },
  ];

  return (
    <div>
      <div style={{ background: '#ffffff', padding: '22px', borderRadius: '3px', border: '1px solid #e5e5e5', marginBottom: '20px' }}>
        <h3 style={{ fontFamily: "'Inter', sans-serif", color: '#1a1a1a', marginTop: 0, fontSize: '16px', fontWeight: 700, letterSpacing: '0.5px' }}>
          🛩️ PRIMARY FLIGHT DISPLAY (PFD) & TACTICAL RADAR HUD
        </h3>
        <p style={{ color: '#6b7280', fontSize: '13px', marginBottom: 0 }}>
          Real-Time Aircraft Flight Attitude, Radar Target Scanning, and Engine Dial Telemetry
        </p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1.2fr', gap: '16px', marginBottom: '20px' }}>
        {/* Column 1: PFD Artificial Horizon */}
        <div className="hud-card">
          <div className="hud-title">PRIMARY FLIGHT DISPLAY (PFD) ARTIFICIAL HORIZON</div>
          <div style={{ textAlign: 'center', padding: '15px 0' }}>
            <svg width="220" height="180" viewBox="0 0 220 180">
              <circle cx="110" cy="90" r="80" fill="#f0f0ef" stroke="#2563eb" strokeWidth="1.5" />
              <clipPath id="horizonClip">
                <circle cx="110" cy="90" r="78" />
              </clipPath>
              <g clipPath="url(#horizonClip)">
                <rect x="10" y="10" width="200" height="80" fill="#93c5fd" opacity="0.5" />
                <rect x="10" y="90" width="200" height="80" fill="#a16207" opacity="0.35" />
                <line x1="20" y1="90" x2="200" y2="90" stroke="#1a1a1a" strokeWidth="2" />
                <path d="M 90 90 L 110 80 L 130 90 L 110 100 Z" fill="#d97706" stroke="#1a1a1a" strokeWidth="1.5" />
              </g>
              <line x1="85" y1="70" x2="135" y2="70" stroke="#1a1a1a" strokeWidth="1" />
              <line x1="85" y1="110" x2="135" y2="110" stroke="#1a1a1a" strokeWidth="1" />
              <text x="110" y="172" textAnchor="middle" fill="#2563eb" fontFamily="Inter" fontSize="11">PITCH: 3.2° | ROLL: 1.5°</text>
            </svg>
          </div>
        </div>

        {/* Column 2: Tactical Radar Scanner */}
        <div className="hud-card">
          <div className="hud-title">TACTICAL RADAR TARGET SCANNER</div>
          <div style={{ textAlign: 'center', padding: '15px 0' }}>
            <svg width="220" height="180" viewBox="0 0 220 180">
              <circle cx="110" cy="90" r="75" fill="#f0f0ef" stroke="#16a34a" strokeWidth="1.5" />
              <circle cx="110" cy="90" r="50" fill="none" stroke="#16a34a" strokeWidth="1" strokeDasharray="3" />
              <circle cx="110" cy="90" r="25" fill="none" stroke="#16a34a" strokeWidth="1" strokeDasharray="3" />
              <line x1="110" y1="15" x2="110" y2="165" stroke="#16a34a" strokeWidth="1" opacity="0.3" />
              <line x1="35" y1="90" x2="185" y2="90" stroke="#16a34a" strokeWidth="1" opacity="0.3" />
              <polygon points="110,90 170,40 180,70" fill="url(#radarSweep)" />
              <defs>
                <linearGradient id="radarSweep" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#16a34a" stopOpacity="0.4"/>
                  <stop offset="100%" stopColor="#16a34a" stopOpacity="0.0"/>
                </linearGradient>
              </defs>
              <circle cx="140" cy="65" r="5" fill="#dc2626" />
              <circle cx="140" cy="65" r="10" fill="none" stroke="#dc2626" strokeWidth="1.5">
                <animate attributeName="r" values="5;12;5" dur="1.5s" repeatCount="indefinite" />
              </circle>
              <text x="110" y="172" textAnchor="middle" fill="#16a34a" fontFamily="Inter" fontSize="11">TARGET: TAPAS-042 [ACTIVE]</text>
            </svg>
          </div>
        </div>

        {/* Column 3: Engine Dial Gauges */}
        <div className="hud-card">
          <div className="hud-title">ENGINE DIAL GAUGES TELEMETRY</div>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px', padding: '10px 0' }}>
            <div style={{ textAlign: 'center', background: '#FAFAF9', padding: '10px', borderRadius: '3px', border: '1px solid #e5e5e5' }}>
              <div style={{ fontSize: '10px', fontWeight: 600, color: '#6b7280', letterSpacing: '0.8px', textTransform: 'uppercase' }}>RPM VELOCITY</div>
              <div style={{ fontSize: '20px', fontWeight: 700, color: '#2563eb' }}>{frame.rpm ? Math.round(frame.rpm) : 4800}</div>
              <div style={{ fontSize: '10px', color: '#9ca3af' }}>Target: 4,800</div>
            </div>
            <div style={{ textAlign: 'center', background: '#FAFAF9', padding: '10px', borderRadius: '3px', border: '1px solid #e5e5e5' }}>
              <div style={{ fontSize: '10px', fontWeight: 600, color: '#6b7280', letterSpacing: '0.8px', textTransform: 'uppercase' }}>CYLINDER HEAD (CHT)</div>
              <div style={{ fontSize: '20px', fontWeight: 700, color: '#d97706' }}>{frame.cht_c ? frame.cht_c.toFixed(1) : 171.3} °C</div>
              <div style={{ fontSize: '10px', color: '#9ca3af' }}>Max Limit: 135°C</div>
            </div>
            <div style={{ textAlign: 'center', background: '#FAFAF9', padding: '10px', borderRadius: '3px', border: '1px solid #e5e5e5' }}>
              <div style={{ fontSize: '10px', fontWeight: 600, color: '#6b7280', letterSpacing: '0.8px', textTransform: 'uppercase' }}>EXHAUST GAS (EGT)</div>
              <div style={{ fontSize: '20px', fontWeight: 700, color: '#dc2626' }}>{frame.egt_c ? frame.egt_c.toFixed(1) : 695.2} °C</div>
              <div style={{ fontSize: '10px', color: '#9ca3af' }}>Max Limit: 880°C</div>
            </div>
            <div style={{ textAlign: 'center', background: '#FAFAF9', padding: '10px', borderRadius: '3px', border: '1px solid #e5e5e5' }}>
              <div style={{ fontSize: '10px', fontWeight: 600, color: '#6b7280', letterSpacing: '0.8px', textTransform: 'uppercase' }}>OIL PRESSURE</div>
              <div style={{ fontSize: '20px', fontWeight: 700, color: '#16a34a' }}>{frame.oil_pressure_bar ? frame.oil_pressure_bar.toFixed(1) : 4.3} bar</div>
              <div style={{ fontSize: '10px', color: '#9ca3af' }}>Nominal: 3-5 bar</div>
            </div>
          </div>
        </div>
      </div>

      <hr style={{ border: 'none', borderTop: '1px solid #e5e5e5', margin: '20px 0' }} />

      {/* Subsystem Health Panel */}
      <span className="section-eyebrow">LIVE ENGINE SUBSYSTEM HEALTH MONITOR</span>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(5, 1fr)', gap: '12px', marginBottom: '20px' }}>
        {subsystemDefs.map((sub, idx) => {
          const color = getHealthColor(sub.val);
          return (
            <div key={idx} className="hud-card">
              <div className="hud-title">{sub.icon} {sub.label}</div>
              <div className="hud-value" style={{ color, fontSize: '22px' }}>{sub.val.toFixed(1)}%</div>
              <div className="hud-sub">{sub.desc}</div>
              <div style={{ width: '100%', background: '#e5e5e5', height: '4px', marginTop: '6px' }}>
                <div style={{ width: `${sub.val}%`, background: color, height: '4px', transition: 'width 0.4s ease' }}></div>
              </div>
            </div>
          );
        })}
      </div>

      <hr style={{ border: 'none', borderTop: '1px solid #e5e5e5', margin: '20px 0' }} />

      {/* Sensor Integrity Grid */}
      <span className="section-eyebrow">SENSOR INTEGRITY & DIGITAL TWIN CONFIDENCE</span>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(7, 1fr)', gap: '10px' }}>
        {sensorDefs.map((sen, idx) => {
          const color = getHealthColor(sen.val);
          const status = sen.val >= 70 ? '✅ OK' : (sen.val >= 40 ? '⚠️ WARN' : '🚨 FAULT');
          return (
            <div key={idx} className="hud-card" style={{ padding: '12px 14px' }}>
              <div className="hud-title">{sen.label}</div>
              <div className="hud-value" style={{ color, fontSize: '18px' }}>{sen.val.toFixed(1)}%</div>
              <div className="hud-sub">{status}</div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
