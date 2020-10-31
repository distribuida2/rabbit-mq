#!/usr/bin/env python3

import pika


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)


connection = pika.BlockingConnection()
channel = connection.channel()
channel.queue_declare(queue='hello')

channel.basic_consume(on_message_callback=callback,
                      queue='hello', auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
