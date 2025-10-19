



# 🧾 Hoja de Trabajo – Docker Compose: Flask + PostgreSQL
----
## 🎯 Objetivo
Aprender a construir y ejecutar una aplicación web multi-contenedor con **Docker Compose**, que integre:
- Una API simple en **Flask (Python)**
- Una base de datos **PostgreSQL** con volumen persistente

## 💡 Contexto
Tu equipo de desarrollo necesita desplegar una aplicación que almacene mensajes en una base de datos PostgreSQL.  
Como ingeniero DevOps, debes crear la configuración Docker necesaria para levantar toda la solución con un solo comando.

## 🧩 Estructura del Proyecto
```
docker-lab/
│
├── app.py
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

---

## 📁 1️⃣ app.py
```python
from flask import Flask, request
import psycopg2, os

app = Flask(__name__)

# Function to connect to PostgreSQL using environment variables
def get_conn():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
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
    cur.execute("SELECT * FROM mensajes;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return {'mensajes': rows}
```

---

## 📦 2️⃣ requirements.txt
```
Flask==3.0.0
psycopg2==2.9.9
```

---

## 🧱 3️⃣ Dockerfile
```dockerfile
# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy files
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# Expose Flask default port
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]
```

---

## ⚙️ 4️⃣ docker-compose.yml
```yaml
version: "3.9"

services:
  app:
    build: .
    container_name: flask-app
    ports:
      - "8080:5000"
    environment:
      # Environment variables for DB connection
      DB_HOST: db
      DB_NAME: mensajesdb
      DB_USER: admin
      DB_PASSWORD: admin123
    depends_on:
      - db
    restart: unless-stopped

  db:
    image: postgres:16
    container_name: postgres-db
    environment:
      # PostgreSQL default configuration
      POSTGRES_DB: mensajesdb
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: admin123
    volumes:
      - db_data:/var/lib/postgresql/data
    restart: unless-stopped

volumes:
  db_data:
```

---

## 🚀 Instrucciones

1. **Construye y ejecuta los servicios:**
   ```bash
   docker compose up -d
   ```

2. **Verifica los contenedores:**
   ```bash
   docker ps
   ```

3. **Prueba la aplicación:**
   ```bash
   # Verify connection to DB
   curl http://localhost:8080

   # Add a new message
   curl -X POST "http://localhost:8080/add?texto=HolaDocker"

   # List all messages
   curl http://localhost:8080/list
   ```

4. **Detén los contenedores y verifica persistencia:**
   ```bash
   docker compose down
   docker compose up -d
   curl http://localhost:8080/list
   ```

   Los mensajes deberían seguir existiendo gracias al volumen `db_data`.

---

## 📋 Criterios de Evaluación (100 pts)

| Criterio | Puntos |
|-----------|--------|
| Dockerfile funcional | 20 |
| `docker-compose.yml` correctamente configurado | 30 |
| Aplicación accede y guarda datos en PostgreSQL | 25 |
| Persistencia mediante volumen | 15 |
| Buenas prácticas y limpieza | 10 |

---

## 💬 Reflexión Final (opcional)

1. ¿Por qué es mejor usar variables de entorno que hardcodear credenciales?  
2. ¿Qué ventaja ofrece Docker Compose frente a ejecutar contenedores por separado?  
3. ¿Qué sucede si eliminas el volumen `db_data`?

---
