#!/usr/bin/env python3

import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy import fftpack
from datetime import datetime, timedelta
import time 
import math
from tqdm import tqdm

fnamedat="../datafiles/ACE_time_seconds.txt"

if len(sys.argv) == 2:
    fnamedat = sys.argv[1]

with open(fnamedat) as file:
    lines = file.readlines()
    lines = [line.rstrip() for line in lines]

for i in tqdm(range(len(lines))):
    if float(lines[i+1])-float(lines[i])<0:
        print(lines[i+1], lines[i], float(lines[i+1])-float(lines[i]))
