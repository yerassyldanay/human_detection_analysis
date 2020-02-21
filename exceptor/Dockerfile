FROM python:latest

RUN pip3 install pytelegrambotapi
RUN pip3 install redis

ADD exceptor.py /
ADD constants.py /

WORKDIR /