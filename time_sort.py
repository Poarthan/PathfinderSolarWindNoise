#!/usr/bin/env python3

import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy import fftpack
from datetime import datetime, timedelta
import time 
import math
from tqdm import tqdm


with open('2000_time_seconds.txt') as file:
    lines = file.readlines()
    lines = [line.rstrip() for line in lines]

sortlist=[]
for i in tqdm(range(len(lines))):
    sortlist.append(float(lines[i]))

sortlist.sort()

for i in tqdm(range(len(sortlist))):
    file = open('sorted_2000_time_seconds.txt',"a")
    file.write(str(sortlist[i]))
    file.write("\n")
    file.close()
