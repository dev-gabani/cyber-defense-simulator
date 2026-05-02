import asyncio
import os

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from database.db import create_table
from defense.defense import get_blocked_ips
from detection.feature_extractor import extract_features
from detection.ml_model import label_features
from server.routes import router

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIST = os.path.join(BASE_DIR, "frontend", "dist")
FRONTEND_INDEX = os.path.join(FRONTEND_DIST, "index.html")

create_table()

app = FastAPI(title="Cyber Defense Simulator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

if os.path.isdir(FRONTEND_DIST):
    app.mount("/assets", StaticFiles(directory=os.path.join(FRONTEND_DIST, "assets")), name="assets")


def react_dashboard():
    if not os.path.exists(FRONTEND_INDEX):
        return JSONResponse(
            status_code=503,
            content={
                "error": "React dashboard is not built yet",
                "solution": "Run `cd frontend` then `npm run build`, then restart the backend.",
            },
        )

    return FileResponse(FRONTEND_INDEX)


@app.get("/")
def home():
    return react_dashboard()


@app.get("/dashboard")
def dashboard():
    return react_dashboard()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    while True:
        try:
            data = label_features(extract_features())

            await websocket.send_json(
                {
                    "features": data,
                    "blocked_ips": get_blocked_ips(),
                }
            )

        except WebSocketDisconnect:
            print("[WEBSOCKET] Client disconnected")
            break
        except Exception as exc:
            print("[WEBSOCKET ERROR]:", exc)

        await asyncio.sleep(1)
