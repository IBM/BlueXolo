FROM python:3.8-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /bluexolo/

WORKDIR /bluexolo

RUN apt update && apt install -y -qq gcc libpq-dev \
    && pip3 install --no-cache-dir -U -r requirements.txt

RUN mkdir -p /var/www/media/ /var/www/static/ /var/www/logs/ \
    && mv static/* /var/www/static/ && rm -rf static

RUN adduser bluexolo && echo "bluexolo:${USER_PASSWORD}" | chpasswd \
    && chown -R bluexolo /var/www/

USER bluexolo

EXPOSE 8000

CMD [ "/bin/bash", "docker/bluexolo-entrypoint-prod.sh" ]