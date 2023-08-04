from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from datetime import datetime

from db.postgres.models import NetworkClient
from .import cache


router = APIRouter(
    prefix='/api/v1/ws',
    tags=['WebSockets']
)

@router.websocket('/netclients')
async def netclients_ws(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            client = await websocket.receive_text()
            data = cache.get_json_set('logon', limit=-1)  # [{}] - получаем последнее сообщение
            await websocket.send_json(data[0])
    except WebSocketDisconnect:
        return