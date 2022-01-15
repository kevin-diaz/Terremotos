# Terremotos
Trabajo de sistemas distribuidos

# Tabla de contenidos
- [Requisitos y versiones](#requisitos-y-versiones)
- [Ejecución con Docker](#ejecución-con-docker)
## Requisitos y versiones

### Requisitos
- Docker
- Docker Compose

## Ejecución con Docker

1. Ejecutar el siguiente comando 
    ```
    sudo docker-compose up --build --remove-orphans
    ```
2. La aplicación estará corriendo en: 

    Backend:
 - http://localhost:8085/
    
    Postgres:
 - http://localhost:5500/

    Zookeper:
 - PORT: 2181

    Kafka (Brocker 1):
 - PORT: 29092

    Kafka (Brocker 2):
 - PORT: 29093

# Proceso:

1. Luego de correr el docker-compose se debe de ejeuctar el fichero info-kafka-infrastructure-v1.sh de la carpeta script:
    sh info-kafka-infrastructure-v1.sh ../docker-compose.yaml 5

2. Dentro de la carpeta bin de la carpeta kafka del proyecto ver los topics que existen:
    kafka-topics --list --zookeeper localhost:2181

