from kafka import KafkaConsumer
import psycopg2
import json
import time

consumer = KafkaConsumer(
    'iot_sensores',
    bootstrap_servers='kafka:9092',
    auto_offset_reset='earliest',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

time.sleep(10)

conn = psycopg2.connect(
    dbname="sensores",
    user="user",
    password="password",
    host="postgres",
    port="5432"
)
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS sensores (
        sensor_id TEXT,
        timestamp TEXT,
        temperatura REAL,
        umidade REAL
    )
''')
conn.commit()

for message in consumer:
    dado = message.value
    print(f"[Consumer] Recebido: {dado}")
    cursor.execute('''
        INSERT INTO sensores (sensor_id, timestamp, temperatura, umidade)
        VALUES (%s, %s, %s, %s)
    ''', (dado['sensor_id'], dado['timestamp'], dado['temperatura'], dado['umidade']))
    conn.commit()