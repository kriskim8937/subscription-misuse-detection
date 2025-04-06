import json
import psycopg2
from kafka import KafkaConsumer
from psycopg2.extras import execute_values
from datetime import datetime

# Kafka setup
KAFKA_TOPICS = ['login_attempts', 'payment_events', 'subscription_updates']
KAFKA_BOOTSTRAP_SERVERS = 'localhost:9092'

# Postgres setup
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'dbname': 'streaming',
    'user': 'postgres',
    'password': 'postgres'  # Change as needed
}

# Connect to Postgres
def get_pg_conn():
    return psycopg2.connect(**DB_CONFIG)

# Create tables if they don't exist
def ensure_tables_exist():
    create_sql = """
    CREATE TABLE IF NOT EXISTS raw_login_attempts (
        event_id SERIAL PRIMARY KEY,
        user_id TEXT,
        device_id TEXT,
        ip_address TEXT,
        location TEXT,
        is_successful BOOLEAN,
        timestamp TIMESTAMPTZ,
        ingested_at TIMESTAMPTZ DEFAULT NOW()
    );

    CREATE TABLE IF NOT EXISTS raw_payments (
        event_id SERIAL PRIMARY KEY,
        user_id TEXT,
        amount DECIMAL(10, 2),
        currency TEXT,
        status TEXT,
        timestamp TIMESTAMPTZ,
        ingested_at TIMESTAMPTZ DEFAULT NOW()
    );

    CREATE TABLE IF NOT EXISTS raw_subscriptions (
        event_id SERIAL PRIMARY KEY,
        user_id TEXT,
        plan_id TEXT,
        is_trial BOOLEAN,
        timestamp TIMESTAMPTZ,
        ingested_at TIMESTAMPTZ DEFAULT NOW()
    );
    """
    with get_pg_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(create_sql)
        conn.commit()

# Insert events into the correct table
def insert_events(topic, events):
    if not events:
        return

    with get_pg_conn() as conn:
        with conn.cursor() as cur:
            if topic == 'login_attempts':
                execute_values(
                    cur,
                    """
                    INSERT INTO raw_login_attempts 
                        (user_id, device_id, ip_address, location, is_successful, timestamp)
                    VALUES %s
                    """,
                    [(
                        e['user_id'],
                        e['device_id'],
                        e['ip_address'],
                        e['location'],
                        e['is_successful'],
                        datetime.fromisoformat(e['timestamp'])
                    ) for e in events]
                )
            elif topic == 'payment_events':
                execute_values(
                    cur,
                    """
                    INSERT INTO raw_payments 
                        (user_id, amount, currency, status, timestamp)
                    VALUES %s
                    """,
                    [(
                        e['user_id'],
                        e['amount'],
                        e['currency'],
                        e['status'],
                        datetime.fromisoformat(e['timestamp'])
                    ) for e in events]
                )
            elif topic == 'subscription_updates':
                execute_values(
                    cur,
                    """
                    INSERT INTO raw_subscription_updates 
                        (user_id, plan_id, is_trial, timestamp)
                    VALUES %s
                    """,
                    [(
                        e['user_id'],
                        e['plan_id'],
                        e['is_trial'],
                        datetime.fromisoformat(e['timestamp'])
                    ) for e in events]
                )
        conn.commit()

def main():
    print("Ensuring tables exist...")
    ensure_tables_exist()

    consumer = KafkaConsumer(
        *KAFKA_TOPICS,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='misuse-detection-group',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    batch = {topic: [] for topic in KAFKA_TOPICS}
    BATCH_SIZE = 10  # Flush every 10 messages per topic

    for msg in consumer:
        topic = msg.topic
        batch[topic].append(msg.value)
        print(f"Consumed [{topic}]: {msg.value}")

        if len(batch[topic]) >= BATCH_SIZE:
            insert_events(topic, batch[topic])
            print(f"Inserted {len(batch[topic])} events into {topic}")
            batch[topic] = []

if __name__ == '__main__':
    main()