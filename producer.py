# producer.py
from kafka import KafkaProducer
from time import strftime
import time

# Use Docker service name instead of IP
KAFKA_BROKER = 'kafka:29092'

def create_producer():
    """Create Kafka producer with retry logic for Docker startup sequence"""
    max_retries = 10
    retry_delay = 5
    for attempt in range(max_retries):
        try:
            return KafkaProducer(bootstrap_servers=KAFKA_BROKER)
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"Kafka connection failed: {e}. Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                raise

producer = create_producer()

def determine_topic(status_code):
    """
    Determine the Kafka topic based on the HTTP status code.
    - 500 or greater: error-logs
    - 400–499: warning-logs
    - Otherwise: info-logs
    """
    if status_code >= 500:
        return "error-logs"
    elif status_code >= 400:
        return "warning-logs"
    else:
        return "info-logs"

def send_log(endpoint, status_code):
    """
    Constructs a log message, determines its destination topic,
    sends the log message to Kafka, and prints the message to the console.
    """
    timestamp = strftime('%Y-%m-%d %H:%M:%S')
    log_message = f"{timestamp} | {endpoint} | Status: {status_code}"
    topic = determine_topic(status_code)
    producer.send(topic, log_message.encode('utf-8'))
    producer.flush()
    print(f"Produced to {topic}: {log_message}")
