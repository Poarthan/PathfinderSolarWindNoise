#!/usr/bin/env python3

#this file is used to calculate the times of the data for the whole time series
#and store the times into a file, allowing the plot making to program to have
#less computation to do

import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy import fftpack
from datetime import datetime, timedelta
import time
import os


huge_file_times = open('datafiles/lisa_times.dat',"a")

def main():
    with open('./datafiles/catalog/filenames_g2_z.txt') as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]
        for j in lines:
            gps=int(j[5:15])
            dur=int(j[16:21])
            num_lines = sum(1 for line in open(f'./datafiles/catalog/{j}'))
            print(gps)
            for i in range(num_lines*2+1):
                diff=dur/(num_lines*2)
                number=diff*i
                number=number+gps
                huge_file_times.write(str(number))
                huge_file_times.write('\n')

if __name__ == '__main__':
    main()
