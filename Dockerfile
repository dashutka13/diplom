FROM python:3
WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    python3-dev \
    && apt-get clean

COPY /requirements.txt /

RUN pip install -r /requirements.txt --no-cache-dir

COPY . .
