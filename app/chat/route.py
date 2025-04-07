from starlette import status
from starlette.websockets import WebSocketDisconnect
from fastapi import WebSocketException
from app.auth.utils import decode_token
from fastapi import HTTPException
from fastapi.params import Depends
from fastapi.websockets import WebSocket
from fastapi.routing import APIRouter
from typing import Annotated
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.main import get_session
from app.chat.connection_manager import ConnectionManager

websocket_route = APIRouter(prefix='/chat', tags=['WebSocket'])
session_dependency = Annotated[AsyncSession, Depends(get_session)]

manager = ConnectionManager()


@websocket_route.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    token = websocket.query_params.get("token")
    if not token:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)

    try:
        user = decode_token(token)
    except HTTPException as ex:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)

    await manager.connect(websocket)

    try:
        await manager.broadcast(f"🔵 {user['username']} joined the chat")
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"👤 You: {data}", websocket)
            await manager.broadcast(f"{user['username']}: {data}", sender=websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"🔴 {user['username']} left the chat")
