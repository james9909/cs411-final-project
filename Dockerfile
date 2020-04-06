FROM alpine:3.11.5

RUN apk update && apk add \
    python3 \
    python3-dev \
    gcc \
    musl-dev \
    linux-headers \
    libffi-dev \
    openssl-dev \
    mariadb-dev

WORKDIR /cs411
COPY requirements.txt /cs411
RUN pip3 install -r requirements.txt

COPY manage.py /cs411
COPY docker-entrypoint.sh /cs411
COPY migrations /cs411/migrations
COPY app /cs411/app
ENTRYPOINT ["sh", "./docker-entrypoint.sh"]
