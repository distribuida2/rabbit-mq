#!/usr/bin/env python3

import pika
import time


def callback(ch, method, properties, body):
    print(" [x] Recibido y procesando %d %r" % (method.delivery_tag, body))
    time.sleep(5)
    print(" [x] Procesado! %d" % method.delivery_tag)
    ch.basic_reject(delivery_tag=method.delivery_tag, requeue=False)


connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()
channel.queue_declare(
    queue='task_queue',
    durable=True,
    arguments={
        "x-dead-letter-exchange": "dlx",
        "x-dead-letter-routing-key": "dead_letter_queue",
        "x-message-ttl": 1000
    }
)
print(' [*] Esperando mensajes PARA RECHAZARLOS, MUEJEJE (?)')

channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_message_callback=callback,
                      queue='task_queue')

try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()
connection.close()
