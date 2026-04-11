FROM python:3.11-slim

WORKDIR /app
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chmod +x scripts/wait_for_postgres.py

CMD ["python", "scripts/wait_for_postgres.py", "flask", "run", "--host=0.0.0.0"]
