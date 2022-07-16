FROM python:3.7-slim

WORKDIR /awesom_o

COPY requirements.txt .

RUN pip3 install -r requirements.txt --no-cache-dir

COPY code/ .

CMD ["python3", "awesom_o.py"]
