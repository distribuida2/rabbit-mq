# Colas de mensajería - Rabbit MQ

## ¿Qué hay en este repositorio?

En la materia vemos colas de mensajería y middleware orientado a mensajes como un tema de la currícula y elegimos por el momento RabbitMQ como herramienta de ejemplo, así que este repositorio contiene algunos recursos que sirven para poder usar este software.

## Instalación

Vamos a usar la [imágen oficial Docker de RabbitMQ](https://hub.docker.com/_/rabbitmq) que viene con el módulo de management incluido.

Vamos a levantarla mediante docker-compose ejecutando en el directorio raíz:

`docker-compose up -d`

Esto nos levanta la aplicación en el puerto **5672** (que está mapeado con nuestro puerto local, así que en localhost:5672 habrá un server de rabbit escuchando) y la UI de management en el puerto **15672**, a la que podremos acceder en la URL http://localhost:15672 con el user/pass por defecto que es *guest/guest*.


## Artículos interesantes

- [Tutoriales RabbitMQ](https://www.rabbitmq.com/getstarted.html)
- [AMQP 0-9-1 explicado](http://www.rabbitmq.com/tutorials/amqp-concepts.html)
- [ACK y Confirms](https://www.rabbitmq.com/confirms.html)
- [Reliability](https://www.rabbitmq.com/reliability.html)
- [Clustering](https://www.rabbitmq.com/clustering.html)

- [RabbitMQ en Mercado Libre](https://docs.google.com/document/d/1SX2DBTJ8pOYnrbM525AtJMFtg6_wZQBrMZOkxO1Qpt8/edit)


## Consola de Rabbit

- Exchanges declarados
>rabbitmqctl list_exchanges
- Bindings de las listas
>rabbitmqctl list_bindings
