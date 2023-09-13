from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from loguru import logger

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
            await websocket.receive_text()
            # [{}] - получаем последнее сообщение
            try:
                data = cache.get_json_set('messages', limit=-1)
                await websocket.send_json(data[0])
            except IndexError:
                await websocket.send_json(None)
    except WebSocketDisconnect as e:
        logger.warning(e)
        return
