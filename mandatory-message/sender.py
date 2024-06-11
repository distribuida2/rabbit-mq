#!/usr/bin/env python3

import sys
import pika
import time

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
# Función de callback para manejar los mensajes no enrutados


def on_return_callback(channel, method, properties, body):
    print(f"Mensaje no enrutado: {body}")


# Configurar el callback para mensajes no enrutados
channel.add_on_return_callback(on_return_callback)

channel.queue_declare(queue='hello')

routing_key = " ".join(sys.argv[1:]) or "hello"

channel.basic_publish(exchange='',
                      routing_key=routing_key,
                      body='Hola mundo!',
                      mandatory=True)

print(f'"Hola mundo enviado a {routing_key}!"')

try:
    print("Esperando por mensajes no enrutados. Presiona Ctrl+C para salir.")
    connection.process_data_events(time_limit=3)
except KeyboardInterrupt:
    print("Interrupción del usuario. Cerrando conexión...")
finally:
    connection.close()
    print("Conexión cerrada.")
