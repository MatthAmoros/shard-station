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
from instance.config import SHARD_ENDPOINT, SHARD_USERNAME, SHARD_PASSWORD
from lib.printer.zebra import Zebra
from lib.services.asset_loader import AssetLoader

""" Initialize connection """
credentials = pika.PlainCredentials(RABBITMQ_USERNAME, RABBITMQ_PASSWORD)
parameters = pika.ConnectionParameters(RABBITMQ_SERVER,
										RABBITMQ_PORT,
										'/',
										credentials)
asset_loader = AssetLoader(SHARD_ENDPOINT, SHARD_USERNAME, SHARD_PASSWORD)

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
			label = asset_loader.get_label(message['type'])
			printer.set_label(label_zpl=label)

			""" Bind a dictionnary of parameter to define label properties """
			printer.set_properties(message['parameters'])

			printer.set_property("ID", message['parameters']['code'])
			printer.set_property("ORIGIN", message['parameters']['location_origin']['name'])
			printer.set_property("PRODUCT_FAMILY", message['parameters']['variety']['specie']['name'])
			printer.set_property("PRODUCT_TYPE", message['parameters']['variety']['name'])
			printer.set_property("DESTINATION", message['parameters']['location_current']['name'])
			printer.set_property("PRODUCT", message['parameters']['packaging']['description'])

			printer.send(quantity=int(message['quantity']))

			channel.basic_ack(method.delivery_tag)
			print("Message sent.")

	channel.basic_consume(queue=RABBITMQ_QUEUE_NAME, on_message_callback=callback, auto_ack=False)
	""" Load labels from Shard """
	print("Loading labels from " + SHARD_ENDPOINT)

	print(" [*] Waiting for messages from queue '" + RABBITMQ_QUEUE_NAME + "'. To exit press CTRL+C ")
	channel.start_consuming()
except pika.exceptions.AMQPConnectionError:
	print(" [*] Could not establish connection to '" + RABBITMQ_QUEUE_NAME + "'. Shuting down. ")