"""
WebSocket Connection Manager (Section 16.3).
"""

from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active: dict[str, list[WebSocket]] = {}

    async def connect(self, mission_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active.setdefault(mission_id, []).append(websocket)

    def disconnect(self, mission_id: str, websocket: WebSocket):
        if mission_id in self.active and websocket in self.active[mission_id]:
            self.active[mission_id].remove(websocket)

    async def broadcast(self, mission_id: str, payload: dict):
        for ws in self.active.get(mission_id, []):
            try:
                await ws.send_json(payload)
            except Exception:
                pass
