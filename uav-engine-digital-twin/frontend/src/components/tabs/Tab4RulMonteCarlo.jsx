import React, { useState } from 'react';
import { BarChart, Bar, LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts';
import { gcsApi } from '../../services/api';

export default function Tab4RulMonteCarlo({ state }) {
  const [simDuration, setSimDuration] = useState(180);
  const [simLoading, setSimLoading] = useState(false);
  const [simResult, setSimResult] = useState(null);

  const ehi = state?.subsystem_health?.engine_health_index ?? 96.8;
  const rulHrs = state?.ai_res?.rul_hours ?? 319.3;

  const handleRunSim = async () => {
    setSimLoading(true);
    try {
      const res = await gcsApi.runMonteCarlo(simDuration);
      setSimResult(res);
    } catch (err) {
      console.error(err);
    } finally {
      setSimLoading(false);
    }
  };

  // Generate RUL Curve Data
  const rulCurveData = [];
  const totalHours = Math.max(10, Math.round(rulHrs * 1.2));
  for (let i = 0; i <= 50; i++) {
    const hrs = (i / 50) * totalHours;
    const health = Math.max(0, ehi * Math.exp(-0.002 * hrs));
    rulCurveData.push({ hours: Math.round(hrs), health: parseFloat(health.toFixed(1)) });
  }

  // Generate Histogram Data from simulation result
  const histogramData = [];
  if (simResult && simResult.end_health_distribution) {
    const dist = simResult.end_health_distribution;
    const bins = 20;
    const minVal = Math.min(...dist);
    const maxVal = Math.max(...dist);
    const step = (maxVal - minVal) / bins || 1;

    for (let b = 0; b < bins; b++) {
      const binStart = minVal + b * step;
      const binEnd = binStart + step;
      const count = dist.filter((v) => v >= binStart && v < binEnd).length;
      histogramData.push({ range: `${Math.round(binStart)}-${Math.round(binEnd)}%`, count });
    }
  }

  return (
    <div style={{ display: 'grid', gridTemplateColumns: '1.1fr 1fr', gap: '16px' }}>
      <div>
        <div style={{ background: '#ffffff', padding: '16px 20px', borderRadius: '3px', border: '1px solid #e5e5e5', marginBottom: '16px' }}>
          <h3 style={{ margin: 0, fontSize: '15px', fontWeight: 700 }}>🎯 500-Run Monte Carlo Mission Reliability Simulator</h3>
        </div>

        <div className="hud-card">
          <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', color: '#6b7280', marginBottom: '6px' }}>
            <span>Target Mission Duration (Minutes)</span>
            <span style={{ fontWeight: 700, color: '#2563eb' }}>{simDuration} min</span>
          </div>
          <input
            type="range"
            min="30"
            max="360"
            step="10"
            className="gcs-slider"
            value={simDuration}
            onChange={(e) => setSimDuration(parseInt(e.target.value))}
          />

          <button className="gcs-button" onClick={handleRunSim} disabled={simLoading}>
            {simLoading ? '⏳ Simulating 500 Stochastic Runs...' : '🚀 Execute 500-Run Monte Carlo Simulation'}
          </button>
        </div>

        {simResult && (
          <div>
            <div style={{ background: '#f0fdf4', border: '1px solid #bbf7d0', color: '#16a34a', padding: '14px', borderRadius: '3px', marginBottom: '14px', fontWeight: 600 }}>
              ✅ Simulation Complete! <b>Mission Success Probability: {simResult.success_probability_pct}%</b>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px', marginBottom: '14px' }}>
              <div className="hud-card" style={{ padding: '12px' }}>
                <div className="hud-title">Predicted End Health</div>
                <div style={{ fontSize: '20px', fontWeight: 700, color: '#2563eb' }}>{simResult.predicted_end_health_pct}%</div>
              </div>
              <div className="hud-card" style={{ padding: '12px' }}>
                <div className="hud-title">Thermal Degradation Rate</div>
                <div style={{ fontSize: '20px', fontWeight: 700, color: '#d97706' }}>{simResult.degradation_rate_per_hr} %/hr</div>
              </div>
            </div>

            {histogramData.length > 0 && (
              <div className="hud-card" style={{ height: '220px' }}>
                <div className="hud-title">500-Run End-of-Mission Engine Health Distribution</div>
                <ResponsiveContainer width="100%" height="80%">
                  <BarChart data={histogramData}>
                    <XAxis dataKey="range" tick={{ fontSize: 10 }} />
                    <YAxis tick={{ fontSize: 10 }} />
                    <Tooltip />
                    <Bar dataKey="count" fill="#16a34a" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            )}
          </div>
        )}
      </div>

      <div>
        <div style={{ background: '#ffffff', padding: '16px 20px', borderRadius: '3px', border: '1px solid #e5e5e5', marginBottom: '16px' }}>
          <h3 style={{ margin: 0, fontSize: '15px', fontWeight: 700 }}>📉 Rolling Engine RUL Degradation Forecast Curve</h3>
          <span style={{ fontSize: '11px', color: '#6b7280' }}>Exponential RUL Degradation Trajectory</span>
        </div>

        <div className="hud-card" style={{ height: '340px' }}>
          <ResponsiveContainer width="100%" height="90%">
            <LineChart data={rulCurveData}>
              <XAxis dataKey="hours" label={{ value: 'Operating Hours', position: 'insideBottom', offset: -5 }} />
              <YAxis domain={[0, 100]} label={{ value: 'Engine Health (%)', angle: -90, position: 'insideLeft' }} />
              <Tooltip />
              <ReferenceLine y={70} stroke="orange" strokeDasharray="3 3" label={{ value: 'Maintenance Limit (70%)', fill: 'orange', fontSize: 10 }} />
              <ReferenceLine y={40} stroke="red" strokeDasharray="3 3" label={{ value: 'Critical Limit (40%)', fill: 'red', fontSize: 10 }} />
              <Line type="monotone" dataKey="health" stroke="#2563eb" strokeWidth={2} dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
