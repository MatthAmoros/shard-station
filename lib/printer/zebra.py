""""
	v0.1
	Print a single label
	v0.2
	Factorized to a class
"""
__all__ = ['Zebra']
__version__ = '0.3'

"""
This class handles communication with Zebra printer.
"""

""" For Windows USB only """
import os, sys
import win32print

import re
import socket
from lib.printer.printer import Printer

class Zebra(Printer):
	REPLACE_LIST = {}

	__content = ''

	""" Send self.__content to printer according to interface and parameters """
	def send(self, quantity=1):
		""" Replace label tags with values """
		populated_label_zpl = self.replace_tags(self.__content, self.REPLACE_LIST)
		
		printed_quantity = 0
		while printed_quantity < quantity:
			if self.interface == 'tcp':
				print('Sending label to : ' + str(self.ip_address) + ':' + str(self.port) + ' ...')
				with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
					s.connect((self.ip_address, self.port))
					s.send(populated_label_zpl.encode())
			elif self.interface == 'usb':
				print("Sending label through USB")

				if sys.version_info >= (3,):
				  raw_data = bytes (populated_label_zpl, "utf-8")
				else:
				  raw_data = populated_label_zpl

				hPrinter = win32print.OpenPrinter (self.name)
				try:
					hJob = win32print.StartDocPrinter (hPrinter, 1, ("Shard Label", None, "RAW"))
					try:
						win32print.StartPagePrinter (hPrinter)
						win32print.WritePrinter (hPrinter, raw_data)
						win32print.EndPagePrinter (hPrinter)
					finally:
						win32print.EndDocPrinter (hPrinter)
				finally:
					win32print.ClosePrinter (hPrinter)
			else:
				print("Interface not defined")

			printed_quantity = printed_quantity + 1

		print('Sent')

	def set_property(self, key, value):
		self.REPLACE_LIST[key] = value

	def set_properties(self, properties):
		for prop in properties:
			self.REPLACE_LIST[prop] = properties[prop]

	def set_label(self, label_zpl):
		self.__content = label_zpl

	def replace_tags(self, content, value_list):
		pattern = re.compile(r"""<(?P<name>.*?)>""", re.VERBOSE)
		matches = pattern.findall(content)

		for match in matches:
			try:
				if '.' in match:
					""" If we have a property accesor """
					property_patch = match.split('.')
					my_prop = value_list
					for node in property_patch:
						my_prop = my_prop[node]
					content = content.replace("<" + match + ">", my_prop)
				elif match in value_list:
					""" Directly access property """
					content = content.replace("<" + match + ">", value_list[match])
			except:
				print("Property skipped: " + str(match))

		return content