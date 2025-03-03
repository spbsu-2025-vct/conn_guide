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