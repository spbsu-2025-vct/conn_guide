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