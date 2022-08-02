import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy import fftpack

def main():
    with open('datafiles/ACE_time.txt') as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]
        for j in lines:
            time=j.split(" ")
            d=int(time[1])
            h=int(time[2])
            m=int(time[3])
            s=float(time[4])
            #print(j)
            #print("2000", d, h, m, s)
            i= 1136073619 + ((d-6)*86400) + (h*3600)+(m*60)+s
            file = open('ACE_time_seconds.txt',"a")
            file.write(str(i))
            file.write("\n")
            file.close()
            #exit()

main()
