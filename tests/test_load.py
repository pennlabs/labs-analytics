import json
import random
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

import requests
from test_token import get_tokens


# Runtime should be less that 3 seconds for most laptops
BENCHMARK_TIME = 3  # seconds

# Simulating 16 users making 1000 requests
NUMBER_OF_REQUESTS = 1000
THREADS = 16


def make_request():
    access_token, _ = get_tokens()

    url = "http://localhost:8000/analytics"
    payload = json.dumps(
        {
            "product": random.randint(1, 10),
            "pennkey": "test_usr",
            "timestamp": int(datetime.now().timestamp()),
            "data": [
                {"key": "user.click", "value": str(random.randint(1, 1000))},
                {"key": "user.drag", "value": str(random.randint(1, 1000))},
                {"key": "data.dowload", "value": str(random.randint(1, 1000))},
                {"key": "user.drive", "value": str(random.randint(1, 1000))},
                {"key": "user.play", "value": str(random.randint(1, 1000))},
                {"key": "user.sit", "value": str(random.randint(1, 1000))},
                {"key": "user.stand", "value": str(random.randint(1, 1000))},
                {"key": "user.bike", "value": str(random.randint(1, 1000))},
                {"key": "user.flip", "value": str(random.randint(1, 1000))},
                {"key": "food.eat", "value": str(random.randint(1, 1000))},
            ],
        }
    )
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }

    try:
        response = requests.post(url, headers=headers, data=payload)
    except Exception as e:
        if "ConnectionError" in str(e):
            return "Please make sure the server is running."
        return str(e)
    return response.text


def run_threads():
    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        _ = [executor.submit(make_request) for _ in range(NUMBER_OF_REQUESTS)]


def test_load():
    start = time.time()
    run_threads()
    end = time.time()
    runtime = end - start
    print(f"Time taken: {runtime} seconds")
    assert runtime < BENCHMARK_TIME
