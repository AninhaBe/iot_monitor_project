FROM python:3.9

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y netcat-openbsd && \
    pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN chmod +x wait-for-services.sh

CMD ["./wait-for-services.sh", "python", "app.py"]
