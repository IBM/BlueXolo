FROM ubuntu:20.04

ARG DEBIAN_FRONTEND="noninteractive"

COPY . /bluexolo/

WORKDIR /bluexolo

RUN apt update && apt install -y -qq libpq-dev gcc \
    python3 python3-pip nano net-tools \
    && pip3 install -U -r requirements.txt

RUN mkdir -p /var/www/media/ /var/www/static/ /var/www/logs/

RUN mv static/* /var/www/static/ && rm -rf static

EXPOSE 8000

CMD [ "/bin/bash", "docker/bluexolo-entrypoint.sh" ]