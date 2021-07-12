from os import path
import pandas as pd
import matplotlib.pyplot as plt

cmd = str(input("Enter the sensor and test to plot [sensor_id test_number]: "))
sensor_id, test_number = cmd.split(" ")

filepath = f'out/test_{test_number}/'
datafile = f'{sensor_id}_data.csv'
graphfile = f'{sensor_id}_graph.png'
histfile = f'{sensor_id}_histogram.png'

data = pd.read_csv(path.join(filepath, datafile), sep=',')

data.plot(kind='line', x="time", y="pir")
plt.xlabel('Time')
plt.savefig(path.join(filepath, graphfile))
plt.close()

data["pir"].plot.hist(bins=60)
plt.savefig(path.join(filepath, histfile))
