from lib.printer.zebra.zebra import Zebra

printer = Zebra("Zebra01", "192.168.2.150", 9100)

printer.send()
