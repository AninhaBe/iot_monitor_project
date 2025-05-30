# IoT Sensor Monitoring System

Este projeto é um sistema completo de **monitoramento de sensores IoT**, que simula o envio de dados em tempo real usando Kafka, armazena essas informações em um banco de dados PostgreSQL (Render) e disponibiliza os dados para análise.

---

## Visão Geral

O sistema é dividido em **quatro partes principais**:

1. **Producer**: Gera dados falsos de sensores (com a biblioteca `faker`) e envia para um tópico Kafka.
2. **Kafka + Zookeeper**: Orquestram a comunicação entre producer e consumer.
3. **Consumer**: Consome dados do tópico Kafka, processa e armazena no banco PostgreSQL.
4. **Exportação CSV**: Os dados também são salvos em arquivos `.csv` diários em uma pasta `exports/`.

---

## Estrutura do Projeto

```
iot_monitor_project/
│
├── consumer/
│   ├── app.py
│   ├── pyproject.toml
│   ├── Dockerfile
│   └── wait-for-services.sh
│
├── producer/
│   ├── app.py
│   ├── pyproject.toml
│   ├── Dockerfile
│   └── wait-for-services.sh
│
├── exports/
│   └── sensores_YYYY-MM-DD.csv  # Exportação local dos dados
│
├── docker-compose.yml
├── .env
└── README.md
```

---

## Arquitetura

```
         +-----------+        Kafka         +-----------+         +----------------+
         | Producer  |  ----------------->  | Consumer  |  ----->  | PostgreSQL (☁️)|
         +-----------+                     +-----------+         +----------------+
                                                                  |   Render.com   |
                                                                  +----------------+

             ▲                                  ▲
             |                                  |
           faker                   kafka-python + CSV export
```

---

## Tecnologias Utilizadas

- **Python 3.9**
- **Kafka + Zookeeper (Confluent)**
- **PostgreSQL 13 (Render)**
- **Poetry** para dependências
- **Faker** para simular sensores
- **Docker & Docker Compose**

---

## Como Executar Localmente

### 1. Pré-requisitos

- Docker e Docker Compose instalados
- Conta na [Render](https://render.com) com banco PostgreSQL configurado

### 2. Clonar o projeto

```bash
git clone https://github.com/seu-usuario/iot_monitor_project.git
cd iot_monitor_project
```

### 3. Criar o `.env`

Crie um arquivo `.env` com o seguinte conteúdo:

```env
DB_NAME=sensores_vncw
DB_USER=user
DB_PASSWORD=sua_senha_aqui
DB_HOST=seu_host.render.com
DB_PORT=5432

KAFKA_BOOTSTRAP_SERVERS=kafka:9092
KAFKA_TOPIC=sensores
EXPORT_FOLDER=exports
```

> Aqui são dados simulados, substitua os dados com os fornecidos pela Render

---

### 4. Subir os containers

```bash
docker-compose up --build
```

Isso vai iniciar:
- Kafka
- Zookeeper
- Producer (simulando sensores)
- Consumer (armazenando e exportando dados)

---

## Como visualizar os dados

1. Acesse o banco via **DBeaver** (ou pgAdmin):
   - Use os dados da Render (host, user, db, password)
   - A tabela se chama `sensores`

2. Execute:

```sql
SELECT * FROM sensores ORDER BY timestamp DESC LIMIT 10;
```

3. Veja os arquivos `.csv` sendo criados em `/exports/`.

---

## Para parar tudo

```bash
docker-compose down
```

---

## Observações

- Os dados são fictícios (temperatura, umidade, sensor_id)
- Os containers são reiniciáveis e independentes
- O banco local (`postgres`) foi removido em favor da nuvem (Render)

---

## Dev

Desenvolvido por **Ana Beatriz**  
contato.anabeatrizoliver@gmail.com

---

## Licença

MIT