FROM ubuntu:latest

RUN apt-get update -y && \
    apt-get install -y python3-dev && \
    apt-get install -y python3-pip && \
    apt-get install -y firefox

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

WORKDIR /fedresurs

COPY requirements.txt ./

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . ./app