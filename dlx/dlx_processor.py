#!/usr/bin/env python3

import pika

republished_key = 'republished'


def estrategia_casos_raros(ch, method, properties, body):
    print('[DLQ] Problema raro. Reencolamos.')


def estrategia_rejected(ch, method, properties, body):
    print('[DLQ] Problema técnico. Revisar. Body: %r' % body.decode())
    channel.basic_ack(delivery_tag=method.delivery_tag)


def republish(ch, method, properties, body):
    channel.basic_ack(delivery_tag=method.delivery_tag)
    original_queue = properties.headers['x-first-death-queue']
    original_exchange = properties.headers['x-first-death-exchange']
    headers_to_republish = {republished_key: True}
    channel.basic_publish(exchange=original_exchange,
                          routing_key=original_queue,
                          body=body,
                          properties=pika.BasicProperties(
                              delivery_mode=2,
                              headers=headers_to_republish,
                              )
                          )
    print('[DLQ] Reencolamos con header republicado. Body: %r' % body.decode())


def callback(ch, method, properties, body):
    # en este punto, mediante headers y flags podemos controlar la estrategia
    is_republished = republished_key in properties.headers
    if is_republished:
        reason = properties.headers['x-death'][0]['reason']
        if reason != 'rejected':
            estrategia_casos_raros(ch, method, properties, body)
        else:
            estrategia_rejected(ch, method, properties, body)
    else:
        republish(ch, method, properties, body)


connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

print(' [*] Esperando mensajes en la retry queue...')

channel.queue_bind(queue='retry_queue', exchange='retry_exchange')
channel.basic_consume(on_message_callback=callback,
                      queue='retry_queue')

try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()
connection.close()
