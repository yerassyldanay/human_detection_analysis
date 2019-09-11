FROM ubuntu:latest

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev python3-setuptools make git git-core \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

ENV PYTHONUNBUFFERED=1

FROM tensorflow/tensorflow:latest-gpu

RUN mkdir human_detection
ADD . /human_detection

WORKDIR human_detection

RUN apt-get update && apt-get -y install python3-pip
RUN pip3 install -r requirements.txt
