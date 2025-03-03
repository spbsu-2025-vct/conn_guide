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