#--------------------------------------------------------
# Docker Image file to create BlueXolo
# CentOS Version.
#--------------------------------------------------------
FROM centos
MAINTAINER F. Quintero <fquinteroa@gmail.com>
ENV REFRESHED_AT=2019-03-08_15:09
ENV container docker

# --------------------------------
# First step:
# Configure systemd
# --------------------------------
RUN yum -y install systemd; yum clean all; 
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
ADD scripts/startup.sh /usr/local/bin/
ADD scripts/update_pg_pwd.sql /
ADD scripts/users.sql /
ADD scripts/create_bluexolo_db.sql /
ADD scripts/init-pg.sh /usr/local/bin/
ADD scripts/setup-bluexolo.sh /usr/local/bin/
ADD scripts/run-server.sh /usr/local/bin/
ADD scripts/run-as.sh /usr/local/bin/
ADD scripts/bluexolo.env /etc
COPY scripts/rc.local /etc
COPY scripts/rc.local /etc/rc.d
ADD scripts/FIRST_SETUP /
ADD scripts/install-robot.sh /
RUN \
chmod 0755 /usr/local/bin/startup.sh &&\
chmod 0755 /usr/local/bin/init-pg.sh &&\
chmod 0755 /usr/local/bin/setup-bluexolo.sh &&\
chmod 0755 /usr/local/bin/run-server.sh &&\
chmod 0755 /usr/local/bin/run-as.sh &&\
chmod 0755 /etc/rc.local &&\
chmod 0755 /etc/rc.d/rc.local 


# --------------------------------
# Install packages from Repository
# --------------------------------
RUN \
  yum makecache && \
  yum -y install epel-release \
  man \
  initscripts \
  openssl \
  wget \
  gcc \
  make  \
  firewalld  \
  unzip  \
  openssl-devel \
  bzip2-devel  \
  postgresql  \
  postgresql-server \
  postgresql-contrib \
  git \
  erlang &&\
  yum -y clean all 

# ------------------------
# Set workdir to tmp
# ------------------------
WORKDIR /tmp  

# ------------------------
# Install python 3.6.6
# ------------------------
RUN \
  wget https://www.python.org/ftp/python/3.6.6/Python-3.6.6.tgz && \
  tar -xvzf Python-3.6.6.tgz && \
  cd Python-3.6.6 && \
  ./configure --enable-optimizations && \
  make altinstall 

# ------------------------
# Setup python3 as default
# ------------------------
RUN \
  ln -sf /usr/local/bin/python3.6 /usr/bin/python3 &&\
  ln -sf /usr/local/bin/pip3.6 /usr/bin/pip3


# ------------------------------
# Install RabbitMQ and enable it
# along with PostgreSQL
# ------------------------------
RUN \
  wget https://www.rabbitmq.com/releases/rabbitmq-server/v3.6.10/rabbitmq-server-3.6.10-1.el7.noarch.rpm 

RUN \
  yum -y install rabbitmq-server-3.6.10-1.el7.noarch.rpm &&\
  yum clean all 

RUN \
  systemctl enable rabbitmq-server  ;\
  systemctl enable postgresql; \
  systemctl enable firewalld 

# ---------------------------------------------
# Install bluexolo sources and install pre-reqs
# ---------------------------------------------

# ------------------
# Install virtualenv 
# ------------------
RUN \
  pip3.6 install virtualenv

COPY sources/bluexolo_src.zip /tmp

RUN \
  mkdir -p /opt/BlueXolo &&\
  cd /opt/BlueXolo &&\
  unzip /tmp/bluexolo_src.zip  
RUN \
  cd /opt/BlueXolo &&\
  pip3.6 install -r requirements.txt 

# Set password for root 'bluexolo'
RUN \
  echo "bluexolo" | passwd --stdin root

ADD sources/secrets.json /opt/BlueXolo/

# -------------------
# Clean tmp directory
# -------------------
RUN rm -rf  /tmp/* &&\
rm -rf /var/cache/yum

# ---------------------------
# Install robot and libraries
# ---------------------------
RUN /install-robot.sh

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
EXPOSE 443
EXPOSE 4369
EXPOSE 25672
EXPOSE 5432
EXPOSE 5671
EXPOSE 5672
EXPOSE 15672
EXPOSE 61613
EXPOSE 61614
EXPOSE 1883
EXPOSE 8883

# ------------------------------
# Set initial command for image
# ------------------------------
CMD ["/usr/sbin/init"]

# ------------------------------
# End of Dockerfile
# ------------------------------

