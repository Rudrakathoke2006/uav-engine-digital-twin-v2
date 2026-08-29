import React from 'react';
import './styles/app.css';

export default function App() {
  return (
    <div className="gcs-container">
      <div className="gcs-sidebar">
        <h2>🛸 AeroTwin-PX</h2>
        <p style={{ fontSize: '12px', color: '#94a3b8' }}>DRDO / iDEX PS 26054</p>
        <hr style={{ borderColor: '#334155' }} />
        <ul style={{ listStyle: 'none', padding: 0 }}>
          <li style={{ padding: '8px 0', color: '#38bdf8', fontWeight: 'bold' }}>🛸 3D Digital Twin</li>
          <li style={{ padding: '8px 0', color: '#94a3b8' }}>📊 Live Monitoring</li>
          <li style={{ padding: '8px 0', color: '#94a3b8' }}>🧠 AI Diagnostics</li>
          <li style={{ padding: '8px 0', color: '#94a3b8' }}>⏳ RUL Degradation</li>
          <li style={{ padding: '8px 0', color: '#94a3b8' }}>🎯 Mission Simulator</li>
          <li style={{ padding: '8px 0', color: '#94a3b8' }}>🎞️ Mission Replay</li>
        </ul>
      </div>
      <div className="gcs-main">
        <h1>✈️ MALE-UAV Aero-Piston Engine Digital Twin GCS</h1>
        <div className="gcs-card">
          <h3>System Status: Operational</h3>
          <p>Local Server running with integrated 3D WebGL WebGL Digital Twin visualization at <a href="http://localhost:8501" style={{ color: '#38bdf8' }}>http://localhost:8501</a></p>
        </div>
      </div>
    </div>
  );
}
