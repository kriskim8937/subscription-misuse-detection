import json
import time
import psycopg2
from kafka import KafkaConsumer
from psycopg2.extras import execute_values

# Kafka setup
KAFKA_TOPIC = 'user_activity'
KAFKA_BOOTSTRAP_SERVERS = 'localhost:9092'

# Postgres setup
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'dbname': 'streaming',
    'user': 'postgres',
    'password': 'postgres'  # change this if needed
}

# Connect to Postgres
def get_pg_conn():
    return psycopg2.connect(**DB_CONFIG)

# Insert events into Postgres
def insert_events(events):
    if not events:
        return

    with get_pg_conn() as conn:
        with conn.cursor() as cur:
            execute_values(
                cur,
                """
                INSERT INTO raw_user_activity (user_id, device_id, ip_location, timestamp)
                VALUES %s
                """,
                [(e['user_id'], e['device_id'], e['ip_location'], time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(e['timestamp']))) for e in events]
            )
        conn.commit()

def ensure_table_exists():
    create_sql = """
    CREATE TABLE IF NOT EXISTS raw_user_activity (
        user_id TEXT,
        device_id TEXT,
        ip_location TEXT,
        timestamp TIMESTAMP
    );
    """
    with get_pg_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(create_sql)
        conn.commit()

def main():
    print("Ensuring table exists...")
    ensure_table_exists()
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    batch = []
    BATCH_SIZE = 10

    for msg in consumer:
        batch.append(msg.value)
        print(f"Consumed: {msg.value}")

        if len(batch) >= BATCH_SIZE:
            insert_events(batch)
            print(f"Inserted {len(batch)} events into Postgres")
            batch = []

if __name__ == '__main__':
    main()
