# Тест соединений к разным БД

Проект написан на языке `python` с применением микрофреймворка `Flask`. 

Перед началом работы с проектом создайте контейнеры с различными БД (например, взяв `docker-compose.yml` с предыдущего практического занятия).

```yml
version: '3'

services:
  postgres:
    image: postgres:14
    ports: ["5432:5432"]
    environment:
      POSTGRES_PASSWORD: postgres

  mariadb:
    image: mariadb:10.6
    ports: ["3306:3306"]
    environment:
      MYSQL_ROOT_PASSWORD: root

  neo4j:
    image: neo4j:4.4
    ports: ["7474:7474", "7687:7687"]
    environment:
      NEO4J_AUTH: neo4j/password

  mongodb:
    image: mongo:6.0
    ports: ["27017:27017"]

  clickhouse:
    image: clickhouse/clickhouse-server:23.3
    ports: ["8123:8123", "9000:9000"]

  flask_app:
    build: .
    ports: ["5000:5000"]
    environment:
      FLASK_ENV: dev
    depends_on:
      - postgres
      - mariadb
      - neo4j
      - mongodb
      - clickhouse
```

После этого:

### 1. Создайте файл `config.yaml` с параметрами соединения:

```yaml
databases:
  postgres:
    host: postgres
    port: 5432
    user: postgres
    password: postgres
    dbname: postgres

  mariadb:
    host: mariadb
    port: 3306
    user: root
    password: root
    dbname: mysql

  neo4j:
    host: neo4j
    port: 7687
    user: neo4j
    password: password

  mongodb:
    host: mongodb
    port: 27017
    dbname: test

  clickhouse:
    host: clickhouse
    port: 9000
    user: default
    password: ""
    dbname: default
```

### 2. В проекте уже задан файл `requirements.txt` с версиями нужных библиотек для виртуального окружения.

```txt
Flask==2.3.2
psycopg2-binary==2.9.6
mysql-connector-python==8.0.33
neo4j==5.8.0
pymongo==4.3.3
clickhouse-driver==0.2.4
```

### 3. `app/__init__.py`

```python
from flask import Flask
import yaml

app = Flask(__name__)

# Чтение config-файла
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

app.config['DATABASES'] = config['databases']

from app.routes import *
```

### 4. `app/routes.py`

```python
from flask import Flask, jsonify
from app.db_connectors import (
    postgres_connector, mariadb_connector, 
    neo4j_connector, mongodb_connector, clickhouse_connector
)

@app.route('/test_all', methods=['GET'])
def test_all():
    results = {}
    results['postgres'] = postgres_connector.test_connection()
    results['mariadb'] = mariadb_connector.test_connection()
    results['neo4j'] = neo4j_connector.test_connection()
    results['mongodb'] = mongodb_connector.test_connection()
    results['clickhouse'] = clickhouse_connector.test_connection()
    return jsonify(results)
```

### 5. `app/db_connectors/postgres_connector.py`

```python
import psycopg2
from app import app

def test_connection():
    config = app.config['DATABASES']['postgres']
    try:
        conn = psycopg2.connect(
            host=config['host'],
            port=config['port'],
            user=config['user'],
            password=config['password'],
            dbname=config['dbname']
        )
        cursor = conn.cursor()
        cursor.execute("SELECT 1;")
        return {"status": "success", "message": "Connection successful"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
```

### 6. `app/db_connectors/mariadb_connector.py`

```python
import mysql.connector
from app import app

def test_connection():
    config = app.config['DATABASES']['mariadb']
    try:
        conn = mysql.connector.connect(
            host=config['host'],
            port=config['port'],
            user=config['user'],
            password=config['password'],
            database=config['dbname']
        )
        cursor = conn.cursor()
        cursor.execute("SELECT 1;")
        return {"status": "success", "message": "Connection successful"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
```

### 7. `app/db_connectors/neo4j_connector.py`

```python
from neo4j import GraphDatabase
from app import app

def test_connection():
    config = app.config['DATABASES']['neo4j']
    try:
        driver = GraphDatabase.driver(
            f"bolt://{config['host']}:{config['port']}",
            auth=(config['user'], config['password'])
        )
        with driver.session() as session:
            session.run("RETURN 1;")
        return {"status": "success", "message": "Connection successful"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
```

### 8. `app/db_connectors/mongodb_connector.py`

```python
from pymongo import MongoClient
from app import app

def test_connection():
    config = app.config['DATABASES']['mongodb']
    try:
        client = MongoClient(
            host=config['host'],
            port=config['port']
        )
        db = client[config['dbname']]
        db.command('ping')
        return {"status": "success", "message": "Connection successful"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
```

### 9. `app/db_connectors/clickhouse_connector.py`

```python
from clickhouse_driver import Client
from app import app

def test_connection():
    config = app.config['DATABASES']['clickhouse']
    try:
        client = Client(
            host=config['host'],
            port=config['port'],
            user=config['user'],
            password=config['password'],
            database=config['dbname']
        )
        client.execute("SELECT 1;")
        return {"status": "success", "message": "Connection successful"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
```

### 10. `Dockerfile` для Flask приложения

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
```

### Запуск проекта

1. Соберите и запустите контейнеры:
   ```bash
   docker-compose up --build
   ```

2. После запуска, Flask приложение будет доступно по адресу `http://localhost:5000`. 

3. Для проверки подключения ко всем базам данных, выполните запрос:
   ```bash
   curl http://localhost:5000/test_all
   ```

   В ответе вы получите JSON с результатами подключения к каждой из баз данных.

Этот пример демонстрирует, как можно организовать подключение к различным типам баз данных с использованием Flask и конфигурационного файла.