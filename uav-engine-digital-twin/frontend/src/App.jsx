import React, { useState, useEffect } from 'react';
import './styles/theme.css';
import { gcsApi } from './services/api';
import AvionicsSidebar from './components/AvionicsSidebar';
import AvionicsHeader from './components/AvionicsHeader';
import TopKpiCards from './components/TopKpiCards';
import Tab0AvionicsHud from './components/tabs/Tab0AvionicsHud';
import Tab1DigitalTwin3D from './components/tabs/Tab1DigitalTwin3D';
import Tab2GisTacticalMap from './components/tabs/Tab2GisTacticalMap';
import Tab3AiDiagnosticsShap from './components/tabs/Tab3AiDiagnosticsShap';
import Tab4RulMonteCarlo from './components/tabs/Tab4RulMonteCarlo';
import Tab5MerkleAuditLedger from './components/tabs/Tab5MerkleAuditLedger';

export default function App() {
  const [activeTab, setActiveTab] = useState(0);
  const [gcsState, setGcsState] = useState(null);
  const [profile, setProfile] = useState('Normal Cruise');
  const [faultChoice, setFaultChoice] = useState('None / Healthy');
  const [faultSeverity, setFaultSeverity] = useState(0.0);
  const [autoStream, setAutoStream] = useState(false);

  useEffect(() => {
    fetchInitialState();
  }, []);

  useEffect(() => {
    let interval = null;
    if (autoStream) {
      interval = setInterval(() => {
        handleStep();
      }, 100); // 10 Hz
    }
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [autoStream, profile, faultChoice, faultSeverity]);

  const fetchInitialState = async () => {
    try {
      const data = await gcsApi.getState();
      setGcsState(data);
    } catch (err) {
      console.error('Error fetching GCS state:', err);
    }
  };

  const handleStep = async () => {
    try {
      const payload = {
        profile,
        fault_choice: faultChoice,
        fault_severity: faultSeverity
      };
      const data = await gcsApi.stepTelemetry(payload);
      setGcsState(data);
    } catch (err) {
      console.error('Error stepping telemetry:', err);
    }
  };

  const handleReset = async () => {
    try {
      const data = await gcsApi.resetTelemetry();
      setGcsState(data);
      setAutoStream(false);
    } catch (err) {
      console.error('Error resetting telemetry:', err);
    }
  };

  const tabs = [
    '📡 AVIONICS HUD & COCKPIT',
    '🛸 3D DIGITAL TWIN CANAL',
    '🗺️ GIS TACTICAL MAP',
    '🧠 AI DIAGNOSTICS & SHAP',
    '⏳ RUL & MONTE CARLO',
    '🔒 MERKLE AUDIT LEDGER'
  ];

  return (
    <div className="app-container">
      <AvionicsSidebar
        profile={profile}
        setProfile={setProfile}
        faultChoice={faultChoice}
        setFaultChoice={setFaultChoice}
        faultSeverity={faultSeverity}
        setFaultSeverity={setFaultSeverity}
        autoStream={autoStream}
        setAutoStream={setAutoStream}
        onStep={handleStep}
        onReset={handleReset}
      />

      <main className="app-main">
        <AvionicsHeader profile={profile} step={gcsState?.step || 0} />

        <TopKpiCards state={gcsState} />

        <div className="tab-navigation">
          {tabs.map((tabLabel, idx) => (
            <button
              key={idx}
              className={`tab-button ${activeTab === idx ? 'active' : ''}`}
              onClick={() => setActiveTab(idx)}
            >
              {tabLabel}
            </button>
          ))}
        </div>

        <div className="tab-content-panel">
          {activeTab === 0 && <Tab0AvionicsHud state={gcsState} />}
          {activeTab === 1 && <Tab1DigitalTwin3D state={gcsState} />}
          {activeTab === 2 && <Tab2GisTacticalMap state={gcsState} />}
          {activeTab === 3 && <Tab3AiDiagnosticsShap state={gcsState} />}
          {activeTab === 4 && <Tab4RulMonteCarlo state={gcsState} />}
          {activeTab === 5 && <Tab5MerkleAuditLedger />}
        </div>
      </main>
    </div>
  );
}
