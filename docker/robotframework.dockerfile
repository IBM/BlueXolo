ARG PYTHON_VERSION=3.8

FROM python:${PYTHON_VERSION}-alpine

ARG ROBOT_VERSION=4.0
ARG USER_PASSWORD=bluexolo
ARG ROBOT_EXECUTABLE=robot

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk add --update --no-cache openssh &&  rm -rf /tmp/* /var/cache/apk/* \
    && pip install --no-cache-dir -U robotframework==${ROBOT_VERSION} \
    robotframework-requests && mv /usr/local/bin/${ROBOT_EXECUTABLE} /usr/bin/robot

RUN adduser -h /robot -D robot && echo "robot:${USER_PASSWORD}" | chpasswd && \
    chown -R robot /robot && rm -rf /etc/ssh/ssh_host_rsa_key /etc/ssh/ssh_host_dsa_key && \
    ssh-keygen -f /etc/ssh/ssh_host_rsa_key -N '' -t rsa && \
    ssh-keygen -f /etc/ssh/ssh_host_dsa_key -N '' -t dsa

EXPOSE 22

CMD [ "/usr/sbin/sshd", "-D" ]