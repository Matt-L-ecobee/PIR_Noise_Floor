import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import time

from hardware import Tstat, RPi
from test_logs import setup_logger


class Compiler:
    device = Tstat('/dev/ttyUSB0')
    board = RPi()

    def __init__(self, test_number):
        self.test_number = test_number
        self.sensor_data = {}

        path = os.path.join('/home/pi/Desktop/PIR_Noise_Floor_Test/out', f'test_{test_number}')
        os.mkdir(path)
        path = os.path.join(path, 'logs')
        os.mkdir(path)

        self.action_logger = setup_logger('test_action_logger', f'out/test_{test_number}/logs/test_actions.log')
        self.console_logger = setup_logger('console_logger', f'out/test_{test_number}/logs/console.log')

        self.action_logger.debug("Data compiler created")
        print("logs set")

    def _is_data_full(self, data_points):
        for sensor in self.sensor_data:
            if len(self.sensor_data[sensor].index) < data_points:
                self.action_logger.debug(f"{sensor} doesn't have enough data points")
                return False
            self.action_logger.debug(f"{sensor} has enough data points")
        return True

    def _clear_data(self, sensor_id):
        data = {"time": [], "raw_temp": [], "pir": []}
        df = pd.DataFrame(data)
        self.sensor_data[sensor_id] = df
        self.action_logger.debug(f"Data cleared for {sensor_id}")

    def add_sensor(self, sensor_id):
        if type(sensor_id) == str:
            data = {"time": [], "raw_temp": [], "pir": []}
            df = pd.DataFrame(data)
            self.sensor_data[sensor_id] = df
            self.action_logger.debug(f"Created data frame for {sensor_id}")
            print(f"Added sensor for {sensor_id}")
            self.new_export(sensor_id)
        else:
            self.action_logger.error(f"{sensor_id} is not a string")

    def collect_data(self, data_points=5):
        self.action_logger.debug("Collecting Data")
        if data_points == 0:
            readout = self.device.read_console()
            self.console_logger.info(readout.strip('\n'))
            parsed_line = readout.split(" ")
            if len(parsed_line) > 3 and parsed_line[3] == "RSv2L,":
                self.board.blink(1,1)
                data_packet = parsed_line[4].split(',')
                print(f"Packet: {data_packet}")
                if len(data_packet) > 5:
                    if data_packet[4] in self.sensor_data:
                        time_string = data_packet[2].split(':')
                        recorded_time = time(int(time_string[0]), int(time_string[1]),
                                            int(time_string[2]))
                        new_entry = pd.Series(data={"time": recorded_time,
                                                    "raw_temp": int(data_packet[7]),
                                                    "pir": int(data_packet[9])
                                                    })
                        self.sensor_data[data_packet[4]] = self.sensor_data[data_packet[4]].append(new_entry,
                                                                                                   ignore_index=True)
                        self.action_logger.info(f"Data for {data_packet[4]} has been added")

                        self.export_data()
                    else:
                        self.add_sensor(str(data_packet[4]))

        else:
            while not self._is_data_full(data_points):
                readout = self.device.read_console()
                parsed_line = readout.split(" ")
                if len(parsed_line) > 3 and parsed_line[3] == "RSv2L,":
                    data_packet = parsed_line[4].split(',')
                    print(f"Packet: {data_packet}")
                    if len(data_packet) > 5 and data_packet[4] in self.sensor_data:
                        time_string = parsed_line[1].split(':')
                        recorded_time = time(int(time_string[0]), int(time_string[1]),
                                             int(time_string[2].split('.')[0]))
                        new_entry = pd.Series(data={"time": recorded_time,
                                                    "raw_temp": int(data_packet[7]),
                                                    "pir": int(data_packet[9])
                                                    })
                        self.sensor_data[data_packet[4]] = self.sensor_data[data_packet[4]].append(new_entry,
                                                                                                   ignore_index=True)
                        self.action_logger.info(f"Data for {data_packet[4]} has been added")

    def new_export(self, sensor_id):
        self.action_logger.info(f"Creating csv file for {sensor_id} data")
        print(f"Created file for {sensor_id} data")
        self.sensor_data[sensor_id].to_csv(f'out/test_{self.test_number}/{sensor_id}_data.csv', index=False,
                                        sep=',',
                                        float_format='%.2f')

    def export_data(self):
        for frame in self.sensor_data:
            self.action_logger.info(f"Exporting {frame} data to csv")
            self.sensor_data[frame].to_csv(f'out/test_{self.test_number}/{frame}_data.csv', index=False,
                                           sep=',',
                                           float_format='%.2f', mode='a', header=False)
            self._clear_data(frame)
