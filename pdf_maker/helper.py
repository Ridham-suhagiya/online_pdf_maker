import os 
import shutil
import numpy as np

def checker(path):
    isdir = os.path.isdir(path)
    if not isdir:
        os.makedirs(path)
    else:
        shutil.rmtree(path)
        os.makedirs(path)


def number(a):
    return int(a.split('-')[-1].split('.')[0])

def oneD_to_threeD(image):
    width = 1128
    height = 800
    out = np.empty((width, height, 3), dtype=np.uint8)
    out[:, :, 0] = image
    out[:, :, 1] = image
    out[:, :, 2] = image
    return out
