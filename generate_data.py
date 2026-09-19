import csv
import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()
Faker.seed(42)
random.seed(42)

NUM_ROWS = 1000

# NYC-style taxi zones (subset of real TLC zone names, for realism)
ZONES = [
    "Upper East Side North", "Upper East Side South", "Midtown Center",
    "Midtown East", "Times Sq/Theatre District", "East Village",
    "West Village", "Financial District North", "Financial District South",
    "Harlem North", "Harlem South", "Astoria", "Long Island City/Queens Plaza",
    "JFK Airport", "LaGuardia Airport", "Williamsburg (North Side)",
    "Williamsburg (South Side)", "Greenwich Village North", "SoHo",
    "Chelsea", "Gramercy", "Bushwick North", "Park Slope", "Brooklyn Heights",
]

PAYMENT_TYPES = ["Credit Card", "Cash", "Mobile Wallet"]

def generate_trip(trip_id):
    pickup_zone = random.choice(ZONES)
    dropoff_zone = random.choice([z for z in ZONES if z != pickup_zone])

    pickup_dt = datetime.now() - timedelta(
        hours=random.randint(0, 23), minutes=random.randint(0, 59)
    )
    trip_minutes = random.randint(4, 45)
    dropoff_dt = pickup_dt + timedelta(minutes=trip_minutes)

    trip_distance = round(random.uniform(0.5, 18.0), 2)
    base_fare = 3.0 + trip_distance * random.uniform(2.0, 3.5)
    fare_amount = round(base_fare, 2)

    return {
        "trip_id": trip_id,
        "pickup_datetime": pickup_dt.strftime("%Y-%m-%d %H:%M:%S"),
        "dropoff_datetime": dropoff_dt.strftime("%Y-%m-%d %H:%M:%S"),
        "pickup_zone": pickup_zone,
        "dropoff_zone": dropoff_zone,
        "trip_distance": trip_distance,
        "fare_amount": fare_amount,
        "payment_type": random.choice(PAYMENT_TYPES),
        "passenger_count": random.randint(1, 4),
    }

def main():
    rows = [generate_trip(i + 1) for i in range(NUM_ROWS)]

    fieldnames = list(rows[0].keys())
    with open("trip_data.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Generated {NUM_ROWS} trip records -> trip_data.csv")

if __name__ == "__main__":
    main()
