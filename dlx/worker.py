#!/usr/bin/env python3

import pika
import time

count = 0


def callback(ch, method, properties, body):
    global count
    print(" [x] Recibido y procesando %d %r" % (method.delivery_tag, body))
    time.sleep(2)
    str_body = body.decode()
    if str_body[0] == 'n':
        ch.basic_reject(delivery_tag=method.delivery_tag, requeue=False)
        print(" [x] Rechazado %d" % method.delivery_tag)
    else:
        ch.basic_ack(delivery_tag=method.delivery_tag)
        print(" [x] Procesado %d" % method.delivery_tag)
    count = count + 1


connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='work_exchange', exchange_type='direct')
channel.exchange_declare(exchange='retry_exchange', exchange_type='direct')
channel.queue_declare(
    queue='work_queue',
    durable=True,
    arguments={
        "x-dead-letter-exchange": "retry_exchange",
        "x-dead-letter-routing-key": "retry_queue",
        "x-message-ttl": 10000
    }
)
channel.queue_bind(queue='work_queue', exchange='work_exchange')
channel.queue_declare(queue='retry_queue', durable=True,)
channel.queue_bind(queue='retry_queue', exchange='retry_exchange')

print(' [*] Esperando mensajes para procesar...')

channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_message_callback=callback,
                      queue='work_queue')

try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()
connection.close()
