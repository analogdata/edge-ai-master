# Simple Dockerfile for the volume persistence demo
FROM python:3.11-slim

WORKDIR /app
COPY app.py .

ENV DATA_FILE=/data/counter.txt

CMD ["python3", "app.py"]
