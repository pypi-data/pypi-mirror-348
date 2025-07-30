import json
import threading
import time
import requests
from .collector import flush

def send(agent_url, metrics):
    try:
        payload = {
            "collected_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "metrics": metrics
        }
        response = requests.post(agent_url, json=payload, timeout=3)
        if response.status_code >= 400:
            pass
            # print(f"[Watchlog APM] Agent error: {response.status_code}")
    except Exception as e:
        pass
        # print(f"[Watchlog APM] Send failed: {e}")

def start(agent_url="http://localhost:3774/apm/flask", interval=10):
    def loop():
        while True:
            metrics = flush()
            if metrics:
                send(agent_url, metrics)
            time.sleep(interval)

    thread = threading.Thread(target=loop, daemon=True)
    thread.start()
