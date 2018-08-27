FROM python:alpine

# bash
RUN apk update
RUN apk upgrade
RUN apk add bash

COPY python-req.txt /challenge_framework_build/req.txt
RUN pip install -r /challenge_framework_build/req.txt

EXPOSE 8000
