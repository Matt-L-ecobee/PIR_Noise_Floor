import serial
import logging
from time import sleep

logging.basicConfig(format='[%(module)s] %(asctime)-12s %(levelname)s - %(message)s',
                    datefmt='%y-%m-%d %H:%M:%S',
                    level=logging.INFO,
                    filename='logs/noiseFloorTest.log',
                    filemode='w'
                    )

class Tstat:
    
    def __init__(self, device_port):
        logging.debug(f"Connecting to Tstat console on {device_port}")
        try:
            self.ser = serial.Serial(port=device_port, baudrate=921600)
            self.ser.reset_input_buffer()
            self.ser.reset_output_buffer()
            logging.info("Connected to Tstat on {device_port}")
        except serial.SerialException:
            logging.error(f"Unable to connect to Tstat on {device_port}")
            
    def __del__(self):
        self.ser.close()
        logging.info("Disconnected from Tstat")
        
    def read_console(self, lines=30):
        output = ""
        try:
            logging.info("Reading from Tstat console")
            for i in range(lines):
                raw_bytes = self.ser.readline()
                output += str(raw_bytes.decode("utf-8"))
                logging.debug("Line read")
        
        except KeyboardInterrupt:
            logging.info("Finished reading from console")
        
        return output
