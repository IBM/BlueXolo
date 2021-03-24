FROM ubuntu:20.04

ARG DEBIAN_FRONTEND="noninteractive"

COPY . /bluexolo/

WORKDIR /bluexolo

RUN apt update && apt install -y -qq \
    libpq-dev gcc python3 python3-pip \
    && pip3 install -U -r requirements.txt

RUN mkdir -p {/var/www/media/,/var/www/static/}

RUN adduser -D bluexolo
RUN chown -R user:bluexolo {/vol,/bluexolo/docker}
RUN chmod -R 755 /vol/web

USER bluexolo

EXPOSE 8000

CMD [ "/bin/bash", "bluexolo-entrypoint.sh" ]