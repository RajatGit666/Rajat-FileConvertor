# Python ka halka version load karo
FROM python:3.9-slim

# Server mein LibreOffice install karo (yahi file convert karega)
RUN apt-get update && apt-get install -y libreoffice

# App ke liye folder banao
WORKDIR /app

# Requirements install karo
COPY requirements.txt .
RUN pip install -r requirements.txt

# Baaki saara code copy karo
COPY . .

# Server start karne ki command
CMD gunicorn app:app --bind 0.0.0.0:$PORT
