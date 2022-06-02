#!/usr/bin/env python3
import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()


message = ' '.join(sys.argv[1:]) or "Hello World!"
channel.basic_publish(exchange='work_exchange',
                      routing_key='work_queue',
                      body=message,
                      properties=pika.BasicProperties(delivery_mode=2,))
print(" [x] Enviando mensaje a la cola de trabajo %r" % message)
connection.close()
