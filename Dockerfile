FROM python:3.11-alpine

WORKDIR /usr/src/app/anfeb

COPY ./requirements.txt /usr/src/app/anfeb
RUN pip install -r /usr/src/app/anfeb/requirements.txt
COPY ./bot /usr/src/app/anfeb/bot
COPY ./module /usr/src/app/anfeb/module
COPY ./main.py /usr/src/app/anfeb