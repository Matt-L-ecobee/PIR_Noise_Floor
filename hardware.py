import serial
import os
from time import sleep


class Tstat:

    def __init__(self, device_port):
        print(f"Connecting to Tstat console on {device_port}")
        board = RPi()
        try:
            board.led_on()
            self.ser = serial.Serial(port=device_port, baudrate=921600)
            self.ser.reset_input_buffer()
            self.ser.reset_output_buffer()
            print("Connected to Tstat on {device_port}")
            board.led_off()
        except serial.SerialException:
            print(f"Unable to connect to Tstat on {device_port}")
            board.blink(20,0.2)

    def __del__(self):
        self.ser.close()

    def read_console(self):
        output = ""
        raw_bytes = self.ser.readline()
        output += str(raw_bytes.decode("utf-8"))
        return output
    
class RPi:
    
    on = 'echo 1 | sudo dd status=none of=/sys/class/leds/led0/brightness'
    off = 'echo 0 | sudo dd status=none of=/sys/class/leds/led0/brightness'

    def led_on(self):
        os.system(self.on)
        
    def led_off(self):
        os.system(self.off)
        
    def blink(self, cycles, cadence):
        for i in range(cycles):
            self.led_on()
            sleep(cadence)
            self.led_off()
            sleep(cadence)