import json
import time
import random
from datetime import datetime, timedelta
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

users = [f"user_{i}" for i in range(1, 101)]  # 100 users
devices = ["iPhone", "Android", "Windows", "Mac"]
locations = ["UK", "US", "Germany", "India", "France"]
plans = ["free_trial", "premium", "family", "student"]

def generate_login_attempt():
    user = random.choice(users)
    event = {
        "event_type": "login_attempt",
        "user_id": user,
        "device_id": random.choice(devices),
        "ip_address": f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}",
        "location": random.choice(locations),
        "is_successful": random.choices([True, False], weights=[0.9, 0.1])[0],
        "timestamp": datetime.utcnow().isoformat()
    }
    producer.send('login_attempts', event)
    print(f"Sent login event: {user}")

def generate_payment_event():
    event = {
        "event_type": "payment",
        "user_id": random.choice(users),
        "amount": round(random.uniform(5, 50), 2),
        "currency": "USD",
        "status": random.choices(["completed", "failed", "chargeback"], weights=[0.85, 0.1, 0.05])[0],
        "timestamp": datetime.utcnow().isoformat()
    }
    producer.send('payment_events', event)
    print(f"Sent payment event: {event['user_id']}")

def generate_subscription_event():
    event = {
        "event_type": "subscription",
        "user_id": random.choice(users),
        "plan_id": random.choice(plans),
        "is_trial": random.choices([True, False], weights=[0.3, 0.7])[0],
        "timestamp": (datetime.utcnow() - timedelta(days=random.randint(0, 30))).isoformat()  # Backdated
    }
    producer.send('subscription_updates', event)
    print(f"Sent subscription event: {event['user_id']}")

while True:
    generate_login_attempt()
    if random.random() < 0.3:  # 30% chance to generate payment/subscription
        generate_payment_event()
    if random.random() < 0.2:  # 20% chance
        generate_subscription_event()
    time.sleep(random.uniform(0.5, 2))  # Random delay