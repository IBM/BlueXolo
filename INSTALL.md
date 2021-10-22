# Installation Guide

## Prerequisites

- [Docker Engine](https://docs.docker.com/engine/install/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Git](https://git-scm.com/downloads)

## Instructions

### Clone the repository

```bash
git clone https://github.com/IBM/BlueXolo.git
```

### Create environment files

In order to use the Compose environments you need the `.env` or `.dev.env` files in the root of the repository depending on the environment that you want to run, you can check the specifications of the production environment in the `docker-compose-deploy.yaml` file, for development use `docker-compose.yaml`. We provide an example of a basic env file in the [Developer Documentation](contribuitor_documentation/Developer_Documentation.md#bluexolo-configurations).

> **Note:** It is important to not just copy and paste the BlueXolo configuration example from the developer documentation, it has some comments marked with #, and those comments are guidelines to differentiate how the configurations changes between production and development environments, so those *comments* must be removed to end up with a `KEY=VALUE` format.

### You are ready to go

Now you are able to run the environment according to the [BlueXolo - Automated Testing Framework](README.md).

