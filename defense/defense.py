from database.db import get_connection
from datetime import datetime

def block_ip(ip):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO blocked_ips (ip, timestamp) VALUES (?, ?)", (ip, datetime.now().isoformat()))
    conn.commit()
    conn.close()
    print(f"[DEFENSE] Blocked IP: {ip}")

def is_blocked(ip):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM blocked_ips WHERE ip = ?", (ip,))
    res = cursor.fetchone()
    conn.close()
    return res is not None

def get_blocked_ips():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT ip FROM blocked_ips")
    res = [row[0] for row in cursor.fetchall()]
    conn.close()
    return res