#!/bin/sh

echo "Aguardando Kafka em $KAFKA_BOOTSTRAP_SERVERS ..."
KAFKA_HOST=$(echo "$KAFKA_BOOTSTRAP_SERVERS" | cut -d':' -f1)
KAFKA_PORT=$(echo "$KAFKA_BOOTSTRAP_SERVERS" | cut -d':' -f2)
while ! nc -z "$KAFKA_HOST" "$KAFKA_PORT"; do
  echo "$(date) :: Kafka ainda não está pronto ..."
  sleep 1
done
echo "Kafka está pronto!"

echo "Iniciando aplicação..."
exec "$@"
