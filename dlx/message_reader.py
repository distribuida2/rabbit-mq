#!/usr/bin/env python3

import pika


def callback(ch, method, properties, body):
    print(" [x] Received DLX %r" % body)
    reason = properties.headers['x-death'][0]['reason']
    if reason != 'rejected':
        print('Problema técnico. Revisar')
    channel.basic_ack(delivery_tag=method.delivery_tag)


connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()
channel.exchange_declare(exchange='dlx', exchange_type='direct')

channel.queue_declare(queue='dead_letter_queue', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')

channel.queue_bind(queue='dead_letter_queue', exchange='dlx')

#channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_message_callback=callback,
                      queue='dead_letter_queue')

try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()
connection.close()
