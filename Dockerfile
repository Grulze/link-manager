FROM python:3.13-alpine

RUN mkdir /dream_job

WORKDIR /dream_job

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
