-- Auto-run on first container startup (MYSQL_DATABASE already creates sda_assignment3)
USE sda_assignment3;

CREATE TABLE IF NOT EXISTS trips (
    trip_id INT,
    pickup_datetime DATETIME,
    dropoff_datetime DATETIME,
    pickup_zone VARCHAR(100),
    dropoff_zone VARCHAR(100),
    trip_distance FLOAT,
    fare_amount FLOAT,
    payment_type VARCHAR(50),
    passenger_count INT
);
