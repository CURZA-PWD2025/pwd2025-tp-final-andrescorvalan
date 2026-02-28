#!/bin/bash

# Este script espera a que el servicio 'db' esté listo antes de continuar.

DB_HOST=$DB_HOST
DB_PORT=3306 # El puerto interno de MySQL es siempre 3306

echo "--- 1. Esperando a la base de datos MySQL en $DB_HOST:$DB_PORT ---"

# Bucle de espera (intenta conectar cada 1 segundo, máximo 30 intentos)
count=0
max_attempts=30
while ! python -c "import socket; s = socket.socket(socket.AF_INET, socket.SOCK_STREAM); s.connect(('$DB_HOST', $DB_PORT))" 2>/dev/null; do
  count=$((count + 1))
  if [ $count -ge $max_attempts ]; then
    echo "ERROR: Falló la conexión a MySQL después de $max_attempts segundos."
    exit 1
  fi
  echo "MySQL aún no está disponible (Intento $count/$max_attempts). Esperando 1 segundo..."
  sleep 1
done

echo "--- MySQL está listo. Procediendo con la inicialización. ---"

# 2. Inicializar la DB (creación de tablas/datos de ejemplo)
# /usr/bin/env python db_init.py

# 3. Iniciar el servidor Flask
#flask run --host=0.0.0.0
python run.py