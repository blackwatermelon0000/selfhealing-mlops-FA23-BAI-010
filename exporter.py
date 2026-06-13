import os
import time
import requests
from prometheus_client import Gauge, start_http_server

APP_CONFIDENCE_URL = os.getenv(
    "APP_CONFIDENCE_URL",
    "http://127.0.0.1:32500/api/latest-confidence"
)

confidence_gauge = Gauge(
    "prediction_confidence_score",
    "Latest confidence score returned by the sentiment API"
)

def poll_confidence():
    try:
        response = requests.get(APP_CONFIDENCE_URL, timeout=3)
        response.raise_for_status()
        value = float(response.json().get("confidence", 1.0))
    except Exception:
        value = 1.0

    confidence_gauge.set(value)

if __name__ == "__main__":
    start_http_server(8000)
    while True:
        poll_confidence()
        time.sleep(5)
