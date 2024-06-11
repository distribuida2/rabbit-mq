#!/usr/bin/env python3
import pika
import sys
import random

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost"))
channel = connection.channel()

channel.exchange_declare(exchange='unrouted_exchange', exchange_type='fanout')

channel.exchange_declare(exchange='task_exchange', exchange_type='direct', arguments={
                         "alternate-exchange": "unrouted_exchange"})

channel.queue_declare(queue="task_queue", durable=True)
channel.queue_bind("task_queue", "task_exchange", "work")

channel.queue_declare(queue="unrouted_msg", durable=True)
channel.queue_bind("unrouted_msg", "unrouted_exchange")


message = "work bitch!"
routing_key = " ".join(sys.argv[1:]) or "work"
channel.basic_publish(
    exchange="task_exchange",
    routing_key=routing_key,
    body=message,
    properties=pika.BasicProperties(
        # necesario si queremos que los mensajes sean persistentes
        delivery_mode=2,
        headers={"message_id": str(random.randrange(1, 1000))},
    ),
)
print("Mensaje enviado - %r" % message)
connection.close()
