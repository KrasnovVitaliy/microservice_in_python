FROM python:3.8-slim

WORKDIR /app

RUN apt-get update
RUN apt install -y \
gcc g++ python-dev librocksdb-dev build-essential \
libsnappy-dev zlib1g-dev libbz2-dev libgflags-dev \
liblz4-dev libzstd-dev curl

COPY ./app /app

RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt


CMD faust -A main worker -l info