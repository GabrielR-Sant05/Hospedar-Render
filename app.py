from flask import Flask, request, jsonify
import psycopg2
from threading import Thread
import time

app = Flask(__name__)

# Configuração do banco de dados
DB_CONFIG = {
    'dbname': 'default_db',
    'user': 'default_user',
    'password': 'default_password',
    'host': 'db',  # Nome do serviço no docker-compose
    'port': '5432'
}

# Conexão com o banco de dados
def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

# Rota base para informações da API
@app.route('/', methods=['GET'])
def index():
    return jsonify({
        'message': 'Welcome to the API! Use GET /api/items to retrieve all items.'
    }), 200

@app.route('/api/items', methods=['POST'])
def create_item():
    data = request.json
    name = data.get('name')
    if not name:
        return jsonify({'error': 'Name is required'}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO items (name) VALUES (%s) RETURNING id;", (name,))
    item_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'id': item_id, 'name': name}), 201

@app.route('/api/items', methods=['GET'])
def get_items():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM items;")
    items = [{'id': row[0], 'name': row[1]} for row in cur.fetchall()]
    cur.close()
    conn.close()
    return jsonify(items), 200

@app.route('/api/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.json
    name = data.get('name')
    if not name:
        return jsonify({'error': 'Name is required'}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE items SET name = %s WHERE id = %s;", (name, item_id))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'id': item_id, 'name': name}), 200

@app.route('/api/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM items WHERE id = %s;", (item_id,))
    conn.commit()
    cur.close()
    conn.close()
    return '', 204

# Keep-alive para evitar que a aplicação caia
def keep_alive():
    while True:
        time.sleep(300)  # 5 minutos
        with app.test_request_context('/'):
            app.preprocess_request()

if __name__ == '__main__':
    # Iniciar o keep-alive em uma thread separada
    Thread(target=keep_alive, daemon=True).start()
    app.run(host='0.0.0.0', port=8080)
