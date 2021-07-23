from data import Compiler
from hardware import RPi
import os

board = RPi()
rootdir = '/home/pi/Desktop/PIR_Noise_Floor_Test/out'

last_test = 0

for it in os.scandir(rootdir):
    if it.is_dir():
        folder = it.path.split('/')[-1]
        test_number = int(folder.split('_')[-1])
        if test_number > last_test:
            last_test = test_number


x = Compiler(last_test+1)

board.blink(3,0.5)
while True:
    x.collect_data(0)
