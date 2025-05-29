# Monitoramento de Sensores IoT (com Kafka + PostgreSQL + Docker)

Este projeto simula um sistema de monitoramento de sensores IoT. Ele envia dados em tempo real via Kafka e armazena esses dados em um banco de dados para posterior análise.

---

## Objetivo

Desenvolver uma solução de streaming que:

- Gere dados fictícios de sensores (temperatura e umidade)
- Envie esses dados para um tópico Kafka usando um **Producer**
- Consuma os dados desse tópico usando um **Consumer**
- Armazene os dados recebidos em um banco de dados relacional (PostgreSQL)

---

## Arquitetura

```
+------------+          Kafka         +-------------+         PostgreSQL
|  Producer  | ───────────────▶──────▶ |  Consumer   | ───────▶  sensores.db
+------------+                       +-------------+          
      ▲                                     ▲
      |                                     |
    faker                             kafka-python
```

- O **Producer** usa a biblioteca `faker` para gerar dados aleatórios.
- O **Consumer** consome do tópico Kafka e armazena no banco.
- Tudo roda dentro de containers usando Docker Compose.

---

## Lógica do Sistema

- A cada 1 segundo, o `Producer` gera um novo dado com:
  - sensor_id: UUID do sensor
  - timestamp: Data e hora de leitura
  - temperatura: valor entre 20.0°C e 30.0°C
  - umidade: valor entre 30% e 80%

- O dado é enviado para o tópico `iot_sensores`.

- O `Consumer` consome as mensagens do tópico e:
  - Cria a tabela `sensores` (caso não exista)
  - Insere os dados no PostgreSQL com persistência

---

## Tecnologias Utilizadas

| Componente      | Tecnologia              |
|-----------------|--------------------------|
| Linguagem       | Python 3.9               |
| Mensageria      | Apache Kafka + Zookeeper |
| Banco de Dados  | PostgreSQL 13            |
| Geração de Dados| faker                    |
| Conectores      | kafka-python, psycopg2   |
| Containerização | Docker + Docker Compose  |
| Gerenciador     | Poetry (pyproject.toml)  |

---

## Estrutura de Pastas

iot_monitor_project/  
├── docker-compose.yml  
├── producer/  
│   ├── app.py  
│   ├── Dockerfile  
│   └── pyproject.toml  
├── consumer/  
│   ├── app.py  
│   ├── Dockerfile  
│   └── pyproject.toml  
├── data_export.py  ← script de exportação para CSV/Excel  

---

## ▶Como executar

1. Clonar o repositório:

```
git clone <repo-url>
cd iot_monitor_project
```

2. Subir os containers:

```
docker-compose up --build -d
```

3. Ver logs (opcional):

```
docker-compose logs -f producer
docker-compose logs -f consumer
```

---

## Exportar dados do banco

Use o script incluído para exportar os dados para `.csv` e `.xlsx`:

```
python data_export.py
```

Gera:

- sensores_exportado.csv  
- sensores_exportado.xlsx

---

## Exemplos de Dados

```json
{
  "sensor_id": "123e4567-e89b-12d3-a456-426614174000",
  "timestamp": "2025-05-29T00:12:34",
  "temperatura": 27.6,
  "umidade": 52.3
}
```

---

## Segurança e Resiliência

- Containers com `restart: always` para tolerância a falhas  
- Isolamento de dependências com Poetry  
- Banco persistente com volume Docker

---

## Possíveis Extensões

- Adicionar Streamlit para visualizar gráficos em tempo real  
- Incluir alertas (ex: se temperatura > 30°C)  
- Salvar históricos diários em arquivos  
- Migrar Kafka para serviço em nuvem (MSK, Confluent Cloud, etc)

---

## Autor

Desenvolvido por **Ana Beatriz**  
Email: contato.anabeatrizoliver@gmail.com  
