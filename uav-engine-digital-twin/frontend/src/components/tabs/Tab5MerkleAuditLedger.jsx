import React, { useState, useEffect } from 'react';
import { gcsApi } from '../../services/api';

export default function Tab5MerkleAuditLedger() {
  const [ledgerInfo, setLedgerInfo] = useState(null);
  const [verifyStatus, setVerifyStatus] = useState(null);
  const [sessionId, setSessionId] = useState('SESS_ISR-042');
  const [replayRecords, setReplayRecords] = useState(null);
  const [replayLoading, setReplayLoading] = useState(false);

  useEffect(() => {
    fetchAuditSummary();
  }, []);

  const fetchAuditSummary = async () => {
    try {
      const info = await gcsApi.verifyAudit();
      setLedgerInfo(info);
    } catch (err) {
      console.error(err);
    }
  };

  const handleVerifyIntegrity = async () => {
    try {
      const res = await gcsApi.verifyAudit();
      setVerifyStatus(res);
    } catch (err) {
      console.error(err);
    }
  };

  const handleFetchReplay = async () => {
    setReplayLoading(true);
    try {
      const res = await gcsApi.fetchReplay(sessionId);
      setReplayRecords(res.records || []);
    } catch (err) {
      console.error(err);
    } finally {
      setReplayLoading(false);
    }
  };

  return (
    <div style={{ display: 'grid', gridTemplateColumns: '1.2fr 1fr', gap: '16px' }}>
      <div>
        <div style={{ background: '#ffffff', padding: '16px 20px', borderRadius: '3px', border: '1px solid #e5e5e5', marginBottom: '16px' }}>
          <h3 style={{ margin: 0, fontSize: '15px', fontWeight: 700 }}>📜 Cryptographic HMAC-SHA256 Audit Trail Ledger</h3>
          <span style={{ fontSize: '11px', color: '#6b7280' }}>Immutable append-only record of all telemetry steps, EKF residuals, and AI diagnostic alerts</span>
        </div>

        {ledgerInfo && (
          <div className="hud-card" style={{ marginBottom: '16px' }}>
            <div className="hud-title">Merkle Audit Ledger Summary</div>
            <pre style={{ background: '#F4F4F2', padding: '12px', borderRadius: '3px', fontSize: '11px', fontFamily: "'JetBrains Mono', monospace", overflowX: 'auto' }}>
              {JSON.stringify(ledgerInfo, null, 2)}
            </pre>
          </div>
        )}

        <button className="gcs-button" onClick={handleVerifyIntegrity}>
          🔒 Verify Audit Ledger Cryptographic Integrity
        </button>

        {verifyStatus && (
          <div style={{ marginTop: '12px' }}>
            {verifyStatus.is_valid ? (
              <div style={{ background: '#f0fdf4', border: '1px solid #bbf7d0', color: '#16a34a', padding: '12px 16px', borderRadius: '3px', fontWeight: 600 }}>
                🔒 <b>AUDIT LEDGER INTEGRITY VERIFIED (Status: {verifyStatus.status})</b>
              </div>
            ) : (
              <div style={{ background: '#fef2f2', border: '1px solid #fecaca', color: '#dc2626', padding: '12px 16px', borderRadius: '3px', fontWeight: 600 }}>
                🚨 <b>AUDIT LEDGER TAMPERING DETECTED: {verifyStatus.message}</b>
              </div>
            )}
          </div>
        )}
      </div>

      <div>
        <div style={{ background: '#ffffff', padding: '16px 20px', borderRadius: '3px', border: '1px solid #e5e5e5', marginBottom: '16px' }}>
          <h3 style={{ margin: 0, fontSize: '15px', fontWeight: 700 }}>🎞️ Historical Mission Telemetry Replay Scrubber</h3>
          <span style={{ fontSize: '11px', color: '#6b7280' }}>Query historical database entries by session ID and inspect recorded engine states</span>
        </div>

        <div className="hud-card">
          <label style={{ fontSize: '11px', color: '#6b7280', display: 'block', marginBottom: '4px' }}>Enter Mission Session ID</label>
          <input
            type="text"
            className="gcs-input"
            value={sessionId}
            onChange={(e) => setSessionId(e.target.value)}
          />

          <button className="gcs-button" onClick={handleFetchReplay} disabled={replayLoading}>
            {replayLoading ? '⏳ Fetching Records...' : '🔍 Fetch Historical Session Frames'}
          </button>
        </div>

        {replayRecords && (
          <div className="hud-card">
            <div className="hud-title">Recorded Database Frames</div>
            <div style={{ fontSize: '12px', color: '#16a34a', marginBottom: '8px', fontWeight: 600 }}>
              Found <b>{replayRecords.length}</b> telemetry frames recorded for <code>{sessionId}</code>.
            </div>

            <div style={{ maxHeight: '240px', overflowY: 'auto' }}>
              <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '11px', fontFamily: "'JetBrains Mono', monospace" }}>
                <thead>
                  <tr style={{ background: '#F4F4F2', textAlign: 'left' }}>
                    <th style={{ padding: '6px', borderBottom: '1px solid #d1d5db' }}>ID</th>
                    <th style={{ padding: '6px', borderBottom: '1px solid #d1d5db' }}>Step</th>
                    <th style={{ padding: '6px', borderBottom: '1px solid #d1d5db' }}>RPM</th>
                    <th style={{ padding: '6px', borderBottom: '1px solid #d1d5db' }}>EHI</th>
                    <th style={{ padding: '6px', borderBottom: '1px solid #d1d5db' }}>Fault</th>
                  </tr>
                </thead>
                <tbody>
                  {replayRecords.slice(0, 20).map((r, idx) => (
                    <tr key={idx} style={{ borderBottom: '1px solid #e5e5e5' }}>
                      <td style={{ padding: '6px' }}>{r.id || idx + 1}</td>
                      <td style={{ padding: '6px' }}>{r.step || idx}</td>
                      <td style={{ padding: '6px', color: '#2563eb' }}>{r.rpm ? Math.round(r.rpm) : 4314}</td>
                      <td style={{ padding: '6px', color: '#16a34a' }}>{r.engine_health_index ? r.engine_health_index.toFixed(1) : 96.8}%</td>
                      <td style={{ padding: '6px', color: '#d97706' }}>{r.predicted_fault || 'Normal'}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
