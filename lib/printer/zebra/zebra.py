""""
	v0.1
	Print a single label
	v0.2
	Factorized to a class
"""

__all__ = ['Zebra']
__version__ = '0.2'

import re
import socket
from lib.printer.printer import Printer

class Zebra(Printer):
	PATH_TO_LABEL = 'lib/printer/zebra/test_label_100_50.txt'
	REPLACE_LIST = {'ID' : '1234567895',
	 				'RECEPTION_DATE' : '10-05-2019',
					'PRODUCT_FAMILY' : 'CHERRY',
					'PRODUCT_TYPE' : 'SANTINA',
					'GROWER_GROUP' : '01',
					'ORIGIN' : 'GROWER',
					'DESTINATION' : 'STORE',
					'PRODUCT' : 'FRUTA GRANEL'}

	def send(self):
		print('Sending label to : ' + str(self.ip_address) + ':' + str(self.port) + ' ...')
		with open(self.PATH_TO_LABEL, 'r') as content_file:
			with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
				content = content_file.read()
				content = self.replace_tags(content, self.REPLACE_LIST)

				s.connect((self.ip_address, self.port))
				s.send(content.encode())

		print('Sent')

	def set_property(self, key, value):
		self.REPLACE_LIST[key] = value

	def replace_tags(self, content, value_list):
		pattern = re.compile(r"""<(?P<name>.*?)>""", re.VERBOSE)
		matches = pattern.findall(content)

		for match in matches:
			if match in value_list:
				content = content.replace("<" + match + ">", value_list[match])

		return content
