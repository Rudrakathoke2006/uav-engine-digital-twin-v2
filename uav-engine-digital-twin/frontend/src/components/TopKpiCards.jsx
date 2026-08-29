import React from 'react';

export default function TopKpiCards({ state }) {
  if (!state) return null;

  const { subsystem_health, sensor_health, ai_res } = state;
  const ehi = subsystem_health?.engine_health_index ?? 98.0;
  const statusTxt = subsystem_health?.health_status ?? 'HEALTHY';
  const twinConf = sensor_health?.digital_twin_confidence ?? 96.5;
  const rulHrs = ai_res?.rul_hours ?? 320.0;
  const rulBounds = ai_res?.rul_interval_hours ?? [260.0, 380.0];
  const anomSc = ai_res?.anomaly_score ?? 0.15;
  const isAnomaly = ai_res?.is_anomaly ?? false;
  const predFault = ai_res?.predicted_fault ?? 'Normal Operation';
  const conf = ai_res?.fault_confidence_pct ?? 98.0;

  const cardClassAnom = isAnomaly ? "hud-card-critical" : "hud-card";
  const anomColor = isAnomaly ? "#dc2626" : "#16a34a";

  return (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(5, 1fr)', gap: '12px', marginBottom: '16px' }}>
      <div className="hud-card">
        <div className="hud-title">ENGINE EHI</div>
        <div className="hud-value" style={{ color: '#16a34a' }}>{ehi}%</div>
        <div className="hud-sub">{statusTxt}</div>
      </div>

      <div className="hud-card">
        <div className="hud-title">TWIN CONFIDENCE</div>
        <div className="hud-value" style={{ color: '#2563eb' }}>{twinConf}%</div>
        <div className="hud-sub">Sensor Integrity Score</div>
      </div>

      <div className="hud-card">
        <div className="hud-title">PREDICTED RUL</div>
        <div className="hud-value" style={{ color: '#2563eb' }}>{rulHrs} hrs</div>
        <div className="hud-sub">CI: {rulBounds[0]} - {rulBounds[1]} h</div>
      </div>

      <div className={cardClassAnom}>
        <div className="hud-title">ANOMALY SCORE</div>
        <div className="hud-value" style={{ color: anomColor }}>{anomSc}</div>
        <div className="hud-sub">{isAnomaly ? 'ALERT TRIGGERED' : 'Nominal Bounds'}</div>
      </div>

      <div className="hud-card">
        <div className="hud-title">DIAGNOSED FAULT</div>
        <div className="hud-value" style={{ color: '#d97706', fontSize: '17px' }}>{predFault}</div>
        <div className="hud-sub">Confidence: {conf.toFixed(1)}%</div>
      </div>
    </div>
  );
}
