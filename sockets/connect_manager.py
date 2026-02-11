from fastapi import WebSocket
from uuid import UUID
from collections import defaultdict


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[UUID,
                                      dict[int, WebSocket]] = defaultdict(dict)

    async def connect(self, websocket: WebSocket, game_sid: UUID, player_id: int):
        await websocket.accept()
        self.active_connections[game_sid][player_id] = websocket

    def disconnect(self, websocket: WebSocket, game_sid: UUID, player_id: int):
        if game_sid in self.active_connections:
            self.active_connections[game_sid].pop(player_id, None)

    def get_websocket(self, game_sid: UUID, player_id: int) -> WebSocket | None:
        return self.active_connections.get(game_sid, {}).get(player_id)

    async def broadcast(self, game_sid: UUID, message: dict):
        if game_sid not in self.active_connections:
            return

        connections_to_remove = []
        for player_id, websocket in self.active_connections[game_sid].items():
            try:
                await websocket.send_json(message)
            except Exception:
                connections_to_remove.append(player_id)

        for player_id in connections_to_remove:
            self.disconnect(None, game_sid, player_id)
