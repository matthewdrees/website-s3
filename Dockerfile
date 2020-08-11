FROM python:3.7-alpine

WORKDIR /app

ADD README.md /app

RUN apk add --no-cache ffmpeg zlib-dev jpeg-dev gcc musl-dev make

RUN pip install natsort pillow boto scons
