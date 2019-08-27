class Printer:
	def __init__(self, name, ip_address, port):
		self.name = str(name)
		self.ip_address = str(ip_address)
		self.port = port

	def send(self):
		raise NotImplementedError('send must be overloaded')

	def replace_tags(self, content, value_list):
		raise NotImplementedError('replace_tags must be overloaded')
