#!/usr/bin/env python3

import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy import fftpack
from datetime import datetime, timedelta
import time 

#load data
fnamedat='datafiles/g1_huge_file.dat'
cols=3
fnametimes='datafiles/g1_huge_file_times.dat'

if len(sys.argv) == 3:
    fnamedat = sys.argv[1]# they can override the file name
    fnametimes = sys.argv[2]
elif len(sys.argv) == 4:
    fnamedat = sys.argv[1]
    fnametimes = sys.argv[2]
    cols = sys.argv[3]
else:
    sys.stderr.write(f'usage: {sys.argv[0]} [--gps] file.dat\n')
        
data=np.loadtxt(fname=fnamedat, usecols=range(cols))

#splitting data into individual colums
frequency=np.array(data[0:, 0])
real=np.array(data[0:, 1])
imaginary=np.array(data[0:, 2])

#data parse check
np.set_printoptions(suppress=True, precision=30)
#print(frequency, real, imaginary)

time_stuff=np.loadtxt(fname=fnametimes)

gps=0

def main():
    combined = 1j*imaginary; combined += real

    print(combined)

    #reversing fourier series
    timedomain=np.fft.ifft(combined)

    freq=time_stuff

    freq=freq+gps
    
    plt.rcParams["figure.figsize"] = (16,11)

    figure, axis = plt.subplots(2,1)
    
    axis[0].plot(freq, timedomain.real, freq, timedomain.imag)
    axis[0].set_title("TimeSeriesDomain: with Imaginary Data")
    
    #scale/unit of signal of time is currently unknown 
    plt.setp(axis[0], xlabel="time(gps)")
    plt.setp(axis[0], ylabel="signal")
    ################33 LEGENDS NOT WORKING
    axis[0].legend()
    
    axis[1].plot(freq, timedomain)
    axis[1].set_title("TimeSeriesDomain: with Real Data ONLY")

    #scale/unit of signal of time is currently unknown 
    plt.setp(axis[1], xlabel="time(gps)")
    plt.setp(axis[1], ylabel="signal")

    #saving plot
    ftypes=['jpg']
    #ftypes=['png', 'svg']
    saveplot('plots/Sensor1_Mar01Jun23_TimeSeriesDomain_of_Satellite_Data', ftypes)
    
    plt.show()

    time_vec, sig = frequency, timedomain
    assert(len(time_vec) == len(sig))
    N = len(time_vec)
    time_step = time_vec[1] - time_vec[0]
    #print(time_step)
    
    # plot the fft signal
    plot_original(freq, sig, 311, 'TimeSeriesDomain of Satellite Data')

    # better frequency format
    sig_fft = fftpack.fft(sig)
    # The corresponding frequencies
    freqs = fftpack.fftfreq(len(sig), d=time_step)
    plot_fft(freqs[:N//2], np.abs(sig_fft[:N//2]), 312, 'FFT-Amplitude Spectrum of Data')
    
    # And the power (sig_fft is of complex dtype)
    power = np.abs(sig_fft)**2

    amplitude = np.sqrt(power)
    
    # plot the fft, zoomed in
    plot_fft(freqs[:N//8], np.abs(sig_fft[:N//8]), 313, 'xzoom')

    ###labels code is made, but kind of ugly, so just title for now
    ftypes=['jpg']
    #ftypes=['png', 'svg']
    saveplot('plots/Sensor1_Mar01Jun23_TimeSeriesDomain_and_FFT_of_data', ftypes)
    plt.show()


def get_data(fname):
    #load data
    data=np.loadtxt(fname, usecols=range(3))

    #splitting column data into individual arrays
    frequency=np.array(data[0:, 0])
    real=np.array(data[0:, 1])
    imaginary=np.array(data[0:, 2])

    #data parse check
    np.set_printoptions(suppress=True, precision=30)
    #print(frequency, real, imaginary)
    return frequency, real, imaginary
    
def get_UTC_datetime(gps):
    utc = datetime(1980, 1, 6) + timedelta(seconds=gps - (37-18))#apparently leap seconds between gps and utc team need to be calculated
    print(utc)
    return utc
    
def saveplot(title, filetypes):
    for ftype in filetypes:
        filename=f'{title}.{ftype}'
        print(f'saving file {filename}')
        plt.savefig(filename)
        
def saving_original_data_to_dat_file(frequency, timedomain):
    #creating 3 column data
    newdata=np.column_stack((frequency, timedomain.real, timedomain.imag))

    #making data printable
    originaldata=np.array2string(newdata, precision=30,suppress_small=True)
    #checking data
    print(newdata)

    #data file and appending data in a way so that its human-readable, not binary and its in 3 column format
    file = open('datafiles/original_spacecraft_data.dat',"a")
    for i in range(timedomain.size):
        file.write(str(frequency[i]))
        file.write("\t")
        file.write(str(timedomain.real[i]))
        file.write("\t")
        file.write(str(timedomain.imag[i]))
        file.write("\n")
    file.close()

def plot_original(times, sig, subp, ylab):
    plt.subplot(subp)
    plt.ylabel(ylab)
    #not the best way to make title and labels, will improve later
    #plt.title(ylab+"                           ", fontsize=13, ha="right")
    #plt.ylabel("signal")
    #plt.xlabel("frequency")
    plt.plot(times, sig, label=ylab)

def plot_fft(freqs, sigfft, subp, ylab):
    plt.subplot(subp)
    plt.ylabel(ylab)
    #not the best way to make the title and labels, will improve later
    #plt.title(ylab+"                           ", fontsize=13, ha="right")
    #plt.ylabel("signal strength")
    #plt.xlabel("frequency")
    markerline, stemlines, baseline = plt.stem(freqs, np.abs(sigfft), '-.')
    plt.setp(stemlines, 'linewidth', 0.2)
    # plt.stem(freqs, np.abs(sigfft))    
    
if __name__ == '__main__':
    main()
