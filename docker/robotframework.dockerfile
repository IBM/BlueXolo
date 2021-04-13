ARG PYTHON_VERSION=3.8

FROM python:${PYTHON_VERSION}-slim-buster

ARG ROBOT_VERSION=3.2.2
ARG USER_PASSWORD=bluexolo

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt update && apt install -y -qq openssh-server \
    && pip install --no-cache-dir -U robotframework==${ROBOT_VERSION} \
    robotframework-requests

RUN adduser robot && echo "robot:${USER_PASSWORD}" | chpasswd && \
    mkdir /robot && chown -R robot /robot && service ssh start

EXPOSE 22

CMD ["/usr/sbin/sshd","-D"]