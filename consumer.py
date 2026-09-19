import json
from kafka import KafkaConsumer
import mysql.connector

BOOTSTRAP_SERVERS = "localhost:9093"
TOPIC_NAME = "trips"

DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "admin",
    "database": "sda_assignment3",
}

def main():
    consumer = KafkaConsumer(
        TOPIC_NAME,
        bootstrap_servers=BOOTSTRAP_SERVERS,
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id="mysql-writer-group-v2",
    )

    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    insert_query = """
        INSERT INTO trips
        (trip_id, pickup_datetime, dropoff_datetime, pickup_zone, dropoff_zone,
         trip_distance, fare_amount, payment_type, passenger_count)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    print(f"Listening on topic '{TOPIC_NAME}' and writing to MySQL...")
    count = 0
    for message in consumer:
        row = message.value
        values = (
            int(row["trip_id"]),
            row["pickup_datetime"],
            row["dropoff_datetime"],
            row["pickup_zone"],
            row["dropoff_zone"],
            float(row["trip_distance"]),
            float(row["fare_amount"]),
            row["payment_type"],
            int(row["passenger_count"]),
        )
        cursor.execute(insert_query, values)
        conn.commit()
        count += 1
        print(f"Inserted trip_id={row['trip_id']} into MySQL (total: {count})")

if __name__ == "__main__":
    main()
