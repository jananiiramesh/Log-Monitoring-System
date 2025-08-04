
import time
import random
import requests
from producer import send_log  # Import the send_log function from producer.py

# Use Docker service name instead of localhost
BASE_URL = "http://flask-api:5000"

# List of endpoints provided by your Flask API.
endpoints = [
    "/endpoint1",
    "/endpoint2",
    "/endpoint3",
    "/endpoint4",
    "/endpoint5",
    "/endpoint6",
    "/endpoint7"
]

def generate_logs():
    # Wait a bit for the Flask API to be ready
    print("Waiting for Flask API to be available...")
    time.sleep(10)
    
    while True:
        # Randomly choose an endpoint.
        ep = random.choice(endpoints)
        url = BASE_URL + ep
        try:
            response = requests.get(url)
            status = response.status_code
            print(f"Called {url} - Status Code: {status}")
            # Pass the generated log to the producer module
            send_log(ep, status)
        except Exception as e:
            print(f"Error calling {url}: {e}")
        time.sleep(1)  # Adjust interval as needed.

if __name__ == "__main__":
    generate_logs()
