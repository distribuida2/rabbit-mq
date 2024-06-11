#!/usr/bin/env python3

import pika


def callback(ch, method, properties, body):
    print("Routing key no ruteada | " + method.routing_key)
    ch.basic_ack(delivery_tag=method.delivery_tag)


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


channel.basic_consume(on_message_callback=callback, queue="unrouted_msg")

try:
    print(" [*] Esperando por mensajes no routeados. Para salir presione CTRL+C")
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()
connection.close()
