from concurrent.futures import ThreadPoolExecutor, as_completed

import requests


def send_request(url):
    """Function to send a single HTTP GET request to the specified URL."""
    try:
        response = requests.post(url)
        return response.status_code
    except Exception as e:
        return str(e)

def main(url, num_requests):
    """Function to send multiple requests to the specified URL using multithreading."""
    with ThreadPoolExecutor(max_workers=1000) as executor:
        # Create a list to hold the futures.
        futures = [executor.submit(send_request, url) for _ in range(num_requests)]
        
        # Process the results as they are completed.
        for future in as_completed(futures):
            response = future.result()
            print(response)

if __name__ == "__main__":
    test_url = "http://localhost:8000/analytics"  # Replace with your target URL
    total_requests = 10000  # Total number of requests to send

    main(test_url, total_requests)
