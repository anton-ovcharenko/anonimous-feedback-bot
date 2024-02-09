FROM python:3.11-alpine

WORKDIR /usr/src/app/anfeb

COPY requirements.txt .
RUN pip install -r ./requirements.txt
COPY bot ./bot
COPY module ./module
COPY *.py .

CMD ["python3", "main.py"]