import machine
# boot.py -- run on boot-up
machine.Pin(13, machine.Pin.OUT).value(0)
machine.Pin(15, machine.Pin.OUT).value(0)
machine.Pin(14, machine.Pin.OUT).value(0)
