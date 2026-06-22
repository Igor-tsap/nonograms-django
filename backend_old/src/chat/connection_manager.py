from fastapi import WebSocket
from database.redis import redis
import asyncio


class ConnectionManager:
    def __init__(self):
        self.connections = {}
        self.listeners = set()

    async def connect(self, websocket: WebSocket, room_id: str):
        await websocket.accept()
        if room_id not in self.connections:
            self.connections[room_id] = set()
        self.connections[room_id].add(websocket)

        if room_id not in self.listeners:
            self.listeners.add(room_id)
            asyncio.create_task(self.start_room_listener(room_id))

    def disconnect(self, websocket: WebSocket, room_id: str):
        if room_id in self.connections:   
            if websocket in self.connections[room_id]:
                self.connections[room_id].discard(websocket)

                if not self.connections[room_id]:
                    del self.connections[room_id]

    async def broadcast_local(self, message: str, room_id: str):
        dead_connections = []

        for connection in self.connections.get(room_id, set()):
            try:
                await connection.send_text(message)
            except Exception as e:
                print("broadcast error:", e)
                dead_connections.append(connection)

        for connection in dead_connections:
            self.disconnect(connection, room_id)

    async def start_room_listener(self, room_id: str):
        pubsub = redis.pubsub()
        await pubsub.subscribe(f"puzzle_{room_id}")
        async for message in pubsub.listen():
            if room_id not in self.connections:
                await pubsub.unsubscribe(f"puzzle_{room_id}")
                break
            if message['type'] == 'message':
                await self.broadcast_local(message['data'], room_id)