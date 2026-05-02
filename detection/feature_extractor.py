import os
import sqlite3
from collections import defaultdict
from datetime import datetime, timedelta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_NAME = os.path.join(BASE_DIR, "logs.db")


def fetch_logs():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    time_limit = (datetime.now() - timedelta(seconds=60)).isoformat()
    cursor.execute("SELECT ip, path, action, timestamp FROM logs WHERE timestamp >= ?", (time_limit,))
    rows = cursor.fetchall()

    conn.close()
    return rows


def extract_features():
    logs = fetch_logs()
    ip_data = defaultdict(list)

    for ip, path, action, timestamp in logs:
        time_obj = datetime.fromisoformat(timestamp)
        ip_data[ip].append((time_obj, path, action))

    features = []

    for ip, entries in ip_data.items():
        total_requests = len(entries)
        failed_logins = sum(1 for entry in entries if "failed" in entry[2])
        success_logins = sum(1 for entry in entries if "success" in entry[2])
        unique_paths = len({entry[1] for entry in entries})

        entries.sort(key=lambda entry: entry[0])
        if len(entries) > 1:
            time_diff = (entries[-1][0] - entries[0][0]).total_seconds()
            request_rate = total_requests / time_diff if time_diff > 0 else total_requests
        else:
            request_rate = total_requests

        features.append(
            {
                "ip": ip,
                "total_requests": total_requests,
                "failed_logins": failed_logins,
                "success_logins": success_logins,
                "unique_paths": unique_paths,
                "request_rate": request_rate,
            }
        )

    return features


if __name__ == "__main__":
    for row in extract_features():
        print(row)
