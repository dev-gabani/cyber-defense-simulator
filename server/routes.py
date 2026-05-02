from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from database.db import get_connection
from defense.defense import block_ip, get_blocked_ips, is_blocked
from detection.feature_extractor import extract_features
from detection.ml_model import label_features
from server.logger import get_client_ip, log_request

router = APIRouter()


def apply_defense_policy(ip):
    for feature in label_features(extract_features()):
        if feature.get("ip") != ip:
            continue

        if feature.get("label") == "ATTACK":
            block_ip(ip)

        break


@router.get("/data")
async def get_data(request: Request):
    ip = get_client_ip(request)

    if is_blocked(ip):
        return JSONResponse(status_code=403, content={"error": "Blocked by defense system"})

    log_request(request, "data_access")
    apply_defense_policy(ip)
    return {"data": "Some secure data"}


@router.post("/login")
async def login(request: Request):
    ip = get_client_ip(request)

    if is_blocked(ip):
        return JSONResponse(status_code=403, content={"error": "Blocked by defense system"})

    body = await request.json()

    username = body.get("username")
    password = body.get("password")

    if username == "admin" and password == "1234":
        status = "success"
    else:
        status = "failed"

    log_request(request, f"login_{status}")
    apply_defense_policy(ip)

    return {"status": status}


@router.get("/health")
async def health():
    return {"status": "ok"}


@router.get("/blocked")
async def blocked_ips():
    return {"blocked_ips": get_blocked_ips()}


@router.get("/logs")
async def logs(limit: int = 50):
    safe_limit = max(1, min(limit, 500))

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT ip, path, action, timestamp
        FROM logs
        ORDER BY id DESC
        LIMIT ?
        """,
        (safe_limit,),
    )
    rows = cursor.fetchall()
    conn.close()

    return {
        "logs": [
            {"ip": ip, "path": path, "action": action, "timestamp": timestamp}
            for ip, path, action, timestamp in rows
        ]
    }
