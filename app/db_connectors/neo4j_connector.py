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