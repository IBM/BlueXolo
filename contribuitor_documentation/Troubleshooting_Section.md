# **BlueXolo Troubleshooting**

In this section you can view troubleshooting related with BlueXolo.

- [Unable to complete BlueXolo installation](#unable-to-complete-bluexolo-installation)
- [Unable to log into BlueXolo](#unable-to-log-into-bluexolo)
- [Page stuck at "waiting for \<ipaddess>" after creating element](#page-stuck-at-waiting-for-ipaddess-after-creating-element)
- [As a user is not posible to run keywords or any robot testing item](#as-a-user-is-not-posible-to-run-keywords-or-any-robot-testing-item)


## **Unable to complete BlueXolo installation**

> Related with Issue [#280](https://github.com/IBM/BlueXolo/issues/280)

#### **Issue**

As user, when I try install BlueXolo show me an error, and I can not complete the steps.

*Steps to reproduce the behavior:*

1. Follows the instructions to install BlueXolo
2. Runs `python manage.py migrate` command
3. Shows an error: `ModuleNotFoundError: No module named '_bz2'`

#### **Solution**

For resolve this issue in Centos 7, you could complete the next steps:

1. Install bzip2-devel
   `sudo yum install bzip2-devel`

2. Then you need re-compile python
   ```
   cd /usr/src/python-3.6.6/
   ./configure --enable-optimizations
   make altinstall
   ````

3. You can run `python manage.py migrate` command and complete the installation.


## **Unable to log into BlueXolo**

> Related with Issue [#281](https://github.com/IBM/BlueXolo/issues/281)

#### **Issue**

When I try to log into BlueXolo Framework on the web browser, it shows me an error on the web page about django.session does not exist.

*Steps to reproduce the behavior:*

1. Run `python manage.py runserver 0.0.0.0:8000` command
2. Go to `0.0.0.0:8000` on the web browser
3. Click on the login
4. Enter credentials
5. See error

#### **Solution**

For resolve this issue you could update PostgreSQL 9.2 to 9.6:

1. Remove PostgreSQL 9.2 from the O.S.

2. Go to https://www.postgresql.org/download/linux/redhat/

3. Select your O.S.

4. Run: 
   ```
   yum install https://download.postgresql.org/pub/repos/yum/reporpms/EL-7-x86_64/pgdg-redhat-repo-latest.noarch.rpm -y
   ```

5. Run: 
   ```
   yum install postgresql96 postgresql96-server postgresql96-contrib postgresql96-libs -y
   ```

6. Initialize PostgreSQL:
   ```
   /usr/pgsql-9.6/bin/postgresql96-setup initdb
   ```

7. Start/Enable PostgreSQL:
   ```
   systemctl enable postgresql-9.6.service
   systemctl start postgresql-9.6.service
   ```

8. Set a password to postgres user:
   ```
   sudo -i -u postgres
   psql
   alter user postgres with encrypted password 'My_password';
   ```

9. Configure file to allow us to authenticate using passwords, change ident to md5:
   ```
   vi /var/lib/pgsql/9.6/data/pg_hba.conf
   ```

10. Restart postgres service:
    ```
    systemctl stop postgresql-9.6.service
    systemctl start postgresql-9.6.service
    ```

11. Create user and database for bluexolo:
    ```
    sudo -i -u postgres
    psql
    CREATE DATABASE yourdbname;
    CREATE USER youruser WITH ENCRYPTED PASSWORD 'yourpass';
    GRANT ALL PRIVILEGES ON DATABASE yourdbname TO youruser;
    ```

12. Set up BlueXolo and create new super user


## **Page stuck at "waiting for \<ipaddess>" after creating element**

> Related with Issue [#346](https://github.com/IBM/BlueXolo/issues/346)

#### **Issue**

Page stuck in loading whenever a user tries to create a Library/Robot Framework version. Item is created but commands are not extracted and success or failure notification is not displayed.

*Steps to reproduce the behavior:*

1. Go to `http://0.0.0.0:8000/sources/robot/`
2. Click on '+' to add a new robot item
3. Fill required fields with valid data
4. Click on "Create"

This also affecting the Libraries view

#### **Solution**

The docker image needs internet for some task (otherwise this issue occur) solution is not make change in the code, and only describes steps to solve it:

1. Login to docker image that is running bluexolo code
   ```
   docker exec -it bluexolo bash
   ```
   
2. Search the process that is keeping alive django webserver, use the command ps -aux. The process should be running the command:
   ```
   python3 manage.py runserver <host>:<port>
   ```
   Example:
   ```
   python3 manage.py runserver 0.0.0.0:8000
   ```

3. Once the process is canceld, rabbitmq should be restarted to do this run the command
   ```
   rabbitmqctl stop
   rabbitmq-server start -detached
   rabbitmq-server start -detached
   ```

4. Finally start again django webserver using the command
   ```
   nohup python3 manage.py runserver <host>:<port> >> logs/django_<dd>_<mm>_<yyyy>_log.txt &
   Example:
   nohup python3 manage.py runserver 0.0.0.0:8000 >> logs/django_25_11_2020_log.txt &
   ```
5. Now django web server should be up and running, the website should be available to be used


## **As a user is not posible to run keywords or any robot testing item**

> Related with Issue [#344](https://github.com/IBM/BlueXolo/issues/344) 

#### **Issue** 
As a user is not posible to run keywords or any robot testing item.

*Steps to reproduce the behavior:*

1. Go to `http://localhost:8000/testings/[keywords, testcases, testsuites]/`
2. Click on '+' and create a new testing item.
3. Click on the run, and select a profile.
4. See error

#### **Solution**

*Approach using an external container running Robot Framework*

1. Create a new directory and add a Dockerfile with the following instructions:

    ```
    FROM python:2
    RUN apt-get update && 
    apt-get install -y openssh-server && python -m pip install robotframework==2.8.7 && 
    python -m pip install robotframework-requests==0.6.4 && 
    python -m pip install robotframework-sshlibrary==2.1.2
    RUN echo "root:Password" | chpasswd
    EXPOSE 22
    ```

2. Build the created Dockerfile:

    ```
    docker build -t robot2 <pathToDockerfile>
    ```

3. Modify the shell script `start-bluexolo.sh` located in `docker/tools/`:

    ```
    #!/bin/bash

    # Create private network
    docker network create --subnet=172.18.0.0/16 bxnetwork

    # Run bluexolo 
    nohup docker run --privileged \
     -p 8000:8000 \
     -h bluexolo \
     --net bxnetwork --ip 172.18.0.22 \
    -e container=docker \
    -v /sys/fs/cgroup:/sys/fs/cgroup \
    -v /opt/sources/BlueXolo:/opt/BlueXolo-src \
    -v /opt/bluexolo-data:/var/lib/postgresql \
    --name bluexolo \
    bluexolo/bluexolo  &
    ```

4. Add the following line at the end of the `stop-bluexolo.sh` script:

    ```
    docker network rm bxnetwork
    ```
    > Remove the private network when BlueXolo is not running.

5. Run the `start-bluexolo.sh` script using the following command located in the `docker/tools` directory:

    ```
    sudo ./start-bluexolo.sh
    ```

6. Run the robot2 docker image:

    ```
    nohup docker run -it -d --privileged --net bxnetwork --ip 172.18.0.22 robot2:latest &
    ```

7. Retrieve the container ID of the running robot2 image with:

    ```
    docker ps
    ```

8. Entry to the bash of the container using:

    ```
    docker exec -it <containerID> /bin/bash
    ```

9. Start the SSH service

    ```
    service shh start
    ```

10. Add your user in robot2 container and give permissions to associated directories:

    ```
    adduser yourUser
    chmod -R 777 home
    chmod 777 media
    ```

11. Create four Local Network Connection parameters in BlueXolo:

    ```
    host
    passwd
    path
    user
    ```

12. Create a Local Network Connection template including the created parameters.

13. Create a new profile using the created template and fill the parameters.

    > user: yourUser  
    > host: 172.18.0.23 (IP of the robot2 container)  
    > passwd: [passwordUsedInTheUserCreation]  
    > path: /home/[yourUser]/

14. Now select this profile at the execution moment of any testing item in BlueXolo.


*Approach installing needed resources in BlueXolo docker image*

1. Add the following instruction in the Dockerfile located in `/BlueXolo/docker/` to expose port 22 :

    ```
    EXPOSE 22
    ````

2. Verify that the port 22 is not listening any process:

    ```
    sudo lsof -i:22
    ```
    > If there is a process associated with the port just use sudo kill [PID]

3. Execute the shell script `start-bluexolo.sh` located in `docker/tools/` :

    ```
    sudo ./start-bluexolo.sh
    ```

4. Entry to the bash of the container using:

    ```
    sudo docker exec -ti bluexolo /bin/bash
    ```
    > Or use the attach-bluexolo.sh script

5. Execute the following command:

    ```
    apt-get update && apt install -y python python-pip && 
    apt-get install -y openssh-server && 
    python -m pip install robotframework==2.8.7 robotframework-requests==0.6.4 robotframework-sshlibrary==2.1.2 &&
    apt-get install net-tools
    ```

6. Retrieve the IP of the running instance of BlueXolo:

    ```
    ifconfig -a
    ```

7. Add your user in BlueXolo container and give permissions to associated directories:

    ```
    adduser yourUser
    chmod -R 777 /home
    chmod 777 /media
    ```

8. Create four Local Network Connection parameters in BlueXolo:

    ```
    host
    passwd
    path
    user
    ```

9. Create a Local Network Connection template including the created parameters.

10. Create a new profile using the created template and fill the parameters.

    > **user:** yourUser  
    > **host:** [runningDockerContainerIP]  
    > **passwd:** [passwordUsedInTheUserCreation]  
    > **path:** /home/[yourUser]

11. Now select this profile at the execution moment of any testing item in BlueXolo.

    > Important: Once the execution was complete, check #344 to open the generated report correctly.



