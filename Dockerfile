FROM python:3.7-slim

WORKDIR /app

COPY requirements.txt .

RUN pip3 install -r requirements.txt --no-cache-dir

COPY awesom_o.py .
COPY functions.py .
COPY texts_for_bot.py .
COPY statistic.bak .
COPY statistic.dat .
COPY statistic.dir .

CMD ["python3", "awesom_o.py"]
