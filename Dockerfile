FROM python:3.9-slim
LABEL authors="Totr"

WORKDIR /btb_app

RUN apt-get update && \
    apt-get install -y git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/TotrCryp/binance-trading-bot.git /btb_app

RUN mkdir -p db/databases

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "main.py"]

CMD ["-S", "BTCUSDT", "--mode", "test", "-u"]
