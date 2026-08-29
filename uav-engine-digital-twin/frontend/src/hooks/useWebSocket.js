import { useEffect, useState } from "react";

export function useWebSocket(missionId) {
  const [state, setState] = useState(null);

  useEffect(() => {
    if (!missionId) return;

    const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
    const host = import.meta.env.VITE_WS_URL || window.location.host;
    const wsUrl = host.includes("http") || host.includes("ws") 
      ? host 
      : `${protocol}//${host}/ws/missions/${missionId}`;

    let ws;
    try {
      ws = new WebSocket(wsUrl);
      ws.onmessage = (event) => {
        setState(JSON.parse(event.data));
      };
    } catch (e) {
      console.warn("WebSocket connection skipped or unavailable:", e);
    }

    return () => {
      if (ws) ws.close();
    };
  }, [missionId]);

  return state;
}
