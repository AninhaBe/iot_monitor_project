from faker import Faker
from kafka import KafkaProducer
import json
import time
import random
import os
from dotenv import load_dotenv

load_dotenv()

KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "sensores")
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")

fake = Faker()

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

while True:
    dado = {
        "sensor_id": fake.uuid4(),
        "timestamp": fake.iso8601(),
        "temperatura": round(random.uniform(20.0, 30.0), 2),
        "umidade": round(random.uniform(30.0, 80.0), 2)
    }
    producer.send(KAFKA_TOPIC, value=dado)
    print(f"[Producer] Enviado: {dado}")
    time.sleep(1)
