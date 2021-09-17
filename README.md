# BlueXolo - Automated Testing Framework

## Introduction

BlueXolo is a WEB framework that allows the generation of test scripts in a visual way using a “drag and drop” interface which allows the generation of complex test cases spending a minimum amount of time. 

> Here you can find the [Main Characteristics](https://github.com/IBM/BlueXolo/blob/master/Main_Characteristics.md) of BlueXolo.

## Getting Started

BlueXolo runs using a Docker Compose environment, so you just need to install:

- Docker
- Docker Compose
- Git

## Installation Guide

Please read the [Installation Guide](INSTALL.md) to get started.

## Development environment

BlueXolo has a development environment to share your local repository with the Docker container running and make the development easy with features like live code changes and configurations for verbose logging. Once you have followed the installation steps you just need to execute one command to run.

### Run

```bash
docker-compose -f docker-compose.yaml up
```

### Stop

```bash
docker-compose -f docker-compose.yaml down
```

### Build

```bash
docker-compose -f docker-compose.yaml build
```

### Clear persistent storage

```bash
docker volume rm bluexolo_development_db bluexolo_development_media
```

## Production environment

This environment is optimized for a faster experience using BlueXolo, with light-weight images just with the required packages.

### Run

```bash
docker-compose -f docker-compose-deploy.yaml up
```

### Stop

```bash
docker-compose -f docker-compose-deploy.yaml down
```

### Build

```bash
docker-compose -f docker-compose-deploy.yaml build
```

### Clear persistent storage

```bash
docker volume rm bluexolo_production_db bluexolo_production_media
```

## Usage

To know more about some common use cases of BlueXolo, please read the [User Guide](https://github.com/IBM/BlueXolo/blob/master/User_Guide.md).

## How To Contribute

Please read [How_To_Contribute.md](https://github.com/IBM/BlueXolo/blob/master/How_To_Contribute.md) for details on our code of conduct, and the process for submitting pull requests to us.

## How to report Issues / Enhancements

If you experience any issues with BlueXolo on any Operating System, or you have a suggestion or enhancement please [open a ticket](https://github.com/IBM/BlueXolo/issues/new/choose) in the issue tracker.

## Licence

[Apache 2.0](https://github.com/IBM/BlueXolo/blob/master/LICENSE)

## YouTube Videos

[Local case study](https://www.youtube.com/watch?v=prtLbBrFsIo)
[Run BlueXolo for Development purposes in MacOSX](https://www.youtube.com/watch?v=U9uG7ZFs-Us&t=118s)
[Libraries](https://www.youtube.com/watch?v=ocdulq2vTL4&t=19s)
[Mextract](https://www.youtube.com/watch?v=ReZXMvrFQOw)

## Contact Links

[BlueXolo Google Group (edited)](https://groups.google.com/forum/#!forum/bluexolo/join)
[BlueXolo Web Page](https://ibm.github.io/BlueXolo/)
[BlueXolo ZenHub](https://app.zenhub.com/workspaces/bluexolo-5c09910d4b5806bc2bfb46c4/board)
[BlueXolo GitHub](https://github.com/IBM/BlueXolo)

## List of Contributors

BlueXolo was originally created in 2016 at IBM by the Systems division in Guadalajara, Jalisco, Mexico.
With a great contribution of Tecnologico de Monterrey.

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore -->

| [<img src="https://avatars3.githubusercontent.com/u/39574410?s=400&v=4" width="100px;"/><br /><sub><b>Abdel Aguilar</b></sub>](https://github.com/abdelmaster)<br />[💻](https://github.com/IBM/BlueXolo/commits?author=abdelmaster) [📖]() [👀](#review-abdelmaster "Reviewed Pull Requests") [✅]() | [<img src="https://avatars2.githubusercontent.com/u/45430016?s=400&v=4" width="100px;"/><br /><sub><b>Jaime Alejandro</b></sub>](https://github.com/jarryfull)<br />[💻](https://github.com/IBM/BlueXolo/commits?author=jarryfull) [📖]() [👀](#review-jarryfull "Reviewed Pull Requests") [✅]()     | [<img src="https://avatars2.githubusercontent.com/u/12001776?s=400&v=4" width="100px;"/><br /><sub><b>Fernando Quintero</b></sub>](https://github.com/fquinteroa)<br />[💻](https://github.com/IBM/BlueXolo/commits?author=fquinteroa) [📖]() [👀](#review-fquinteroa "Reviewed Pull Requests") [✅]() | [<img src="https://avatars1.githubusercontent.com/u/22551455?s=400&v=4" width="100px;"/><br /><sub><b>Oscar Pacheco</b></sub>](https://github.com/scar86)<br />[💻](https://github.com/IBM/BlueXolo/commits?author=scar86) [📖]() [👀](#review-scar86 "Reviewed Pull Requests") [✅]() | [<img src="https://avatars1.githubusercontent.com/u/952272?s=400&v=4" width="100px;"/><br /><sub><b>Ulises Buendia</b></sub>](https://github.com/ulibn)<br />[💻](https://github.com/IBM/BlueXolo/commits?author=ulibn) [📖]() [👀](#review-ulibn "Reviewed Pull Requests") [✅]() | [<img src="https://avatars2.githubusercontent.com/u/36703047?s=400&v=4" width="100px;"/><br /><sub><b>Arianne Navarro</b></sub>](https://github.com/arinavarro)<br />[💻](https://github.com/IBM/BlueXolo/commits?author=arinavarro) [📖]() [👀](#review-arinavarro "Reviewed Pull Requests") [✅]() | [<img src="https://avatars3.githubusercontent.com/u/31775043?s=400&v=4" width="100px;"/><br /><sub><b>David Anizar</b></sub>](https://github.com/davidanizar)<br />[💻](https://github.com/IBM/BlueXolo/commits?author=davidanizar) [📖]() [👀](#review-davidanizar "Reviewed Pull Requests") [✅]() | [<img src="https://avatars2.githubusercontent.com/u/45462773?s=400&v=4" width="100px;"/><br /><sub><b>Victor Hernández</b></sub>](https://github.com/ivicman)<br />[💻](https://github.com/IBM/BlueXolo/commits?author=ivicman) [📖]() [👀](#review-ivicman "Reviewed Pull Requests") [✅]() | [<img src="https://avatars0.githubusercontent.com/u/46430704?s=400&v=4" width="100px;"/><br /><sub><b>Adolfo Reynoso</b></sub>](https://github.com/capikp)<br />[💻](https://github.com/IBM/BlueXolo/commits?author=capikp) [📖]() [👀](#review-capikp "Reviewed Pull Requests") [✅]() | 
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |

<!-- ALL-CONTRIBUTORS-LIST:END -->

Please read the [List of Contributors](https://github.com/IBM/BlueXolo/blob/master/CONTRIBUTORS_LIST.md) to know the all the people that makes this projects possible.
