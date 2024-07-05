# syntax=docker/dockerfile:1

FROM python:3.10-slim-bullseye

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6 libxrender-dev -y

COPY requirements.txt requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
RUN pip install gunicorn pymysql

COPY app app
COPY migrations migrations
COPY study.py config.py boot.sh ./
RUN chmod a+x boot.sh

ENV FLASK_APP study.py

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
