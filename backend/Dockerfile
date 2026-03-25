FROM python:3.11-slim-bullseye

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

COPY start.sh . 
RUN chmod +x start.sh
CMD ["./start.sh"]