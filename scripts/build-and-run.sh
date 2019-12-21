#!/bin/sh

rm ./requirements.txt

pipenv lock --requirements > ./requirements.txt

docker build --build-arg BUILD_ENV=docker -t localized-twitter-stream-handler --no-cache .

docker-compose up