## Docker Bluexolo HowTo



#### Remover imagen de Bluexolo en Docker.

1. Detenemos los contenedores que están corriendo 

   1. `docker rm $(docker ps -qa)`

      `docker rmi $(docker images|grep none|awk '{print $3}')`
2. Removemos la imagen.

   1. `docker rmi $(docker images bluexolo -q)`

#### Instalar una nueva imagen de Bluexolo en Docker

1. Ejecutamos el comando:
   1. `docker load -i <archivo de imagen de bluexolo>`

