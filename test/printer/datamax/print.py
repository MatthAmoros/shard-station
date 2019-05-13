""""
	v0.1
	Print a single label
"""
import re
import socket

PATH_TO_LABEL = 'test_label_100_50.txt'
PRINTER = '192.168.2.152'  # Printer IP
PORT = 9100        # Printer Port
REPLACE_LIST = {'ID' : '1234567895',
 				'RECEPTION_DATE' : '10-05-2019',
				'PRODUCT_FAMILY' : 'CHERRY',
				'PRODUCT_TYPE' : 'SANTINA',
				'GROWER_GROUP' : '01',
				'ORIGIN' : 'GROWER',
				'DESTINATION' : 'STORE',
				'PRODUCT' : 'FRUTA GRANEL'}

def send():
	with open(PATH_TO_LABEL, 'r') as content_file:
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			content = content_file.read()
			content = replace_tags(content, REPLACE_LIST)

			s.connect((PRINTER, PORT))
			s.send(content.encode())

	print('Sent')

def replace_tags(content, value_list):
	pattern = re.compile(r"""<(?P<name>.*?)>""", re.VERBOSE)
	matches = pattern.findall(content)

	for match in matches:
		if match in value_list:
			content = content.replace("<" + match + ">", value_list[match])

	return content

send()
