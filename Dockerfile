FROM python:3.6.5-alpine3.7

WORKDIR /localized-twitter-streaming-handler

ARG BUILD_ENV
ENV BUILD_ENV=$BUILD_ENV

RUN echo $BUILD_ENV

COPY app ./app/
COPY requirements.txt .
COPY wait-for-it.sh .
COPY config.yaml .

RUN apk update && apk add gcc g++ musl-dev postgresql-dev bash
RUN pip install -r requirements.txt
