"""
TODO :

Start a RabbitMQ Client
Get message, behave, answer
"""
#!/usr/bin/env python
import pika
import json
from instance.config import RABBITMQ_SERVER, RABBITMQ_QUEUE_NAME, RABBITMQ_PORT, RABBITMQ_USERNAME, RABBITMQ_PASSWORD
from lib.printer.zebra.zebra import Zebra

""" Initialize connection """
credentials = pika.PlainCredentials(RABBITMQ_USERNAME, RABBITMQ_PASSWORD)
parameters = pika.ConnectionParameters(RABBITMQ_SERVER,
										RABBITMQ_PORT,
										'/',
										credentials)

connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.queue_declare(queue=RABBITMQ_QUEUE_NAME)

def callback(ch, method, properties, body):
	message = json.loads(body)
	message['parameters'] = json.loads(message['parameters'])

	printer = Zebra("Zebra01", "192.168.2.150", 9100)

	""" Bind label properties """
	printer.set_property("ID", message['parameters']['code'])
	printer.set_property("ORIGIN", message['parameters']['location_origin']['name'])

	printer.send()

	channel.basic_ack(method.delivery_tag)
	print("Message sent.")

channel.basic_consume(queue=RABBITMQ_QUEUE_NAME, on_message_callback=callback, auto_ack=False)

print(" [*] Waiting for messages from queue '" + RABBITMQ_QUEUE_NAME + "'. To exit press CTRL+C ")
channel.start_consuming()
