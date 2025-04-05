import psycopg2
import os
from datetime import datetime, timedelta

# Database connection parameters
DB_PARAMS = {
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "database": os.getenv("POSTGRES_DB", "streaming"),
    "user": os.getenv("POSTGRES_USER", "postgres"),
    "password": os.getenv("POSTGRES_PASSWORD", "postgres"),
    "port": 5432,
}

def get_connection():
    """Establish a connection to the PostgreSQL database."""
    return psycopg2.connect(**DB_PARAMS)

def fetch_user_activity():
    """Fetch user activity data from the clean_user_activity table."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT user_id, device_id, ip_location, timestamp
        FROM clean_user_activity
    """)
    
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def flag_users(user_activities):
    """Flag users based on defined rules."""
    flagged_users = []
    now = datetime.now()

    # Define the time threshold (1 hour)
    time_threshold = timedelta(hours=1)

    # Create a dictionary to track user activity
    user_activity_dict = {}

    for activity in user_activities:
        user_id, device_id, ip_location, timestamp = activity

        # timestamp is already a datetime object; no need for conversion
        if user_id not in user_activity_dict:
            user_activity_dict[user_id] = []

        user_activity_dict[user_id].append((ip_location, timestamp))

    # Apply rule: flag users with activity from 3+ unique locations within 1 hour
    for user_id, activities in user_activity_dict.items():
        activities.sort(key=lambda x: x[1])  # Sort by timestamp
        unique_locations = set()
        activity_time_frame = []

        for ip_location, timestamp in activities:
            # Collect unique locations and timestamps within the last hour
            if (now - timestamp) <= time_threshold:
                unique_locations.add(ip_location)
                activity_time_frame.append(timestamp)

        if len(unique_locations) >= 3:
            flagged_users.append((user_id, "Multiple locations in a short time"))

    return flagged_users

def insert_flagged_users(flagged_users):
    """Insert flagged users into the flagged_users table."""
    conn = get_connection()
    cursor = conn.cursor()

    for user_id, reason in flagged_users:
        cursor.execute("""
            INSERT INTO flagged_users (user_id, reason)
            VALUES (%s, %s)
            ON CONFLICT (user_id) DO NOTHING
        """, (user_id, reason))

    conn.commit()
    cursor.close()
    conn.close()

def main():
    user_activities = fetch_user_activity()
    flagged_users = flag_users(user_activities)
    insert_flagged_users(flagged_users)

    if flagged_users:
        print(f"Flagged {len(flagged_users)} users:")
        for user_id, reason in flagged_users:
            print(f" - User ID: {user_id}, Reason: {reason}")
    else:
        print("No users flagged.")

if __name__ == "__main__":
    main()
