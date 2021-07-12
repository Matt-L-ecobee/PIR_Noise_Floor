import serial
import logging

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

    def read_console(self):
        output = ""
        logging.debug("Reading from Tstat console")
        raw_bytes = self.ser.readline()
        output += str(raw_bytes.decode("utf-8"))
        return output
