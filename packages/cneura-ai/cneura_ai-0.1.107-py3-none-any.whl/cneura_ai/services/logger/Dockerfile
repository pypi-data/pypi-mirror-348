FROM python:3.12-slim

WORKDIR /app

RUN pip install --upgrade pip 

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/app

CMD ["python", "main.py"]
