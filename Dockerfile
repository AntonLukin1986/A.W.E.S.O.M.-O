FROM python:3.7-slim

WORKDIR /awesom_o_bot

COPY requirements.txt .

RUN pip3 install -r requirements.txt --no-cache-dir

COPY awesom_o/ .

CMD ["python3", "awesom_o.py"]
