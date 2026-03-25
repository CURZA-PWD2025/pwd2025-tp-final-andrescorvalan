#!/bin/bash
set -e  # Si algo falla, el script se detiene inmediatamente

echo "--- 1. Esperando conexión TCP con MySQL ($DB_HOST:3306) ---"

# Ejecuta sleep hasta que el comando de python tenga éxito
until python3 -c "import socket; s = socket.socket(); s.connect(('$DB_HOST', 3306))" 2>/dev/null; do
  echo "MySQL no responde en el puerto 3306... reintentando en 1s"
  sleep 1
done

echo "--- 2. Conexión establecida. Iniciando Servidor API ---"

exec gunicorn --bind 0.0.0.0:5000 run:app