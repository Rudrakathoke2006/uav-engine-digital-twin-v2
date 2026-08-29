import React, { useState, useEffect, useRef } from 'react';
import * as THREE from 'three';

export default function Tab1DigitalTwin3D({ state }) {
  const mountRef = useRef(null);
  const [viewMode, setViewMode] = useState('uav');
  const twinState = state?.twin_state || {};

  const pitch = twinState.pitch_deg || 0.0;
  const roll = twinState.roll_deg || 0.0;
  const yaw = twinState.yaw_deg || 0.0;
  const lat = twinState.latitude || 28.6139;
  const lon = twinState.longitude || 77.2090;
  const alt = twinState.altitude_ft || 18000;
  const rpm = twinState.rpm || 4314;
  const rads = (rpm * 0.1047).toFixed(1);

  useEffect(() => {
    if (!mountRef.current) return;
    const width = mountRef.current.clientWidth;
    const height = 500;

    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0xf0f0ef);

    const camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000);
    camera.position.set(0, 5, 12);
    camera.lookAt(0, 0, 0);

    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(window.devicePixelRatio);
    mountRef.current.appendChild(renderer.domElement);

    // Lights
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.7);
    scene.add(ambientLight);

    const dirLight = new THREE.DirectionalLight(0x2563eb, 1.2);
    dirLight.position.set(10, 20, 10);
    scene.add(dirLight);

    // Drone Group
    const droneGroup = new THREE.Group();

    // Fuselage
    const fuseGeo = new THREE.CylinderGeometry(0.5, 0.4, 6, 16);
    fuseGeo.rotateX(Math.PI / 2);
    const fuseMat = new THREE.MeshPhongMaterial({ color: 0xd1d5db, flatShading: false });
    const fuselage = new THREE.Mesh(fuseGeo, fuseMat);
    droneGroup.add(fuselage);

    // Wings
    const wingGeo = new THREE.BoxGeometry(10, 0.1, 1.2);
    const wingMat = new THREE.MeshPhongMaterial({ color: 0x2563eb });
    const wings = new THREE.Mesh(wingGeo, wingMat);
    wings.position.set(0, 0.1, 0);
    droneGroup.add(wings);

    // Tail Wing
    const tailGeo = new THREE.BoxGeometry(3, 0.08, 0.6);
    const tailMat = new THREE.MeshPhongMaterial({ color: 0x1a1a1a });
    const tail = new THREE.Mesh(tailGeo, tailMat);
    tail.position.set(0, 0.2, -2.6);
    droneGroup.add(tail);

    // Vertical Fin
    const finGeo = new THREE.BoxGeometry(0.08, 1.2, 0.8);
    const fin = new THREE.Mesh(finGeo, tailMat);
    fin.position.set(0, 0.7, -2.6);
    droneGroup.add(fin);

    // Engine Block (Piston Engine)
    const engineGeo = new THREE.BoxGeometry(0.8, 0.8, 1.2);
    const engineMat = new THREE.MeshPhongMaterial({ color: 0xd97706 });
    const engine = new THREE.Mesh(engineGeo, engineMat);
    engine.position.set(0, 0.2, 2.5);
    droneGroup.add(engine);

    // Propeller
    const propGeo = new THREE.BoxGeometry(2.4, 0.1, 0.04);
    const propMat = new THREE.MeshPhongMaterial({ color: 0x16a34a });
    const prop = new THREE.Mesh(propGeo, propMat);
    prop.position.set(0, 0.2, 3.15);
    droneGroup.add(prop);

    // Grid Floor
    const grid = new THREE.GridHelper(20, 20, 0x2563eb, 0xd1d5db);
    grid.position.y = -2;
    scene.add(grid);

    scene.add(droneGroup);

    let animationFrameId;
    const animate = () => {
      animationFrameId = requestAnimationFrame(animate);
      prop.rotation.z += (rpm / 6000) * 0.4;

      droneGroup.rotation.x = THREE.MathUtils.degToRad(pitch);
      droneGroup.rotation.z = -THREE.MathUtils.degToRad(roll);
      droneGroup.rotation.y = THREE.MathUtils.degToRad(yaw);

      renderer.render(scene, camera);
    };

    animate();

    return () => {
      cancelAnimationFrame(animationFrameId);
      if (mountRef.current && renderer.domElement) {
        mountRef.current.removeChild(renderer.domElement);
      }
      renderer.dispose();
    };
  }, [rpm, pitch, roll, yaw]);

  return (
    <div>
      <div style={{ background: '#ffffff', padding: '16px 20px', borderRadius: '3px', border: '1px solid #e5e5e5', marginBottom: '16px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h3 style={{ margin: 0, fontSize: '15px', fontWeight: 700 }}>🛸 Interactive 3D MALE-UAV Drone & Engine Digital Twin</h3>
          <span style={{ fontSize: '11px', color: '#6b7280' }}>Live WebGL 3D virtual representation synchronized with telemetry</span>
        </div>

        <div style={{ display: 'flex', gap: '8px' }}>
          <button className={`gcs-button ${viewMode === 'uav' ? 'active' : ''}`} style={{ width: 'auto', margin: 0 }} onClick={() => setViewMode('uav')}>✈️ UAV View</button>
          <button className={`gcs-button ${viewMode === 'engine' ? 'active' : ''}`} style={{ width: 'auto', margin: 0 }} onClick={() => setViewMode('engine')}>🔧 Engine View</button>
          <button className={`gcs-button ${viewMode === 'cutaway' ? 'active' : ''}`} style={{ width: 'auto', margin: 0 }} onClick={() => setViewMode('cutaway')}>⚙️ Cutaway Mode</button>
          <button className={`gcs-button ${viewMode === 'diagnostic' ? 'active' : ''}`} style={{ width: 'auto', margin: 0 }} onClick={() => setViewMode('diagnostic')}>🌡️ Diagnostic View</button>
        </div>
      </div>

      <div ref={mountRef} style={{ width: '100%', height: '500px', background: '#f0f0ef', borderRadius: '3px', border: '1px solid #e5e5e5', marginBottom: '16px' }} />

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '12px', marginBottom: '14px' }}>
        <div className="hud-card" style={{ padding: '12px' }}>
          <div className="hud-title">Aircraft Attitude</div>
          <div style={{ fontSize: '13px', color: '#1a1a1a' }}>
            Pitch: <code style={{ color: '#2563eb' }}>{pitch}°</code> | Roll: <code style={{ color: '#2563eb' }}>{roll}°</code> | Yaw: <code style={{ color: '#2563eb' }}>{yaw}°</code>
          </div>
        </div>
        <div className="hud-card" style={{ padding: '12px' }}>
          <div className="hud-title">Route Position</div>
          <div style={{ fontSize: '13px', color: '#1a1a1a' }}>
            Lat: <code style={{ color: '#2563eb' }}>{lat}</code> | Lon: <code style={{ color: '#2563eb' }}>{lon}</code> | Alt: <code style={{ color: '#2563eb' }}>{alt} ft</code>
          </div>
        </div>
        <div className="hud-card" style={{ padding: '12px' }}>
          <div className="hud-title">Propeller Velocity</div>
          <div style={{ fontSize: '13px', color: '#1a1a1a' }}>
            <code style={{ color: '#16a34a', fontWeight: 700 }}>{rpm} RPM</code> (ω = {rads} rad/s)
          </div>
        </div>
      </div>

      <div style={{ background: '#eff6ff', border: '1px solid #bfdbfe', padding: '12px 16px', borderRadius: '3px', fontSize: '12px', color: '#1e40af' }}>
        💡 <b>3D Interaction Guide:</b> Rotate around 3D WebGL drone model. Active view mode: <b>{viewMode.toUpperCase()}</b>. Synchronized with 11 engine sensors, MVEM physics expectations, and residuals.
      </div>
    </div>
  );
}
