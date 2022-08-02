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
cols=1
truncate=True
fnametimes='datafiles/lisa_times.dat'
#ftimes='datafiles/gapfilldata/data_timefiles.txt'
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

if truncate==True:
    file = open(f'datafiles/LISA_full_25_gf.txt',"a")
    file.truncate(0)
    file.close()

data=np.loadtxt(fname=fnamedat, usecols=range(1))
numbers=np.array(data)
data=np.loadtxt(fname=fnametimes)
times=np.array(data)
#data=np.loadtxt(fname=ftimes)
#ftime=np.array(data)
def main():
    global numbers, times, badtimes, diffthreshold
    finished=False
    begin=time.perf_counter()
    diffthreshold=16384/(3276*2)
    count=0
    check=True
    while finished==False:
        count+=1
        bad, check, bdlen, ifbad=checktimes()
        print("current count:",  count)
        if not check:
            print("GAP FILL DONE")
            break
        gap_count=int(bad[2]/diffthreshold)
        '''
        if not bdlen:
            n1=bad[3]-gap_count
            n2=bad[3]+gap_count
        else:
            fill_count=int(ifbad/diffthreshold)
            n1=bad[3]-fill_count
            n2=bad[3]+fill_count
        '''
        n1=bad[3]-25
        n2=bad[3]+25
        tmpset=numbers[n1:n2]
        tmptime=times[n1:n2]
        tmpd, tmpt=calculatedata(tmpset, bad[0], bad[1], bad[2], diffthreshold, tmptime)
        numbers=np.insert(numbers, bad[3]+1, tmpd)
        times=np.insert(times, bad[3]+1, tmpt)
    print("writing to", 'datafiles/LISA_full_25_gf.txt')
    for i in tqdm(range(numbers.size)):
        write_file(times[i], numbers[i])
    finalsfds=time.perf_counter()
    print(finalsfds-begin, "<- SECONDS THIS PROGRAM TOOK")

def checktimes():
    global numbers, times, badtimes, diffthreshold
    bbb=False
    whatthe=[]
    diffthreshold=16384/(3276*2)+0.2
    for i in range(times.size-1):
        a=float(times[i+1])
        b=float(times[i])
        diff=a-b
        if diff>diffthreshold:
            badset=[b, a, diff, i]
            bbb=True
            whatthe.append(badset)
#            break
    print(len(whatthe))
    badlen=False
    if bbb==False:
        return "KEKKED", bbb, "KEKKED", "KEKKED"
    if len(whatthe)>1:
        space=whatthe[1][0]-whatthe[0][2]-whatthe[0][1]
        if space < 0:
            badlen=True
    
    else:
        space=times[-1]-whatthe[0][2]-whatthe[0][1]
        if space < 0:
            badlen=True
    if len(whatthe)>1:
        return whatthe[0], bbb, badlen, whatthe[1][0]-whatthe[0][1]
    else:
        return whatthe[0], bbb, badlen, times[-1]-whatthe[0][1]
def calculatedata(tmp, tstart, tend, tdiff, diffthresh, ttime):    
    global numbers, times
    start=time.perf_counter()
    gap_array=np.array([])
    sample_freq=diffthresh
    gap_count=tdiff/sample_freq
    gc=int(gap_count)
    prev_time_spot=tstart
    print("Gap Count:", gap_count, gc, tdiff)
#    print(tmp.size, "asdfadsf")
    x1=tmp[tmp.size//2-1]
    x2=tmp[tmp.size//2]
    z=(x2-x1)/gap_count
    hanning=np.hanning(tmp.size//2)
    for i in range(tmp.size//2):
        gapFill=hanning[i]*tmp[i]+x1+z*(i+1)
        gap_array=np.append(gap_array, gapFill)
    xtime=np.array([])
    xtmp=np.array([])
    for i in tqdm(range(int(gap_count))):
        fill_time_spot=prev_time_spot+sample_freq
        xtime=np.append(xtime, fill_time_spot)
        xtmp=np.append(xtmp, gap_array[i%len(gap_array)])
        prev_time_spot=fill_time_spot
    #print(tmp, ttime)
    end=time.perf_counter()
    final=end-start
    print(final)
    return xtmp, xtime
    
def calculate_gapFill(val, dp):    
    val=float(val)
    dp=float(dp)
    fill=math.pi*val
    fill2=fill/25
    cos=math.cos(fill2)
    gapFill2=0.5-(0.5*(cos))
    gapFill=gapFill2*dp
    return gapFill
    
def write_file(time, gap_fill):
    file = open('datafiles/LISA_full_25_gf.txt',"a")
    file.write(str(time))
    file.write("\t")
    file.write(str(gap_fill))
    file.write("\n")
    file.close()
if __name__ == '__main__':
    main()
