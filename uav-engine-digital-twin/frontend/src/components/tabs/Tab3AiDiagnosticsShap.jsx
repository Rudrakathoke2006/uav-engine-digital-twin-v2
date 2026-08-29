import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';

export default function Tab3AiDiagnosticsShap({ state }) {
  if (!state) return null;

  const aiRes = state.ai_res || {};
  const sensorHealth = state.sensor_health || {};

  const isAnomaly = aiRes.is_anomaly || false;
  const predFault = aiRes.predicted_fault || 'Normal Operation';
  const conf = aiRes.fault_confidence_pct || 98.0;
  const anomScore = aiRes.anomaly_score || 0.15;
  const suspectSensors = sensorHealth.suspect_sensors || [];

  const shapData = (aiRes.shap_top_contributors || []).map((item) => ({
    feature: item.feature,
    weight: item.shap_weight,
    val: item.val
  }));

  return (
    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
      <div>
        <div style={{ background: '#ffffff', padding: '16px 20px', borderRadius: '3px', border: '1px solid #e5e5e5', marginBottom: '16px' }}>
          <h3 style={{ margin: 0, fontSize: '15px', fontWeight: 700 }}>🔍 Intelligent Fault Diagnostic Alert</h3>
        </div>

        {isAnomaly || aiRes.fault_class_id !== 0 ? (
          <div style={{ background: '#fef2f2', border: '1px solid #fecaca', color: '#dc2626', padding: '14px 18px', borderRadius: '3px', marginBottom: '16px', fontWeight: 600 }}>
            🚨 <b>ALERT: {predFault}</b> (Confidence: {conf.toFixed(1)}%)
          </div>
        ) : (
          <div style={{ background: '#f0fdf4', border: '1px solid #bbf7d0', color: '#16a34a', padding: '14px 18px', borderRadius: '3px', marginBottom: '16px', fontWeight: 600 }}>
            ✅ <b>SYSTEM NOMINAL: Normal Engine Combustion State</b>
          </div>
        )}

        <div className="hud-card">
          <div className="hud-title">Anomaly Score</div>
          <div style={{ fontSize: '18px', fontWeight: 700, color: isAnomaly ? '#dc2626' : '#16a34a', marginBottom: '6px' }}>
            {anomScore} / 1.0 <span style={{ fontSize: '11px', color: '#6b7280', fontWeight: 400 }}>(Threshold: 0.45)</span>
          </div>
          <div style={{ width: '100%', background: '#e5e5e5', height: '6px' }}>
            <div style={{ width: `${Math.min(anomScore * 100, 100)}%`, background: isAnomaly ? '#dc2626' : '#16a34a', height: '6px', transition: 'width 0.4s ease' }} />
          </div>
        </div>

        <div className="hud-card">
          <div className="hud-title">📡 Sensor Integrity & Drift Status</div>
          {suspectSensors.length > 0 ? (
            <div style={{ color: '#d97706', fontSize: '13px', fontWeight: 600 }}>
              ⚠️ Suspect Sensors Flagged: {suspectSensors.join(', ')}
            </div>
          ) : (
            <div style={{ color: '#16a34a', fontSize: '13px', fontWeight: 600 }}>
              🟢 All 8 Engine Telemetry Sensors Validated (Zero Drift Detected)
            </div>
          )}
        </div>
      </div>

      <div>
        <div style={{ background: '#ffffff', padding: '16px 20px', borderRadius: '3px', border: '1px solid #e5e5e5', marginBottom: '16px' }}>
          <h3 style={{ margin: 0, fontSize: '15px', fontWeight: 700 }}>🧬 SHAP Explainable AI Feature Importance Weightings</h3>
          <span style={{ fontSize: '11px', color: '#6b7280' }}>Top Diagnostic Feature Attribution Weights</span>
        </div>

        <div className="hud-card" style={{ height: '300px' }}>
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={shapData} layout="vertical" margin={{ top: 10, right: 30, left: 80, bottom: 10 }}>
              <XAxis type="number" domain={[0, 'dataMax + 0.05']} />
              <YAxis type="category" dataKey="feature" tick={{ fontSize: 11 }} width={120} />
              <Tooltip />
              <Bar dataKey="weight" fill="#2563eb">
                {shapData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={index === 0 ? '#d97706' : '#2563eb'} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
