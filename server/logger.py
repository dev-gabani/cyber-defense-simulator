from datetime import datetime

from database.db import get_connection


def get_client_ip(request):
    forwarded_for = request.headers.get("x-forwarded-for")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()

    real_ip = request.headers.get("x-real-ip")
    if real_ip:
        return real_ip.strip()

    return request.client.host if request.client else "unknown"


def log_request(request, action):
    client_ip = get_client_ip(request)
    timestamp = datetime.now().isoformat()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO logs (ip, path, action, timestamp)
        VALUES (?, ?, ?, ?)
        """,
        (client_ip, request.url.path, action, timestamp),
    )
    cursor.execute(
        """
        DELETE FROM logs
        WHERE id NOT IN (
            SELECT id FROM logs
            ORDER BY id DESC
            LIMIT 1000
        )
        """
    )

    conn.commit()
    conn.close()

    print(f"[LOGGED] {client_ip} | {action}")
