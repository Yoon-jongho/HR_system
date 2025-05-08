FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y default-mysql-client

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chmod +x /app/wait-for-db.sh

CMD ["/app/wait-for-db.sh", "db", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]