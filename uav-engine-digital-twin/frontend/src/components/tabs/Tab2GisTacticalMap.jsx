import React, { useEffect, useRef } from 'react';

export default function Tab2GisTacticalMap({ state }) {
  const canvasRef = useRef(null);
  const step = state?.step || 20;

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;

    ctx.clearRect(0, 0, width, height);

    // Draw Map Grid
    ctx.strokeStyle = '#e5e5e5';
    ctx.lineWidth = 1;
    for (let x = 0; x < width; x += 40) {
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x, height);
      ctx.stroke();
    }
    for (let y = 0; y < height; y += 40) {
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(width, y);
      ctx.stroke();
    }

    // Generate trajectory points
    const points = [];
    const numPoints = Math.max(20, Math.min(step, 200));
    for (let i = 0; i < numPoints; i++) {
      const t = (i / 50) * Math.PI * 2;
      const px = width / 2 + Math.sin(t) * 140;
      const py = height / 2 + Math.cos(t * 0.8) * 100;
      points.push({ x: px, y: py });
    }

    // Draw Flight Path Line
    ctx.strokeStyle = '#16a34a';
    ctx.lineWidth = 3;
    ctx.beginPath();
    points.forEach((p, idx) => {
      if (idx === 0) ctx.moveTo(p.x, p.y);
      else ctx.lineTo(p.x, p.y);
    });
    ctx.stroke();

    // Draw Flight Path Waypoint Markers
    points.forEach((p) => {
      ctx.fillStyle = '#2563eb';
      ctx.beginPath();
      ctx.arc(p.x, p.y, 3, 0, Math.PI * 2);
      ctx.fill();
    });

    // Draw Active Drone Marker
    const lastPoint = points[points.length - 1];
    ctx.fillStyle = '#dc2626';
    ctx.beginPath();
    ctx.arc(lastPoint.x, lastPoint.y, 8, 0, Math.PI * 2);
    ctx.fill();

    ctx.strokeStyle = '#dc2626';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.arc(lastPoint.x, lastPoint.y, 16, 0, Math.PI * 2);
    ctx.stroke();

    ctx.fillStyle = '#1a1a1a';
    ctx.font = 'bold 11px Inter';
    ctx.fillText('✈️ MALE UAV DRONE (ACTIVE)', lastPoint.x - 70, lastPoint.y - 20);
  }, [step]);

  return (
    <div>
      <div style={{ background: '#ffffff', padding: '16px 20px', borderRadius: '3px', border: '1px solid #e5e5e5', marginBottom: '16px' }}>
        <h3 style={{ margin: 0, fontSize: '15px', fontWeight: 700 }}>🗺️ Tactical GIS Flight Trajectory Map & Drone Telemetry</h3>
        <span style={{ fontSize: '11px', color: '#6b7280' }}>Real-Time GIS Drone Flight Path Tracker, Coordinates, Groundspeed, Altitude, and Geo-Fencing Boundary</span>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '16px' }}>
        <div style={{ background: '#FAFAF9', border: '1px solid #e5e5e5', borderRadius: '3px', padding: '12px', textAlign: 'center' }}>
          <canvas ref={canvasRef} width={640} height={400} style={{ width: '100%', height: '400px', display: 'block' }} />
        </div>

        <div className="hud-card">
          <div className="hud-title">✈️ Drone Flight Navigation HUD</div>
          <p style={{ fontSize: '13px', color: '#1a1a1a', marginBottom: '8px' }}><b>Callsign:</b> DRDO-TAPAS-042</p>
          <p style={{ fontSize: '13px', color: '#1a1a1a', marginBottom: '8px' }}><b>Latitude:</b> 28.6139° N</p>
          <p style={{ fontSize: '13px', color: '#1a1a1a', marginBottom: '8px' }}><b>Longitude:</b> 77.2090° E</p>
          <p style={{ fontSize: '13px', color: '#1a1a1a', marginBottom: '8px' }}><b>Altitude:</b> 18,000 ft (MSL)</p>
          <p style={{ fontSize: '13px', color: '#1a1a1a', marginBottom: '8px' }}><b>Groundspeed:</b> 142.5 knots</p>
          <p style={{ fontSize: '13px', color: '#1a1a1a', marginBottom: '8px' }}><b>Heading:</b> 045° (NE)</p>

          <hr style={{ border: 'none', borderTop: '1px solid #e5e5e5', margin: '12px 0' }} />

          <p style={{ fontSize: '13px', color: '#16a34a', fontWeight: 600, margin: 0 }}>
            <b>Geo-Fence Status:</b> INSIDE SAFE BOUNDS
          </p>
        </div>
      </div>
    </div>
  );
}
