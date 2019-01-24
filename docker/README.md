## Using Bluexolo in Docker

### Steps to build the image:
1. Get the CentOS image from Docker repository

   `docker pull centos`
   
   This process is only needed once, after that is not necessary anymore, unless you wish to update the image.  
   
2. Run build tool

   `tools/build-image`
   
   (it may be needed to use `sudo` when running in Linux)   
   
   `sudo tools/build-image`
   
   `The process may last between 10 and 15 min. depends on equipment`   

### Starting Bluexolo

1. Run:

    `tools/run-bluexolo.sh`

    The initialization process is executed after container init.    
    
    Note: Port 8000 is open by default.

### Accessing web interface

  Run:

    `http://localhost:8000/home`
    
### Users and Passwords
  User | Password | Description
  ------- | -------- | -----------
  bluexolo | bluexolo | Regular User
  root | bluexolo | System User
  bluexolo | bluexolo | RabbitMQ User
  bluexolo@bluexolo.net | darkprogrammers | Bluexolo User

` It is possible to change users and passwords in Dockerfile, but secrets.json file must be changed as well in sources directory.`
  
### Additional information

  - bluexolo sources must be in a file named `bluexolo_src.tgz` in sources directory.
  - `secrets.json` file is located in sources directory.
 
    
### Todo 

  - Generate a process to configure users in Dockerfile 

### Doubts and questions
Fernando Quintero <fquinteroa@gmail.com>


