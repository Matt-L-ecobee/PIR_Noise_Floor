from hardware import Tstat

device = Tstat('/dev/ttyUSB0')
print(device.read_console(5))