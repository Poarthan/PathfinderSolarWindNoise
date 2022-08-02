import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy import fftpack

def main():
    file = open('datafiles/ACE_time_seconds.txt',"a")
    file.truncate(0)
    file.close()
    with open('datafiles/ACE_data.txt') as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]
        lines = lines[31:]
        print(lines[0:10])
        for j in lines:
            time=[]
            data=j.split('  ')
            for thing in data:
                tmpdata=thing.split(" ")
                for tmp in tmpdata:
                    time.append(tmp)

            time = list(filter(None,time))
            print(time)
            d=int(time[0])
            h=int(time[1])
            m=int(time[2])
            s=float(time[3])
            i= 1135641617 + ((d-6)*86400) + (h*3600)+(m*60)+s
            file = open('datafiles/ACE_time_seconds.txt',"a")
            file.write(str(i))
            file.write("\n")
            file.close()
            #exit()

main()
