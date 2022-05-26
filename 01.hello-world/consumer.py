#!/usr/bin/env python3

import pika


def callback(ch, method, properties, body):
    print(" [x] Received %r" % str(body))


connection = pika.BlockingConnection()
channel = connection.channel()
channel.queue_declare(queue='hello')

channel.basic_consume(on_message_callback=callback,
                      queue='hello')

try:
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()
connection.close()
