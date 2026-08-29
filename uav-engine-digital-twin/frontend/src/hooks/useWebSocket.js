import { useEffect, useState } from "react";

export function useWebSocket(missionId) {
  const [state, setState] = useState(null);

  useEffect(() => {
    if (!missionId) return;

    const ws = new WebSocket(
      `ws://localhost:8000/ws/missions/${missionId}`
    );

    ws.onmessage = (event) => {
      setState(JSON.parse(event.data));
    };

    return () => ws.close();
  }, [missionId]);

  return state;
}
