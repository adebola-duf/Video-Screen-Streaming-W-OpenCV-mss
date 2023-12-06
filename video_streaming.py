from fastapi import FastAPI, WebSocket, Request, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import cv2
import numpy as np
import asyncio

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# This line initializes a video capture object (cap) using OpenCV's cv2.VideoCapture.
# The argument 0 indicates that the default camera (usually the built-in webcam) should be used.
# If you have multiple cameras or other video sources, you can specify a different index accordingly.
cap = cv2.VideoCapture(0)


async def generate_frames(websocket: WebSocket):
    while True:

        # Read a frame from the webcam
        # cap.read(): Reads a frame from the video capture object (cap).
        # The returned success variable indicates whether the frame was successfully read, and frame contains the actual image data.

        success, video_frame = cap.read()

        if not success:
            break

        # 0: Flip vertically (upside down).
        # 1: Flip horizontally (left to right).
        # -1: Flip both vertically and horizontally.
        video_frame = cv2.flip(video_frame, 1)

        # Encode the frame to JPEG format
        # cv2.imencode('.jpg', frame): Encodes the frame in JPEG format.
        # The result is a tuple where the first element is a boolean indicating success,
        # and the second element is a NumPy array containing the encoded image data.
        _, video_buffer = cv2.imencode('.jpg', video_frame)
        # print(video_buffer)

        # Convert the frame to bytes
        # buffer.tobytes(): Converts the NumPy array to bytes. This is the format that will be sent over the WebSocket connection.
        video_frame_bytes = video_buffer.tobytes()
        # Send the frame bytes to the client via WebSocket
        await websocket.send_bytes(video_frame_bytes)

        await asyncio.sleep(0.1)


@app.websocket("/video-feed")
async def video_feed(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Continuously send frames to the client
            await generate_frames(websocket)
    except WebSocketDisconnect:
        cap.release()


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("video_streaming.html", {"request": request})
