#--------------------------------------------------------
# Docker Image file to create BlueXolo
# CentOS Version.
#--------------------------------------------------------
FROM ubuntu:18.04
MAINTAINER F. Quintero <fquinteroa@gmail.com>
ENV REFRESHED_AT=2020-07-31_12:17
ENV container docker
# ENV TZ=America/Mexico_City
# RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# --------------------------------
# First step:
# Configure systemd
# --------------------------------
RUN apt-get update
RUN apt-get -y -qq install apt-utils;
# RUN apt-get install -y init
RUN apt-get -y -qq install systemd python3.6 rabbitmq-server postgresql unzip nvi; 
RUN apt-get -y -qq install python3-pip; 
RUN (cd /lib/systemd/system/sysinit.target.wants/; for i in ; do [ $i == systemd-tmpfiles-setup.service ] || rm -f $i; done); \
rm -f /lib/systemd/system/multi-user.target.wants/;\
rm -f /etc/systemd/system/.wants/;\
rm -f /lib/systemd/system/local-fs.target.wants/; \
rm -f /lib/systemd/system/sockets.target.wants/udev;\ 
rm -f /lib/systemd/system/sockets.target.wants/initctl;\ 
rm -f /lib/systemd/system/basic.target.wants/;\
rm -f /lib/systemd/system/anaconda.target.wants/*;
VOLUME [ “/sys/fs/cgroup” ]
VOLUME [ "/opt/BlueXolo-src" ]
VOLUME [ "/var/lib/pgsql" ]
VOLUME [ "/opt/bluexolo-custom" ]

# ----------------------------------
# Copy important files to filesystem
# ----------------------------------
ADD scripts/update_pg_pwd.sql /
ADD scripts/users.sql /
ADD scripts/create_bluexolo_db.sql /
COPY scripts/rc.local /etc
ADD scripts/FIRST_SETUP /
ADD scripts/install-robot.sh /
RUN \
chmod 0755 /etc/rc.local 

# ------------------------
# Set workdir to tmp
# ------------------------
WORKDIR /tmp  

RUN \
  systemctl enable rabbitmq-server  ;\
  systemctl enable postgresql; 

# ---------------------------------------------
# Install bluexolo sources and install pre-reqs
# ---------------------------------------------

# ------------------
# Install virtualenv 
# ------------------

COPY sources/bluexolo_src.zip /tmp

RUN \
  mkdir -p /opt/BlueXolo &&\
  cd /opt/BlueXolo &&\
  unzip /tmp/bluexolo_src.zip  

# Set password for root 'bluexolo'

ADD sources/secrets.json /opt/BlueXolo/

# -------------------
# Clean tmp directory
# -------------------
RUN rm -rf  /tmp/* 

# ---------------------------
# Install robot and libraries
# ---------------------------
#RUN /install-robot.sh

# --------------------------
# Tweak logind.conf to avoid 
# terminals
# -------------------------
RUN echo 'NAutoVTs=0' >> /etc/systemd/logind.conf
RUN echo 'ReserveVT=0' >> /etc/systemd/logind.conf
RUN rm -f /lib/systemd/system/console-getty.service
# --------------------------
# Set ports to be accesible
# --------------------------
EXPOSE 8000

# ------------------------------
# Set initial command for image
# ------------------------------
CMD ["/sbin/init"]

# ------------------------------
# End of Dockerfile
# ------------------------------

