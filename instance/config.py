#!/usr/bin/python

RABBITMQ_SERVER = "localhost"
RABBITMQ_PORT = 5672
RABBITMQ_QUEUE_NAME = "shard"
RABBITMQ_USERNAME = "admin"
RABBITMQ_PASSWORD = "SomePassword"

""" Should be a shard network wide unique ID (could be MAC address) """
STATION_ID = 'printer-01'

""" Printer configuration """
""" usb or tcp """
PRINTER_INTERFACE = 'usb'
PRINTER_NAME = 'ZDesigner GK420t'
PRINTER_IP_ADDRESS = '192.168.1.10'
PRINTER_PORT = '9100'
