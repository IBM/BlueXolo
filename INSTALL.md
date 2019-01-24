# Install instructions for RHEL/Centos 7.5

## Install Pre-req:


* Python 3.6
* virtualenv
* Install epel repo
* Rabbit-mq
* Postgresql
* bluexolo specific requierements

## Install Python 3.6

RHEL/Centos doesn't have python3, we will compile it from source

```
#Install build dependencies
yum install gcc openssl-devel bzip2-devel´

#Change to build directory
cd/usr/src

#Download python source code
wget https://www.python.org/ftp/python/3.6.6/Python-3.6.6.tgz

#uncompress python
tar -xvf Python-3.6.6.tgz
cd Python-3.6.6/

#build python
./configure --enable-optimizations
make altinstall

#Verify python ins installed
python3.6

#You can exit python with CTRL-D
```

## Install virtualenv
Having a virtualenv for our project allow us to mess with the overall python installation/packages

```
pip3.6 install virtualenv
```

## Install epel repo

Epel repo allow us to install rabbitmq erlang dependencies

```
su -c 'rpm -Uvh http://download.fedoraproject.org/pub/epel/7/x86_64/e/epel-release-7-10.noarch.rpm'
cd /tmp
wget https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
ls *.rpm
yum install epel-release-latest-7.noarch.rpm
```

## Install Rabbit-MQ
Rabbit MQ is what is called a broker, it allow us to run async task

```
#Refresh repos
yum repolist

#install Erlang
yum install erlang

#Download a compatible epel-erlang Rabbitmq
cd /root
wget https://www.rabbitmq.com/releases/rabbitmq-server/v3.6.10/rabbitmq-server-3.6.10-1.el7.noarch.rpm
yum install rabbitmq-server-3.6.10-1.el7.noarch.rpm

#Start and enable rabbitmq
systemctl start rabbitmq-server
systemctl status rabbitmq-server
systemctl enable rabbitmq-server

#Open some tcp ports needed
firewall-cmd --zone=public --permanent --add-port=80/tcp
firewall-cmd --zone=public --permanent --add-port=443/tcp
firewall-cmd --zone=public --permanent --add-port=4369/tcp
firewall-cmd --zone=public --permanent --add-port=25672/tcp
firewall-cmd --zone=public --permanent --add-port=5671-5672/tcp
firewall-cmd --zone=public --permanent --add-port=15672/tcp
firewall-cmd --zone=public --permanent --add-port=61613-61614/tcp
firewall-cmd --zone=public --permanent --add-port=1883/tcp
firewall-cmd --zone=public --permanent --add-port=8883/tcp

```

Create a rabbitmq user for bluexolo

```
#user bluexolo
#Passwd Bluxolo
#vhost Bluexolo
rabbitmqctl add_user bluexolo
rabbitmqctl add_user bluexolo Bluexolo
rabbitmqctl add_vhost bluehost
rabbitmqctl set_user_tags bluezolo bluetag
rabbitmqctl set_user_tags bluexolo bluetag
rabbitmqctl set_permissions -p bluehost bluexolo ".*" ".*" ".*"

```

## Install Postgresql
Postgress sql is a relational database, it is the default db to use with bluexolo

```
#install posgtress
yum install postgresql-server postgresql-contrib
#Initialize postresql database
postgresql-setup initdb
```

Start and enable postgresql

```
systemctl start postgresql
systemctl enable postgresql
```


Set a password to postgress user
```
sudo -i -u postgres
psql
alter user postgres with encrypted password 'My_password';
```

We will need to edit one postgressql config file to allow us to authenticate using passwords

```
vi /var/lib/pgsql/data/pg_hba.conf
```

And modify the lines starting with local/host to change ident to md5 at the end of those lines

```
# "local" is for Unix domain socket connections only
local   all             all                                    md5
# IPv4 local connections:
host    all             all             127.0.0.1/32            md5
# IPv6 local connections:
host    all             all             ::1/128                 md5
```

Restart postgress to pick up the changes

```
systemctl stop postgresql
systemctl start postgresql
```


Create a user and database for bluexolo

```
# as root
adduser my_user

#change to postgress user to create bluexolo database
su -i -u postgresql
psql

CREATE DATABASE yourdbname;
CREATE USER youruser WITH ENCRYPTED PASSWORD 'yourpass';
GRANT ALL PRIVILEGES ON DATABASE yourdbname TO youruser;

```


## Set up bluexolo and install specifig pre-req


Download or clone the latest release of bluexolo

```
git clone git@github.ibm.com:blue-xolo/blue-xolo-framework.git
```

Create a virtualenv called vend and activate it

```
python3.6 -m virtualenv venv
source venv/bin/python
source venv/bin/activate
```

Install bluexolo python requirements on our virtualenv

```
cd blue-xolo-framework/

pip install -r requirements.txt
```

## Set up bluexolo and run it
```
cp secrets.json.dist secrets.json

```
Populate the secrets.json with your credentials for posgress and rabiitmq


Perform the initializazion of the databases

```
python manage.py migrate
python manage.py makemigrations
python manage.py migrate
```

Create a superuser

```
python manage.py createsuperuser
```

run celery in the background

```
nohup celery -A CTAFramework worker -l info &
```

Run bluexolo
This command will run bluexolo on port `8000`, you can use your browser to connect to it

```
python manage.py runserver 0.0.0.0:8000
```
