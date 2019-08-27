"""
TODO :

Start a RabbitMQ Client
Get message, behave, answer
"""
#!/usr/bin/env python
import pika

queue_name = 'shard'
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue=queue_name)

def callback(ch, method, properties, body):
	print(" [x] Received %r" % body)

channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

print(" [*] Waiting for messages from queue '" + queue_name + "'. To exit press CTRL+C ")
channel.start_consuming()
