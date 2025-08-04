import argparse
import random  # For dummy uptime calculation; replace with real logic as needed.
from kafka import KafkaConsumer
from datetime import datetime
import db  # Import the helper functions from db.py
import time

# Parse command-line arguments for topics to subscribe to.
parser = argparse.ArgumentParser(
    description="Kafka Consumer that subscribes to specified topics and processes log messages."
)
parser.add_argument(
    "topics",
    nargs="+",
    help="List of Kafka topics to subscribe to (space-separated)."
)
args = parser.parse_args()

topics_to_subscribe = args.topics

# Use Docker service name instead of IP
KAFKA_BROKER = 'kafka:29092'

def create_consumer(topics):
    """Create Kafka consumer with retry logic for Docker startup sequence"""
    max_retries = 10
    retry_delay = 5
    for attempt in range(max_retries):
        try:
            return KafkaConsumer(
                *topics,
                bootstrap_servers=KAFKA_BROKER,
                auto_offset_reset='earliest',
                group_id='stats-consumer-group',
                enable_auto_commit=True
            )
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"Kafka connection failed: {e}. Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                raise

# Ensure the logs table exists before processing any messages.
db.create_table_if_not_exists()

# Create the Kafka consumer.
consumer = create_consumer(topics_to_subscribe)

# Establish a connection to the MySQL DB using our shared connection function from db.py.
conn = db.get_connection()
cursor = conn.cursor()

def calculate_uptime(log_line):
    """
    Dummy uptime calculation.
    Replace this function with your actual uptime logic based on log content.
    For demonstration, we return a random uptime percentage.
    """
    return round(random.uniform(95.0, 100.0), 2)

def insert_log(topic, log_text, uptime):
    """
    Inserts a log entry into the logs table.
    """
    query = "INSERT INTO logs (topic, log_text, uptime, created_at) VALUES (%s, %s, %s, %s)"
    values = (topic, log_text, uptime, datetime.now())
    cursor.execute(query, values)
    conn.commit()

print(f"Subscribed to topics: {topics_to_subscribe}")
print("Waiting for messages...\n")

try:
    # Continuously read messages from the topics.
    for message in consumer:
        log_text = message.value.decode('utf-8')
        topic = message.topic
        uptime = calculate_uptime(log_text)
        
        print(f"Topic: {topic} | Log: {log_text} | Uptime: {uptime}%")
        insert_log(topic, log_text, uptime)

except KeyboardInterrupt:
    print("\nConsumer stopped manually.")

finally:
    cursor.close()
    conn.close()
    print("Database connection closed.")
