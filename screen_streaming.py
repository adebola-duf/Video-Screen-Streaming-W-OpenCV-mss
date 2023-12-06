import asyncio
from fastapi import FastAPI, WebSocket, Request, WebSocketDisconnect, BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import mss
import numpy as np
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


async def generate_screen_frames(websocket: WebSocket, receiver_id: int):
    with mss.mss() as screen_shotter:
        while True:
            monitor = screen_shotter.monitors[1]
            screen_shot_image = screen_shotter.grab(monitor)
            png_bytes = mss.tools.to_png(
                screen_shot_image.rgb, screen_shot_image.size)
            for id, ws in websockets.items():
                if id == receiver_id:
                    await websockets[receiver_id].send_bytes(png_bytes)

            # to allow our server do other things
            await asyncio.sleep(0.1)

websockets: dict[int, WebSocket] = {}


@app.websocket("/video-feed/{sender_id}/{receiver_id}")
async def video_feed(websocket: WebSocket, sender_id: int, receiver_id: int):
    await websocket.accept()
    websockets[sender_id] = websocket

    while True:
        try:
            await generate_screen_frames(websocket, receiver_id)

        except WebSocketDisconnect:
            # Remove the sender_id from the dictionary when the WebSocket is closed
            del websockets[sender_id]


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("screen_streaming.html", {"request": request})
