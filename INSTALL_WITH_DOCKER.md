# BlueXolo using Docker in Ubuntu

## Install Docker

### Update your system
```
sudo apt update
sudo apt upgrade
```

### Remove older installations of Docker
```
sudo apt remove docker docker-engine docker.io
```

```
sudo apt install apt-transport-https ca-certificates curl software-properties-common gnupg
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo apt-key fingerprint 0EBFCD88
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
```

### If there is not stable version of Docker for your system use the following command instead
```
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable edge test"
```

```
sudo apt update
sudo apt install docker-ce
sudo usermod -aG docker $USER
```

## Clone the BlueXolo Repository
```
sudo apt install git
git clone https://github.com/IBM/BlueXolo.git
```
## Start BlueXolo
```
cd BlueXolo/docker/tools
sudo ./start-bluexolo.sh
```
## Stop BlueXolo
```
sudo ./stop-bluexolo.sh

```
