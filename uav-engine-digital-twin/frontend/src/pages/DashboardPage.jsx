import React from 'react';

export default function DashboardPage() {
  return (
    <div className="gcs-dashboard" style={{ background: '#0b0f19', padding: '16px', color: '#e2e8f0' }}>
      {/* TOP BAR */}
      <div className="top-bar" style={{ display: 'flex', justifyContent: 'space-between', background: '#0f172a', padding: '12px 20px', borderRadius: '8px', border: '1px solid #334155', marginBottom: '16px' }}>
        <div><strong>Mission ID:</strong> ISR-2026-001 | <strong>Engine:</strong> Rotax 914 Turbo</div>
        <div><span className="status-healthy">🟢 CONNECTED (CAN-BUS 1000ms)</span></div>
        <div><strong>Mission Time:</strong> 01:42:15 | <button style={{ background: '#ef4444', color: '#fff', border: 'none', borderRadius: '4px', padding: '4px 12px' }}>STOP</button></div>
      </div>

      {/* ROW 1: CORE METRICS */}
      <div className="row-1" style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '16px', marginBottom: '16px' }}>
        <div className="gcs-card"><h4>Overall Engine Health</h4><h2 style={{ color: '#10b981' }}>96.8% (HEALTHY)</h2></div>
        <div className="gcs-card"><h4>Engine Operating State</h4><h2 style={{ color: '#38bdf8' }}>CRUISE (72% Throttle)</h2></div>
        <div className="gcs-card"><h4>Anomaly Score</h4><h2 style={{ color: '#10b981' }}>0.16 (NORMAL)</h2></div>
        <div className="gcs-card"><h4>Predicted RUL</h4><h2 style={{ color: '#38bdf8' }}>319.3 Hours (80% CI)</h2></div>
      </div>

      {/* ROW 2: LIVE TELEMETRY GAUGES */}
      <div className="row-2" style={{ display: 'grid', gridTemplateColumns: 'repeat(6, 1fr)', gap: '12px', marginBottom: '16px' }}>
        <div className="gcs-card"><div>RPM</div><h3>4314 RPM</h3></div>
        <div className="gcs-card"><div>CHT</div><h3>171.3 °C</h3></div>
        <div className="gcs-card"><div>EGT</div><h3>695.2 °C</h3></div>
        <div className="gcs-card"><div>Oil Pressure</div><h3>4.3 bar</h3></div>
        <div className="gcs-card"><div>Oil Temp</div><h3>96.0 °C</h3></div>
        <div className="gcs-card"><div>Vibration</div><h3>2.15 mm/s</h3></div>
      </div>

      {/* ROW 3 & RIGHT PANEL */}
      <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '16px' }}>
        <div>
          {/* ROW 3: SUBSYSTEM HEALTH BARS */}
          <div className="gcs-card" style={{ marginBottom: '16px' }}>
            <h3>Subsystem Health Breakdown</h3>
            <div style={{ margin: '8px 0' }}>Combustion: 98% ■■■■■■■■■□</div>
            <div style={{ margin: '8px 0' }}>Thermal: 94% ■■■■■■■■9□</div>
            <div style={{ margin: '8px 0' }}>Lubrication: 96% ■■■■■■■■9□</div>
            <div style={{ margin: '8px 0' }}>Mechanical: 97% ■■■■■■■■9□</div>
            <div style={{ margin: '8px 0' }}>Electrical: 99% ■■■■■■■■■■</div>
          </div>
          {/* ROW 4: TELEMETRY CHARTS */}
          <div className="gcs-card">
            <h3>Live Telemetry Trend Curves</h3>
            <p style={{ color: '#94a3b8' }}>Real-time 1000ms sync curves for RPM, EGT, CHT, and Oil Pressure.</p>
          </div>
        </div>

        {/* RIGHT / LOWER PANEL */}
        <div className="gcs-card">
          <h3>AI Predictive Diagnostics</h3>
          <hr style={{ borderColor: '#334155' }} />
          <p><strong>Probable Fault:</strong> Normal Operation</p>
          <p><strong>Confidence:</strong> 95.2%</p>
          <p><strong>Degradation Rate:</strong> 0.0% / Hour</p>
          <hr style={{ borderColor: '#334155' }} />
          <h4>Operator Maintenance Advisory</h4>
          <p style={{ color: '#10b981' }}>✅ Engine operating within nominal ISA thermodynamic parameters. No action required.</p>
        </div>
      </div>
    </div>
  );
}
