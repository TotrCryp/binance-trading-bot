FROM python:3.11-slim
LABEL authors="Totr"

WORKDIR /app

COPY . /app

RUN mkdir -p db/databases

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
