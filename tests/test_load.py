import json
import random
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

import requests


def make_request():
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
    }

    try:
        response = requests.request("POST", url, headers=headers, data=payload)
    except Exception as e:
        if "ConnectionError" in str(e):
            return "Please make sure the server is running."
        return str(e)
    return response.text


def run_threads():
    # Simulating 16 users making 100000 requests
    number_of_requests = 1000
    with ThreadPoolExecutor(max_workers=16) as executor:
        futures = [executor.submit(make_request) for _ in range(number_of_requests)]
        # for future in futures:
        # print(future.result())


def test_load():
    start = time.time()
    run_threads()
    end = time.time()
    runtime = end - start
    print(f"Time taken: {end - start} seconds")
    # Runtime should be less that 3 seconds for most laptops
    assert runtime < 3
