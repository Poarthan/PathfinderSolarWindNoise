#!/usr/bin/env python3

import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy import fftpack
from datetime import datetime, timedelta
import time 
import math
from tqdm import tqdm

#load data
fnamedat='datafiles/g2_huge_file_ifft.dat'
cols=2
truncate=True

fnametimes='datafiles/g2_huge_file_times.dat'

ftimes='datafiles/gapfilldata/data_timefiles.txt'

if len(sys.argv) == 2:
    fnamedat = sys.argv[1]
elif len(sys.argv) == 3:
    fnamedat = sys.argv[1]
    cols = sys.argv[2]
elif len(sys.argv) == 4:
    fnamedat = sys.argv[1]
    cols = sys.argv[2]
    truncate = False
elif len(sys.argv) == 1:
    print("filling gaps")
else:
    sys.stderr.write(f'usage: {sys.argv[0]} [--gps] file.dat\n')
'''
if truncate==True:
    file = open(f'{fnamedat[:-4]}_radians_calculated_data.txt',"a")
    file.truncate(0)
    file.close()
'''
data=np.loadtxt(fname=fnamedat, usecols=range(cols))

n1=np.array(data[0:, 0])

n2=np.array(data[0:, 1])

data=np.loadtxt(fname=fnametimes)

tstuff=np.array(data)

#data=np.loadtxt(fname=ftimes)

#ftime=np.array(data)

def main():
    global n1, n2, ftime, tstuff 
    realadsf, finaltimes=general(n1, tstuff)
    imaginaryasdf, tmpbs=general(n2, tstuff)
    #assert(tmpbs==finaltimes)
    for i in tqdm(range(len(finaltimes))):
        write_file(finaltimes[i], n1[i], n2[i])


def general(numbers, times):
    global ftime
    with open(ftimes) as file:
        ftimess = file.readlines()
        ftimess = [line.rstrip() for line in ftimess]
    for i in range(len(ftimess)):
        print(f"datafiles/gapfilldata/{ftimess[i]}")
        ftime=np.loadtxt(fname=f"datafiles/gapfilldata/{ftimess[i]}")
        print(ftime)
        numbers, ftime, times=calculatedata(numbers, ftime, times)
    return numbers, times

def calculatedata(nn, ft, ti):    
    start=time.perf_counter()
    gap_array=np.array([])
    for i in tqdm(range(len(ft))):
        timespot=np.where(ti==ft[i])
        datapoint=nn[timespot[0]-1]
        gapFill=calculate_gapFill(ft[i], datapoint)
        gap_array=np.append(gap_array, gapFill)
    end=time.perf_counter()
    final=end-start
    start=time.perf_counter()
    sample_freq=16384/3276
    mid=len(ft)//2
    gap_count=ft[mid]-ft[mid-1]
    print(gap_count, "_G__A___P__C___O____U____N____T________________________")
    gap_count=gap_count/sample_freq
    prev_time_spot=ft[mid-1]
    for i in tqdm(range(int(gap_count))):
        fill_time_spot=prev_time_spot+sample_freq
        insert_spot=np.where(ti==prev_time_spot)
        ti=np.insert(ti, insert_spot[0]+1, fill_time_spot)
        #print(float(ti[insert_spot[0]]), float(ti[insert_spot[0]+1]), float(ti[insert_spot[0]+2]))
        #print(float(prev_time_spot), float(fill_time_spot))
        nn=np.insert(nn, insert_spot[0]+1, gap_array[i%len(gap_array)])
        prev_time_spot=fill_time_spot
    end=time.perf_counter()
    final=end-start
    print(final)
    return nn, ft, ti
    
def calculate_gapFill(val, dp):
    val=float(val)
    dp=float(dp)
    fill=math.pi*val
    fill2=fill/25
    cos=math.cos(fill2)
    gapFill2=0.5-(0.5*(cos))
    gapFill=gapFill2*dp
    return gapFill
    
def write_file(time, gap_fillr, gap_filli):
    print("writing to", f'{fnamedat[:-4]}_filled.txt')
    file = open(f'{fnamedat[:-4]}_filled.txt',"a")
    file.write(str(time))
    file.write("\t")
    file.write(str(gap_fillr))
    file.write("\t")
    file.write(str(gap_filli))
    file.write("\n")
    file.close()


if __name__ == '__main__':
    main()
