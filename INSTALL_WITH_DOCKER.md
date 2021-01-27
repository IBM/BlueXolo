# BlueXolo in Linux with Docker

## Requirements

> Guide for `Ubuntu 20.04`

* Docker
* Git
* BlueXolo Repository

## Install Docker

```bash
sudo apt install -y docker.io 
sudo usermod -aG docker $USER
docker -v
```

## Get the BlueXolo Repository

```bash
git clone https://github.com/IBM/BlueXolo.git
```

## Using BlueXolo

Before you can use BlueXolo, create a folder named _BlueXoloData_ in a directory with
read and write permissions, you will need the path of this folder and the path of the
BlueXolo repository. If you want to run BlueXolo execute the following script located
inside the repository.

```bash
/docker/tools/start-bluexolo.sh
```

This script will ask for the path of the repository and the path of _BlueXoloData_, and
that is it, the BlueXolo will be running after a few minutes in _localhost:8000_.

To stop BlueXolo run the script:

```bash
/docker/tools/stop-bluexolo.sh
```

> Tip: You can modify your _start-bluexolo.sh_ script and set a value for the variable
__BLUEXOLO_DIR__ with the path of the repository and __BLUEXOLO_DATA__ with the path to
the folder that you have created.
