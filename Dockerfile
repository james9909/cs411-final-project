FROM alpine:3.11.5

RUN apk update && apk add \
    python3 \
    python3-dev \
    gcc musl-dev linux-headers \
    mariadb-dev

WORKDIR /cs411
COPY requirements.txt /cs411
RUN pip3 install -r requirements.txt

COPY app /cs411/app
COPY docker-entrypoint.sh /cs411
ENTRYPOINT ["sh", "./docker-entrypoint.sh"]
