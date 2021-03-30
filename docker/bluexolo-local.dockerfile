# build -t snvc00/bluexolo:local -f docker/bluexolo-local.dockerfile .
# run -p 8000:8000 -v $REPO_LOCAL:/bluexolo --env-file .env --rm --name bluexolo snvc00/bluexolo:local

# celery process in different container
#docker run --env-file .env --rm --name bluexolo-celery snvc00/bluexolo:local '/bin/bash' -c 'cd /bluexolo && celery -A CTAFramework worker -l info'

FROM python:3.8-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /bluexolo/

WORKDIR /bluexolo

RUN apt update && apt install -y -qq gcc \
    && pip3 install --no-cache-dir -U -r requirements-local.txt

RUN mkdir -p /var/www/media/ /var/www/static/ /var/www/logs/

RUN mv static/* /var/www/static/ && rm -rf static

EXPOSE 8000

CMD [ "/bin/bash", "docker/bluexolo-entrypoint.sh" ]