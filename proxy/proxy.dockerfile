FROM nginxinc/nginx-unprivileged:1-alpine

COPY ./proxy/default.conf.template /etc/nginx/templates/default.conf.template
COPY ./proxy/uwsgi_params /etc/nginx/uwsgi_params

USER root

RUN mkdir -p /var/www/static /var/www/media
RUN chmod 755 /var/www/static /var/www/media

COPY ./static/ /var/www/static/

USER nginx