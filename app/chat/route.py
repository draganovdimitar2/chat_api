from starlette import status
from starlette.websockets import WebSocketDisconnect
from app.auth.utils import decode_token
from fastapi import HTTPException
from fastapi.params import Depends
from fastapi.websockets import WebSocket
from fastapi.routing import APIRouter
from typing import Annotated
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.main import get_session
from app.chat.connection_manager import ConnectionManager

websocket_route = APIRouter(prefix='/ws', tags=['WebSocket'])
session_dependency = Annotated[AsyncSession, Depends(get_session)]

manager = ConnectionManager()


@websocket_route.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    try:
        user = decode_token(token)
    except HTTPException:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

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
