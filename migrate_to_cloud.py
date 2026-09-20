import mysql.connector

local_conn = mysql.connector.connect(
    host='localhost', port=3306, user='root', password='admin', database='sda_assignment3'
)
local_cursor = local_conn.cursor()
local_cursor.execute('SELECT trip_id, pickup_datetime, dropoff_datetime, pickup_zone, dropoff_zone, trip_distance, fare_amount, payment_type, passenger_count FROM trips')
rows = local_cursor.fetchall()
print(f'Fetched {len(rows)} rows from local MySQL.')
local_cursor.close()
local_conn.close()

try:
    cloud_conn = mysql.connector.connect(
        host='sda-taxi-db-sda-taxi-project.b.aivencloud.com',
        port=26509, user='avnadmin', password='YOUR_AIVEN_PASSWORD_HERE',
        database='defaultdb', ssl_disabled=False
    )
    cloud_cursor = cloud_conn.cursor()
    insert_query = '''
        INSERT INTO trips
        (trip_id, pickup_datetime, dropoff_datetime, pickup_zone, dropoff_zone,
         trip_distance, fare_amount, payment_type, passenger_count)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
    batch_size = 200
    total_inserted = 0
    for i in range(0, len(rows), batch_size):
        batch = rows[i:i+batch_size]
        cloud_cursor.executemany(insert_query, batch)
        cloud_conn.commit()
        total_inserted += len(batch)
        print(f'Inserted {total_inserted} / {len(rows)} rows so far...')
    print('DONE. Total inserted:', total_inserted)
    cloud_cursor.close()
    cloud_conn.close()
except Exception as e:
    print('ERROR during cloud insert:', e)
