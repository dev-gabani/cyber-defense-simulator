import random
import time

import requests

TARGET = "http://127.0.0.1:8000"
SIMULATED_IPS = [
    "192.168.1.10",
    "192.168.1.11",
    "10.0.0.21",
    "10.0.0.22",
    "172.16.0.15",
]


def headers_for(ip=None):
    return {"X-Forwarded-For": ip or random.choice(SIMULATED_IPS)}


def normal_traffic():
    print("\n[START] Normal Traffic (Press CTRL+C to stop)\n")
    try:
        while True:
            response = requests.get(f"{TARGET}/data", headers=headers_for(), timeout=5)
            print(f"[NORMAL] Status: {response.status_code}")
            time.sleep(random.uniform(1, 3))

    except KeyboardInterrupt:
        print("\n[STOPPED] Normal traffic stopped by user\n")

    except Exception as exc:
        print(f"[ERROR] {exc}")


def dos_attack():
    print("\n[START] DoS Attack (Press CTRL+C to stop)\n")
    attacker_ip = "203.0.113.50"
    try:
        while True:
            response = requests.get(f"{TARGET}/data", headers=headers_for(attacker_ip), timeout=5)
            print(f"[FLOOD] Status: {response.status_code}")

    except KeyboardInterrupt:
        print("\n[STOPPED] DoS attack stopped by user\n")

    except Exception as exc:
        print(f"[ERROR] {exc}")


def brute_force():
    print("\n[START] Brute Force Attack (Press CTRL+C to stop)\n")

    attacker_ip = "198.51.100.25"
    passwords = ["admin", "password", "test", "letmein", "qwerty", "welcome"]

    try:
        while True:
            for password in passwords:
                response = requests.post(
                    f"{TARGET}/login",
                    json={"username": "admin", "password": password},
                    headers=headers_for(attacker_ip),
                    timeout=5,
                )

                print(f"[BRUTE] Trying: {password} | Status: {response.json()}")
                time.sleep(0.2)

    except KeyboardInterrupt:
        print("\n[STOPPED] Brute force attack stopped by user\n")

    except Exception as exc:
        print(f"[ERROR] {exc}")


if __name__ == "__main__":
    while True:
        print("\n=== Attack Simulator ===")
        print("1. Normal Traffic")
        print("2. DoS Attack")
        print("3. Brute Force")
        print("4. Exit")

        try:
            choice = input("Enter choice: ").strip()
        except EOFError:
            break

        if choice == "1":
            normal_traffic()
        elif choice == "2":
            dos_attack()
        elif choice == "3":
            brute_force()
        elif choice == "4":
            print("Exiting...")
            break
        else:
            print("Invalid choice, please try again.")
