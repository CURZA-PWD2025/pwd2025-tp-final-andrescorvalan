FROM python:3.11-slim-bullseye

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY start.sh . 
RUN chmod +x start.sh

# Copiar el resto del código de la aplicación
#COPY . .

#COPY app/ app/
#COPY run.py .   
#COPY db_init.py .
#COPY db_rollback.py .

#ENV FLASK_APP=run.py

EXPOSE 5000

# Comando que se ejecutará al iniciar el contenedor
#CMD ["bash", "-c", "/usr/bin/env python db_init.py && flask run --host=0.0.0.0"]


#CMD ["bash", "-c", "/usr/bin/env python db_init.py && flask run --host=0.0.0.0"]

#command: ["./start.sh"]
