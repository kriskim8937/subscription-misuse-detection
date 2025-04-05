import json
import time
import random
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],  # Switch to localhost
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    retries=5
)

users = ["user_1", "user_2", "user_3"]
devices = ["iPhone", "Android", "Windows", "Mac"]
locations = ["UK", "US", "Germany", "India"]

def generate_fake_data():
    while True:
        event = {
            "user_id": random.choice(users),
            "device_id": random.choice(devices),
            "ip_location": random.choice(locations),
            "timestamp": time.time()
        }
        producer.send('user_activity', event)
        print(f"Sent: {event}")
        time.sleep(1)

generate_fake_data()