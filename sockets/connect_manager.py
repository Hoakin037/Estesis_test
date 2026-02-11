from fastapi import WebSocket, WebSocketDisconnect, HTTPException

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, game_sid: str):
        await websocket.accept()
        if game_sid not in self.active_connections:
            self.active_connections[game_sid] = []
        self.active_connections[game_sid].append(websocket)

    async def disconnect(self, websocket: WebSocket, game_sid: str):
        if websocket in self.active_connections:
            try:
                self.active_connections[game_sid].remove(websocket)
            except ValueError:
                raise HTTPException(status_code=404, detail="Соединение уже удалено или еще не было подключено.")
            if not self.active_connections[game_sid]:
                del self.active_connections[game_sid]

    async def broadcast(self, game_sid: str, message: dict):
        if game_sid not in self.active_connections:
            return
        
        for connection in self.active_connections[game_sid][:]:
            try:
                await connection.send_json(message) 
            except Exception:
                self.disconnect(connection, game_sid)


