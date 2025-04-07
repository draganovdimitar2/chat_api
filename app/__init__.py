from fastapi import FastAPI
from app.auth.routes import router as user_router
from app.chat.route import websocket_route as ws_route

app = FastAPI()
app.include_router(user_router)
app.include_router(ws_route)
