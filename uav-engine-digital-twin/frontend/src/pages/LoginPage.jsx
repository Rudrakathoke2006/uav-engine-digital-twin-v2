import React from "react";

export default function LoginPage() {
  return (
    <div className="gcs-card" style={{ maxWidth: '400px', margin: '100px auto', padding: '30px' }}>
      <h2>🛸 AeroTwin-PX GCS Login</h2>
      <p style={{ color: '#94a3b8' }}>DRDO / iDEX PS 26054 Operator Access</p>
      <form onSubmit={(e) => { e.preventDefault(); window.location.href = "/dashboard"; }}>
        <div style={{ marginBottom: '15px' }}>
          <label>Operator ID:</label>
          <input type="text" defaultValue="OP-SIH-2026" style={{ width: '100%', padding: '8px', marginTop: '5px', background: '#0f172a', color: '#fff', border: '1px solid #334155' }} />
        </div>
        <div style={{ marginBottom: '20px' }}>
          <label>Password:</label>
          <input type="password" defaultValue="••••••••" style={{ width: '100%', padding: '8px', marginTop: '5px', background: '#0f172a', color: '#fff', border: '1px solid #334155' }} />
        </div>
        <button type="submit" style={{ width: '100%', padding: '10px', background: '#38bdf8', color: '#000', fontWeight: 'bold', border: 'none', cursor: 'pointer' }}>LOGIN TO GCS</button>
      </form>
    </div>
  );
}
