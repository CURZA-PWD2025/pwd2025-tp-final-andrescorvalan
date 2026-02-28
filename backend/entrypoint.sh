#!/bin/sh

# ====================================================
# ESPERAR A QUE LA BASE DE DATOS ESTÉ LISTA
# ====================================================
echo "Esperando que la base de datos MySQL esté disponible..."
# Este bucle verifica continuamente la conexión a la DB
while ! timeout 1 bash -c "echo > /dev/tcp/$DB_HOST/$DB_PORT"; do
  echo "MySQL aún no está listo. Reintentando en 1 segundo..."
  sleep 1
done
echo "MySQL está disponible. Iniciando inicialización de DB..."

# ====================================================
#  INICIALIZAR LA BASE DE DATOS
# ====================================================
echo "Ejecutando script de inicialización db_init.py..."
python db_init.py

# ====================================================
# 3. INICIAR EL SERVIDOR FLASK
# ====================================================
# Una vez completada la inicialización, inicia el servidor de producción Gunicorn.
# 'exec' reemplaza el proceso actual del shell, lo que es una buena práctica Docker.
echo "Iniciando servidor Gunicorn..."
exec gunicorn --bind 0.0.0.0:5000 run:app