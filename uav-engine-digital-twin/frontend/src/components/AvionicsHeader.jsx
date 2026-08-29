import React from 'react';

export default function AvionicsHeader({ profile, step }) {
  return (
    <div className="avionics-header">
      <div>
        <span className="hud-badge badge-cyan">DRDO / iDEX PS 26054</span>
        <span className="hud-badge badge-emerald">
          <span className="pulse-dot"></span>LIVE DOWNLINK
        </span>
        <span className="hud-badge badge-amber">ENVELOPE: {(profile || 'Normal Cruise').toUpperCase()}</span>
        <h2 style={{ fontFamily: "'Inter', sans-serif", fontSize: '18px', fontWeight: 700, color: '#1a1a1a', margin: '4px 0 0 0', letterSpacing: '0.5px' }}>
          AEROTWIN-PX v2 DEFENSE AVIONICS SUITE
        </h2>
      </div>
      <div style={{ textAlign: 'right' }}>
        <div style={{ fontFamily: "'Inter', sans-serif", fontSize: '15px', fontWeight: 700, color: '#2563eb' }}>
          MISSION STEP: #{String(step || 0).padStart(4, '0')}
        </div>
        <div style={{ fontSize: '12px', color: '#6b7280' }}>SAT-LINK: 99.8% | LATENCY: 18.4 ms</div>
      </div>
    </div>
  );
}
