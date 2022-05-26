#!/usr/bin/env python3

import pika
import time


def callback(ch, method, properties, body):
    print(" [x] Recibido %r" % body)
    message = str(body)
    if "urgente" in message:
        print("Tarea urgente. Rechazada.")
        ch.basic_reject(delivery_tag=method.delivery_tag)
    time.sleep(4)
    print(" [x] Procesado %r" % body)
    ch.basic_ack(delivery_tag=method.delivery_tag)


connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)

# channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_message_callback=callback,
                      queue='task_queue')

try:
    print(' [*] Esperando por mensajes. Para salir presione CTRL+C')
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()
connection.close()
