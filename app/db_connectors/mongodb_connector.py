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