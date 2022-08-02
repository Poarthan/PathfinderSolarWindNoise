#!/usr/bin/env python3

import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy import fftpack
from datetime import datetime, timedelta
import time 

#load data
fnamedat='datafiles/LISA_full_gf.txt'
cols=2
#fnametimes='datafiles/g1_huge_file_times.dat'

if len(sys.argv) == 2:
    fnamedat = sys.argv[1]# they can override the file name
    #fnametimes = sys.argv[2]
elif len(sys.argv) == 3:
    fnamedat = sys.argv[1]
    #fnametimes = sys.argv[2]
    cols = sys.argv[3]
else:
    sys.stderr.write(f'usage: {sys.argv[0]} [--gps] file.dat\n')
        
data=np.loadtxt(fname=fnamedat, usecols=range(cols))

#splitting data into individual colums
time=np.array(data[0:, 0])
combined=np.array(data[0:, 1])
#imaginary=np.array(data[0:, 2])

#data parse check
np.set_printoptions(suppress=True, precision=30)
#print(time, combined, imaginary)

#time_stuff=np.loadtxt(fname=fnametimes)

#gps=0

def main():
    #combined = 1j*imaginary; combined += combined

    #print(combined)

    #reversing fourier series
    #timedomain=np.fft.ifft(combined)

    freq=time

    #freq=freq+gps
    
    plt.rcParams["figure.figsize"] = (16,11)

    figure, axis = plt.subplots(2,1)
    
    axis[0].plot(freq, combined)
    axis[0].set_title("TimeSeriesDomain: with Gaps Filled")
    
    #scale/unit of signal of time is currently unknown 
    plt.setp(axis[0], xlabel="time(gps)")
    plt.setp(axis[0], ylabel="signal")
    ################33 LEGENDS NOT WORKING
    axis[0].legend()
    
    axis[1].plot(freq, combined)
    axis[1].set_title("TimeSeriesDomain: with Gaps filled")

    #scale/unit of signal of time is currently unknown 
    plt.setp(axis[1], xlabel="time(gps)")
    plt.setp(axis[1], ylabel="signal")

    #saving plot
    #ftypes=['jpg', 'svg']
    ftypes=['png']
    saveplot('plots/LISA_gaps_filled_timeseries_test_plot', ftypes)
    
    plt.show()


def get_data(fname):
    #load data
    data=np.loadtxt(fname, usecols=range(3))

    #splitting column data into individual arrays
    time=np.array(data[0:, 0])
    combined=np.array(data[0:, 1])
    #imaginary=np.array(data[0:, 2])

    #data parse check
    np.set_printoptions(suppress=True, precision=30)
    #print(time, combined, imaginary)
    return time, combined
    
def get_UTC_datetime(gps):
    utc = datetime(1980, 1, 6) + timedelta(seconds=gps - (37-18))#apparently leap seconds between gps and utc team need to be calculated
    print(utc)
    return utc
    


def saveplot(title, filetypes):
    for ftype in filetypes:
        filename=f'{title}.{ftype}'
        print(f'saving file {filename}')
        plt.savefig(filename)
        
def saving_original_data_to_dat_file(time, combined):
    #creating 3 column data
    newdata=np.column_stack((time, combined))

    #making data printable
    originaldata=np.array2string(newdata, precision=30,suppress_small=True)
    #checking data
    print(newdata)

    #data file and appending data in a way so that its human-readable, not binary and its in 3 column format
    file = open('gaps_plot.txt',"a")
    for i in range(combined.size):
        file.write(float(time[i]))
        file.write("\t")
        file.write(str(combined[i]))
       # file.write("\t")
        #file.write(str(combined.imag[i]))
        file.write("\n")
    file.close()

def plot_original(times, sig, subp, ylab):
    plt.subplot(subp)
    plt.ylabel(ylab)
    #not the best way to make title and labels, will improve later
    #plt.title(ylab+"                           ", fontsize=13, ha="right")
    #plt.ylabel("signal")
    #plt.xlabel("time")
    plt.plot(times, sig, label=ylab)

def plot_fft(freqs, sigfft, subp, ylab):
    plt.subplot(subp)
    plt.ylabel(ylab)
    #not the best way to make the title and labels, will improve later
    #plt.title(ylab+"                           ", fontsize=13, ha="right")
    #plt.ylabel("signal strength")
    #plt.xlabel("time")
    markerline, stemlines, baseline = plt.stem(freqs, np.abs(sigfft), '-.')
    plt.setp(stemlines, 'linewidth', 0.2)
    # plt.stem(freqs, np.abs(sigfft))    
    
if __name__ == '__main__':
    main()
