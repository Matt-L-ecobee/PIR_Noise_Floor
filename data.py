import logging
import pandas as pd
import matplotlib.pyplot as plt
from datetime import time

from hardware import Tstat

logging.basicConfig(format='[%(module)s] %(asctime)-12s %(levelname)s - %(message)s',
                    datefmt='%y-%m-%d %H:%M:%S',
                    level=logging.DEBUG,
                    filename='logs/noiseFloorTest.log',
                    filemode='w'
                    )


class Compiler:

    device = Tstat('/dev/ttyUSB0')
    
    def __init__(self):
        logging.debug("Data compiler created")
        self.sensor_data = {}
        
    def _is_data_full(self,data_points):
        for sensor in self.sensor_data:
            if len(self.sensor_data[sensor].index) < data_points:
                logging.debug(f"{sensor} doesn't have enough data points")
                return False
            logging.debug(f"{sensor} has enough data points")
        return True
        
    def add_sensor(self, sensor_id):
        if type(sensor_id) == str:
            data = {"time":[],"raw_temp":[],"weight":[]}
            df = pd.DataFrame(data)
            self.sensor_data[sensor_id] = df
            logging.debug(f"Created data frame for {sensor_id}")
        else:
            loggin.error(f"{sensor_id} is not a string")
            
    def collect_data(self, data_points = 5):
        logging.info("Data collection started")
        while not self._is_data_full(data_points):
            readout = self.device.read_console(10)
            print(readout)
            readout_lines = readout.split("\n")
            for line in readout_lines:
                parsed_line = line.split(" ")
                print(parsed_line)
                if len(parsed_line)>2 and parsed_line[3] in self.sensor_data:
                    time_string = parsed_line[1].split(':')
                    recorded_time = time(int(time_string[0]),int(time_string[1]),int(time_string[2].split('.')[0]))
                    new_entry = pd.Series(data={"time":recorded_time,
                                                "raw_temp":int(parsed_line[5].split("=")[1]),
                                                "weight":float(parsed_line[7].split("=")[1])
                                                })
                    self.sensor_data[parsed_line[3]] = self.sensor_data[parsed_line[3]].append(new_entry, ignore_index=True)
                    logging.debug(f"Data for {parsed_line[3]} has been added")
        logging.info("Data collection ended")
        
    def plot_results(self,sensor_id):
        try:
            logging.info(f"Plotting line graph for {sensor_id}")
            self.sensor_data[sensor_id].plot(kind = 'line', x="time", y="raw_temp")
            plt.show()
        except KeyError:
            print(f"{sensor_id} is not a valid sensor id")
        except TypeError:
            print("No data available to plot")
        
    def plot_histogram(self,sensor_id):
        try:
            logging.info(f"Plotting histogram for {sensor_id}")
            self.sensor_data[sensor_id].hist(column="raw_temp", grid=False)
            plt.show()
        except KeyError:
            print(f"{sensor_id} is not a valid sensor id")
        except TypeError:
            print("No data available to plot")
        
    def export_data(self):
        for frame in self.sensor_data:
            logging.info(f"Exporting {frame} data to csv")
            self.sensor_data[frame].to_csv("out/"+frame+"_data.csv", index=False, sep='\t',float_format='%.2f')