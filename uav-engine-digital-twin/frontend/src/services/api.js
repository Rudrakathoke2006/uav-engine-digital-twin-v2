import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_URL || '/api';

export const gcsApi = {
  getState: async () => {
    const res = await axios.get(`${API_BASE}/gcs/state`);
    return res.data;
  },
  stepTelemetry: async (payload = {}) => {
    const res = await axios.post(`${API_BASE}/gcs/step`, payload);
    return res.data;
  },
  resetTelemetry: async () => {
    const res = await axios.post(`${API_BASE}/gcs/reset`);
    return res.data;
  },
  runMonteCarlo: async (duration = 180) => {
    const res = await axios.post(`${API_BASE}/gcs/monte-carlo`, { mission_duration_min: duration });
    return res.data;
  },
  verifyAudit: async () => {
    const res = await axios.get(`${API_BASE}/gcs/audit/verify`);
    return res.data;
  },
  fetchReplay: async (sessionId = 'SESS_ISR-042') => {
    const res = await axios.get(`${API_BASE}/gcs/audit/replay/${sessionId}`);
    return res.data;
  }
};
