from faker import Faker
from kafka import KafkaProducer
import json
import time
import random

fake = Faker()

producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

while True:
    dado = {
        "sensor_id": fake.uuid4(),
        "timestamp": fake.iso8601(),
        "temperatura": round(random.uniform(20.0, 30.0), 2),
        "umidade": round(random.uniform(30.0, 80.0), 2)
    }
    producer.send('iot_sensores', value=dado)
    print(f"[Producer] Enviado: {dado}")
    time.sleep(1)