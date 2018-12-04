## Usando Bluexolo en Docker.

### Pasos para construir la imagen:
1. Obtenemos la imagen de CentOS del repositorio de Docker

   `docker pull centos`
   
   Este proceso solo es necesario una vez, posteriormente ya no es necesario, a menos que se desee actualizar la imagen.
   
2. Corremos la herramienta de construccion.

   `tools/build-image`
   
   (en Linux puede ser necesario anteponer el comando `sudo`)
   
   `sudo tools/build-image`
   
   `El proceso puede durar entre 10 y 15 min. dependiendo de la velocidad del equipo`

### Iniciando Bluexolo en Docker

1. ejecutamos:

    `tools/run-bluexolo.sh`

    El proceso de inicializacion se ejecuta posteriormente de inicio del container. 

    Nota: Por omision se encuentra abierto solo el puerto 8000.

### Accediendo a la interfaz web.

  Ejecutar:

    `http://localhost:8000/home`
    
### Usuarios y Passwords por omision.
  Usuario | Password | Descripcion
  ------- | -------- | -----------
  bluexolo | bluexolo | Usuario del sistema
  root | bluexolo | Usuario root
  bluexolo | bluexolo | Usuario de RabbitMQ
  bluexolo@bluexolo.net | darkprogrammers | Usuario de Bluexolo

  `Es posible cambiar los usuarios y passwords en el Dockerfile, pero tambien debe de modificarse el archivo secrets.json en 
  el directorio sources`
  
### Informacion adicional.
  - Los fuentes de bluexolo deben estar contenidos en un archivo denominado `bluexolo_src.tgz` en el directorio sources.
  - El archivo `secrets.json` se encuentra en el directorio sources
    
### Todo 

  - Generar un proceso automatico de configuracion del Dockerfile para configurar usuarios.

### Dudas y preguntas.
Fernando Quintero <quintero@mx1.ibm.com>


