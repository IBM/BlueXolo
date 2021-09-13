FROM python:3.8-slim-buster

ARG USER_PASSWORD=bluexolo

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /bluexolo/

WORKDIR /bluexolo

RUN apt update && apt install -y -qq gcc libpq-dev \
    && pip3 install --no-cache-dir -U -r requirements.txt

RUN useradd bluexolo && echo "bluexolo:${USER_PASSWORD}" | chpasswd \
    && mkdir /var/www && chown -R bluexolo /bluexolo /var/www

USER bluexolo

RUN mkdir -p /var/www/media/ /var/www/static/ /var/www/logs/ \
    && mv static/* /var/www/static/ && rm -rf static

EXPOSE 8000

CMD [ "/bin/bash", "docker/bluexolo-entrypoint.sh" ]