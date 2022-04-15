# Developer Documentation

## Introduction

This document complements the [User Guide](../README.md). Here you can find specifics about the services used by BlueXolo to have a better understanding during development and configure both docker compose environments `docker-compose-deploy.yaml` and `docker-compose.yaml`.

## Architecture

You can find a simple diagram with the architecture from a component view in this [image](BlueXolo_Architecture.png).

## Environments

| Environment | Variable's file | Uses local repository |                    Runs at                     |
| :---------: | :-------------: | :-------------------: | :--------------------------------------------: |
| Production  |      .env       |          No           |      [http://localhost](http://localhost)      |
| Development |    .dev.env     |          Yes          | [http://localhost:8000](http://localhost:8000) |

## Services

As mentioned in the [Architecture](#architecture) section, BlueXolo works with multiple services running on different containers, and most of them are configurable using environment variables, there is a table
with useful information about them. If a service is marked as configurable you can dive into details of [Configurations](#configurations).

### Production services

Defined in `docker-compose-deploy.yaml`.

|        Name        | Port  | Published port |           Configurable           |   Requires volumes   |
| :----------------: | :---: | :------------: | :------------------------------: | :------------------: |
|      bluexolo      | 8000  |       -        | [Yes](#bluexolo-configurations)  |   [Yes](#volumes)    |
|  bluexolo-celery   |   -   |       -        |  Uses bluexolo's configurations  | Shared with bluexolo |
| bluexolo-postgres  | 5432  |       -        | [Yes](#postgres-configurations)  |   [Yes](#volumes)    |
|       redis        | 6789  |       -        |                No                |          No          |
|      robot4.0      |  22   |       -        |                No                |          No          |
|     robot3.2.2     |  22   |       -        |                No                |          No          |
|      robot2.9      |  22   |       -        |                No                |          No          |
| bluexolo-assistant | 3000  |       -        | [Yes](#assistant-configurations) |          No          |
|   bluexolo-proxy   |  80   |       80       |   [Yes](#proxy-configurations)   |   [Yes](#volumes)    |

### Development services

Defined in `docker-compose.yaml`.

|        Name        | Port  | Published port |           Configurable           |   Requires volumes   |
| :----------------: | :---: | :------------: | :------------------------------: | :------------------: |
|      bluexolo      | 8000  |      8000      | [Yes](#bluexolo-configurations)  |   [Yes](#volumes)    |
|  bluexolo-celery   |   -   |       -        |  Uses bluexolo's configurations  | Shared with bluexolo |
| bluexolo-postgres  | 5432  |       -        | [Yes](#postgres-configurations)  |   [Yes](#volumes)    |
|       redis        | 6789  |       -        |                No                |          No          |
|      robot4.0      |  22   |       -        |                No                |          No          |
|     robot3.2.2     |  22   |       -        |                No                |          No          |
|      robot2.9      |  22   |       -        |                No                |          No          |
| bluexolo-assistant | 3000  |      3000      | [Yes](#assistant-configurations) |          No          |

## Configurations

### BlueXolo configurations

Located at `settings.py`, most of them defined in `.env` or `.dev.env` depending on the enviroment. The differences between configurations for development and production are important, feel free to use the following example for the production environment, just make sure to use your own secret key and passwords. You can also use this example to define de development configuration in `.dev.env` just follow the instructions in the comments. 

> This is just an example for you to create your own `.dev.env` or `.env` file, do not forget to remove the comments pointing the differences between the configurations according to the environment.

```bash
ENV_FILE=production # or development
SECRET_KEY=yourSecretKey
ALLOWED_HOSTS=*
ADMIN_MAIL=bluexolo@bluexolo.net
DJANGO_SU_PASSWORD=bluexolopw # Password to login with bluexolo@bluexolo.net
EMAIL_HOST=HOST
EMAIL_PORT=111
EMAIL_HOST_USER=MAILUSER
EMAIL_HOST_PASSWORD=MAILPASSWORD
DB_ENGINE=django.db.backends.postgresql
DB_NAME=bluexolo
DB_HOST=bluexolo-postgres
DB_USER=bluexolo
DB_PASSWORD=bluexolo
DB_PORT=5432
SITE_DNS=http://localhost # http://localhost:8000 in development
IBM_CLIENT=0
DEPTH_SEARCH=0
PLATFORM_VERSION=3.1.0
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
COMPRESS_OFFLINE=0
DEBUG=0 # 1  in development
X_FRAME_OPTIONS=SAMEORIGIN
BOTPRESS_ENDPOINT=/botpress # http://localhost:3000 in development
SESSION_COOKIE_SECURE=0
CSRF_COOKIE_SECURE=0
SECURE_SSL_REDIRECT=0
SECURE_HSTS_SECONDS=3600
SECURE_HSTS_SECONDS=3600
GUNICORN_LOG_LEVEL=DEBUG # Just for development environment
GUNICORN_BIND=0.0.0.0:8000 # Just for development environment
GUNICORN_RELOAD=1 # Just for development environment
GUNICORN_MAX_THREADS=4 # Just for development environment
```

### Postgres configurations

Located at `docker-compose.yaml` or `docker-compose-deploy.yaml` depending on the environment.

```
POSTGRES_USER: bluexolo
POSTGRES_PASSWORD: bluexolo
POSTGRES_DB: bluexolo
```

### Assistant configurations

Located at `docker-compose.yaml` or `docker-compose-deploy.yaml` depending on the environment.

```bash
EXTERNAL_URL: http://localhost/botpress # Don't add this configuration in development
BP_HOST: localhost
PORT: 3000
REVERSE_PROXY: 1 # Don't add this configuration in development
BP_PRODUCTION: 1 # Use 0 in development
VERBOSITY_LEVEL: 1 # Use 3 in development
```

### Proxy configurations

Located at `docker-compose-deploy.yaml`.

```bash
NGINX_PORT: 80
BLUEXOLO_HOST: bluexolo
BLUEXOLO_PORT: 8000
BOTPRESS_HOST: bluexolo-assistant
BOTPRESS_PORT: 3000
NGINX_ENTRYPOINT_QUIET_LOGS: 1 # If debugging is required use 0
```

## Volumes

### Media volume

Docker managed volume used for persistant and shared media files e.g. user uploads, named as `bluexolo_media` and used by the services: 

- bluexolo
- bluexolo-celery
- bluexolo-proxy

### Database volume

Docker managed volume used for persistant database files, named as `bluexolo_db` and used just by `bluexolo-postgres`.

## Extras

### Clear volumes

```bash
docker volume rm bluexolo_media bluexolo_db
```

### Attach to a service shell

```bash
docker exec -it <container_name> <shell> # bash or ash
```

### Build all images

```bash
docker compose -f <compose_file> build --no-cache
```

### Build and run all

```bash
docker compose -f <compose_file> run --build
```

### Build and run specific service

```bash
docker compose -f <compose_file> run --build --no-deps <service_name>
```

### Check logs of container

```bash
docker logs <container_name>
```