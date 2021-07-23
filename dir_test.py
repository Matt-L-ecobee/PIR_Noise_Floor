import os

rootdir = '/home/pi/Desktop/PIR_Noise_Floor_Test/out'

for it in os.scandir(rootdir):
    if it.is_dir():
        folder = it.path.split('/')[-1]
        test_number = str(folder.split('_')[-1])