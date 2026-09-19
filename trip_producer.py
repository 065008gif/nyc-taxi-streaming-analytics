import csv
import json
import time
from kafka import KafkaProducer

BOOTSTRAP_SERVERS = "localhost:9093"
TOPIC_NAME = "trips"
DATA_FILE = "trip_data.csv"
DELAY_SECONDS = 1  # simulated real-time gap between events

def main():
    producer = KafkaProducer(
        bootstrap_servers=BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )

    with open(DATA_FILE, newline="") as f:
        reader = csv.DictReader(f)
        count = 0
        for row in reader:
            producer.send(TOPIC_NAME, value=row)
            count += 1
            print(f"Sent: {row}")
            time.sleep(DELAY_SECONDS)

    producer.flush()
    print(f"Finished sending {count} messages to topic '{TOPIC_NAME}'.")

if __name__ == "__main__":
    main()
