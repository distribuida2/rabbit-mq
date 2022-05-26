#!/usr/bin/env python3

import pika


def callback(ch, method, properties, body):
    print(" [x] %r" % body)


connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs',
                         exchange_type='fanout')

result = channel.queue_declare(
    queue='queue_logs',
    exclusive=True,
    durable=True
)
queue_name = result.method.queue

channel.queue_bind(exchange='logs',
                   queue=queue_name)


channel.basic_consume(on_message_callback=callback,
                      queue=queue_name)

try:
    print(' [*] Esperando por mensajes. Para salir presione CTRL+C')
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()
connection.close()
