FROM ubuntu:latest

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev python3-setuptools make git git-core \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

ENV PYTHONUNBUFFERED=1
ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0:7000

FROM tensorflow/tensorflow:latest-gpu

WORKDIR /code

RUN apt-get update && apt-get -y install python3-pip
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . /code
