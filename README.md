# NYC Taxi Streaming Analytics

A real-time streaming data pipeline — **Kafka → MySQL → Grafana** — that
ingests NYC taxi trip events and visualizes live fleet operations metrics:
demand by zone, revenue, fares, and time-of-day patterns.

![Dashboard screenshot](docs/dashboard-screenshot.png)

## The problem this solves

Dispatch managers need to see demand *as it happens*, not in yesterday's
report. This pipeline simulates that: a fleet manager watching live pickup
demand by zone can reposition idle vehicles the moment demand starts
climbing in an area — say, a business district clearing out at 6 PM —
instead of finding out the next morning that a zone was under-served, after
riders already gave up and booked a competitor. The dashboard turns a
same-day miss into a same-minute save.

## What it does

- Streams NYC-taxi-style trip events (pickup/dropoff zone, fare, distance,
  payment type, timestamps) through **Apache Kafka** in real time
- A Python consumer writes every trip into **MySQL** as it arrives
- **Grafana** reads live from MySQL and renders 9 panels: total revenue,
  trip volume, top-demand zones, payment mix, fare by zone, and
  time-of-day demand patterns

## Architecture

```
trip_data.csv  --->  trip_producer.py  --->  Kafka (topic: trips)  --->  consumer.py  --->  MySQL  --->  Grafana
   (Faker-generated,         (Python/kafka-python)                    (Python/kafka-python +          (9 live panels)
    real NYC TLC schema)                                               mysql-connector)
```

## Dashboard panels

| Panel | Type | Insight |
|---|---|---|
| Total Revenue | Stat | Headline KPI |
| Total Trips | Stat | Headline KPI |
| Average Fare | Stat | Headline KPI |
| Active Pickup Zones | Stat | Headline KPI |
| Top 10 Pickup Zones by Trip Volume | Bar chart | Where demand concentrates |
| Revenue by Payment Type | Pie chart | Payment mix |
| Average Fare by Pickup Zone | Gauge | Most/least profitable zones |
| Trip Demand by Time of Day | Pie chart | Morning/afternoon/evening/night demand split |
| Average Trip Distance by Zone | Bar gauge | Short-haul vs. long-haul zones |

## Run it yourself

Requirements: Docker and Docker Compose.

```bash
git clone <this-repo-url>
cd <repo-folder>

# 1. Start the full stack (Kafka, Zookeeper, MySQL, Grafana)
docker-compose up -d

# 2. Set up a Python environment and install dependencies
python3 -m venv venv
source venv/bin/activate
pip install kafka-python mysql-connector-python faker

# 3. Generate sample trip data
python generate_data.py

# 4. In one terminal, start the consumer
python consumer.py

# 5. In another terminal, start the producer
python trip_producer.py
```

Then open **http://localhost:3002** (Grafana, login `admin` / `admin`) — the
MySQL data source and the full "NYC Taxi Streaming Analytics" dashboard are
auto-provisioned on startup, no manual configuration needed.

## Project structure

```
.
├── docker-compose.yml          # Kafka, Zookeeper, MySQL, Grafana — one command
├── generate_data.py            # Synthetic trip data generator (Faker)
├── trip_producer.py            # Kafka producer
├── consumer.py                 # Kafka consumer -> MySQL writer
├── db/
│   └── init.sql                # Auto-creates the trips table on first run
└── grafana/
    └── provisioning/
        ├── datasources/
        │   └── mysql.yml       # Auto-connects Grafana to MySQL
        └── dashboards/
            ├── provider.yml
            └── nyc-taxi-dashboard.json   # The full 9-panel dashboard
```

## Tech stack

Python · Apache Kafka · MySQL · Grafana · Docker & Docker Compose

## Notes

This project was built as Assignments 1–3 for a Streaming Data Analytics
course (industry/data-source identification, Kafka producer, and consumer +
dashboard respectively), then extended with Docker Compose and provisioning
config so the full pipeline is reproducible by anyone in under five minutes.
