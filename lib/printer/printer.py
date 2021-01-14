class Printer:
	def __init__(self, name, ip_address, port, interface='tcp'):
		assert(interface in ['usb', 'tcp'])
		self.name = str(name)
		self.ip_address = str(ip_address)
		self.port = port
		self.interface = interface

	def send(self):
		raise NotImplementedError('send must be overloaded')

	def replace_tags(self, content, value_list):
		raise NotImplementedError('replace_tags must be overloaded')

	def set_properties(self, properties):
		raise NotImplementedError('set_properties must be overloaded')