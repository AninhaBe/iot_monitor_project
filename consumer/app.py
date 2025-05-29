import json
import os
import time
import csv
from datetime import datetime
from kafka import KafkaConsumer
import psycopg2
from dotenv import load_dotenv

load_dotenv()

KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "sensores")
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
EXPORT_FOLDER = os.getenv("EXPORT_FOLDER", "exports")

DB_NAME = os.getenv("DB_NAME", "sensores")
DB_USER = os.getenv("DB_USER", "user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_HOST = os.getenv("DB_HOST", "postgres")
DB_PORT = os.getenv("DB_PORT", "5432")

os.makedirs(EXPORT_FOLDER, exist_ok=True)

# Conexão com o banco
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS sensores (
    id SERIAL PRIMARY KEY,
    sensor_id VARCHAR(50),
    timestamp TIMESTAMP,
    temperatura FLOAT,
    umidade FLOAT,
    ingestion_date DATE
);
""")
conn.commit()

# Kafka consumer com tentativas
print("Tentando conectar ao Kafka...")

max_retries = 5
for attempt in range(1, max_retries + 1):
    try:
        consumer = KafkaConsumer(
            KAFKA_TOPIC,
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='sensor-group'
        )
        print("Conectado ao Kafka!")
        break
    except Exception as e:
        print(f"Tentativa {attempt}/{max_retries} falhou ao conectar ao Kafka: {e}")
        time.sleep(3)
else:
    print("Não foi possível conectar ao Kafka após várias tentativas. Encerrando.")
    exit(1)

print("Aguardando mensagens...")

for message in consumer:
    data = message.value
    sensor_id = data["sensor_id"]
    timestamp = data["timestamp"]
    temperatura = data["temperatura"]
    umidade = data["umidade"]
    ingestion_date = datetime.now().date()

    # Banco de dados
    cursor.execute(
        "INSERT INTO sensores (sensor_id, timestamp, temperatura, umidade, ingestion_date) VALUES (%s, %s, %s, %s, %s)",
        (sensor_id, timestamp, temperatura, umidade, ingestion_date)
    )
    conn.commit()

    # Arquivo CSV
    today_str = ingestion_date.isoformat()
    file_path = os.path.join(EXPORT_FOLDER, f"sensores_{today_str}.csv")
    file_exists = os.path.isfile(file_path)

    with open(file_path, mode="a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["sensor_id", "timestamp", "temperatura", "umidade", "ingestion_date"])
        writer.writerow([sensor_id, timestamp, temperatura, umidade, ingestion_date])

    print(f"[Consumer] Recebido: Sensor {sensor_id}, Temp: {temperatura}, Umid: {umidade}")
