from lib.printer.printer import Printer
from lib.printer.zebra.zebra import Zebra

printer = Zebra("Zebra01", "192.168.2.50", 9100)

printer.send()
