from flask import Flask, request, jsonify # type: ignore
import psycopg2 # type: ignore
import os

app = Flask(__name__)


# Function to connect to PostgreSQL using environment variables
def get_conn():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME", "mensajesdb"),
        user=os.getenv("DB_USER", "admin"),
        password=os.getenv("DB_PASSWORD", "admin123")
    )


@app.route('/')
def index():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS mensajes (id SERIAL PRIMARY KEY, texto VARCHAR(100));")
    conn.commit()
    cur.close()
    conn.close()
    return "App connected to PostgreSQL ✅"


@app.route('/add', methods=['POST'])
def add():
    texto = request.args.get('texto', 'Sin mensaje')
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO mensajes (texto) VALUES (%s);", (texto,))
    conn.commit()
    cur.close()
    conn.close()
    return f"Message added: {texto}"


@app.route('/list')
def list_msg():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, texto FROM mensajes ORDER BY id;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    # Convert rows to list of dicts for JSON friendliness
    mensajes = [{'id': r[0], 'texto': r[1]} for r in rows]
    return jsonify({'mensajes': mensajes})


if __name__ == '__main__':
    # Run on 0.0.0.0 so container can map ports
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
