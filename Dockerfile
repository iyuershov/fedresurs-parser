FROM ubuntu:latest

RUN apt-get update -y && \
    apt-get install -y python3-dev && \
    apt-get install -y python3-pip


COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

ENV FLASK_APP routes.py
ENV FLASK_RUN_HOST 0.0.0.0
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN pip3 install -r requirements.txt

COPY . /app

CMD ["flask", "run"]
