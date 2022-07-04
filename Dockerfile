FROM python:3.7-slim

WORKDIR /awesom_o

COPY requirements.txt .

RUN pip3 install -r requirements.txt --no-cache-dir

COPY code/ .

# без этого бот не запустится автоматом. Попробовать вручную внутри контейнера через удалённый обозреватель!
CMD ["python3", "awesom_o.py"]


# подключить ТОМ
# сделать COPY .env . -> без этого же не запустится?!
