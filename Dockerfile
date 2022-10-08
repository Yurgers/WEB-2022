#syntax=docker/dockerfile:1
FROM python:3.10

LABEL version="0.1"

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip  &&  pip install -r requirements.txt

COPY src src
COPY service service
COPY run.py run.py

CMD [ "python", "run.py" ]
