FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN echo "v2" && pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
