"""
TODO :

Start a RabbitMQ Client
Get message, behave, answer
"""
#!/usr/bin/env python
import pika
import json
from instance.config import STATION_ID
from instance.config import RABBITMQ_SERVER, RABBITMQ_QUEUE_NAME, RABBITMQ_PORT, RABBITMQ_USERNAME, RABBITMQ_PASSWORD
from instance.config import PRINTER_INTERFACE, PRINTER_IP_ADDRESS, PRINTER_PORT, PRINTER_NAME
from lib.printer.zebra import Zebra

""" Initialize connection """
credentials = pika.PlainCredentials(RABBITMQ_USERNAME, RABBITMQ_PASSWORD)
parameters = pika.ConnectionParameters(RABBITMQ_SERVER,
										RABBITMQ_PORT,
										'/',
										credentials)

try:
	connection = pika.BlockingConnection(parameters)
	channel = connection.channel()

	channel.queue_declare(queue=RABBITMQ_QUEUE_NAME)

	def callback(ch, method, properties, body):
		message = json.loads(body)

		if 'target' in message and message['target'] == STATION_ID:
			message['parameters'] = json.loads(message['parameters'])

			printer = Zebra(PRINTER_NAME, PRINTER_IP_ADDRESS, PRINTER_PORT, PRINTER_INTERFACE)

			""" Bind label properties """
			printer.set_property("ID", message['parameters']['code'])
			printer.set_property("ORIGIN", message['parameters']['location_origin']['name'])
			printer.set_property("PRODUCT_FAMILY", message['parameters']['product_type']['product_family']['name'])
			printer.set_property("PRODUCT_TYPE", message['parameters']['product_type']['name'])
			printer.set_property("DESTINATION", message['parameters']['location_current']['name'])
			printer.set_property("PRODUCT", message['parameters']['packaging']['description'])

			printer.send()

			channel.basic_ack(method.delivery_tag)
			print("Message sent.")

	channel.basic_consume(queue=RABBITMQ_QUEUE_NAME, on_message_callback=callback, auto_ack=False)

	print(" [*] Waiting for messages from queue '" + RABBITMQ_QUEUE_NAME + "'. To exit press CTRL+C ")
	channel.start_consuming()
except pika.exceptions.AMQPConnectionError:
	print(" [*] Could not establish connection to '" + RABBITMQ_QUEUE_NAME + "'. Shuting down. ")