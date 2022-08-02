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
fnamedat='datafiles/ACE_data_concise_Filtered_Data_calculated_data.txt'
cols=3
fnametimes='datafiles/ACE_time_seconds.txt'

if len(sys.argv) == 3:
    fnamedat = sys.argv[1]# they can override the file name
    fnametimes = sys.argv[2]
elif len(sys.argv) == 4:
    fnamedat = sys.argv[1]
    fnametimes = sys.argv[2]
    cols = sys.argv[3]
elif len(sys.argv) == 1:
    print("_testing, 2000 data_")
else:
    sys.stderr.write(f'usage: {sys.argv[0]} [--gps] file.dat\n')
        
data=np.loadtxt(fname=fnamedat, usecols=range(int(cols)))

#splitting data into individual colums
particle_x_force=np.array(data[0:, 0])
particle_z_force=np.array(data[0:, 1])
f_gen=np.array(data[0:, 2])
time_stuff=np.loadtxt(fname=fnametimes)

freq=time_stuff

def main():
    plt.rcParams["figure.figsize"] = (16,11)

#########################################################################3
###########     Normal Graph

    plot_data(particle_x_force, particle_z_force, "Solar Wind X Force", "Solar Wind X Force")
    plt.show()
    

######################################################################
############## fft of fx Force
    
    time_vec, sig = freq, particle_x_force
    assert(len(time_vec) == len(sig))
    N = len(time_vec)
    time_step = time_vec[1] - time_vec[0]
    #print(time_step)
    
    # plot the fft signal
    plot_original(freq, sig, 311, 'Force X ACE Solar Wind Data')

    # better frequency format
    sig_fft = fftpack.fft(sig)
    # The corresponding frequencies
    freqs = fftpack.fftfreq(len(sig), d=time_step)
    plot_fft(freqs[:N//2], np.abs(sig_fft[:N//2]), 312, 'FFT-Amplitude Spectrum of Data')
    # plot the fft, zoomed in
    plot_fft(freqs[:N//8], np.abs(sig_fft[:N//8]), 313, 'xzoom')

    #ftypes=['jpg']
    ftypes=['png']
    saveplot(f'plots/ACE/Force_X_{fnamedat[10:-4]}_and_FFT', ftypes)
    print("uhhh")
    plt.show()

######################################################################
############## fft of general Force
    time_vec, sig = freq, f_gen
    assert(len(time_vec) == len(sig))
    N = len(time_vec)
    time_step = time_vec[1] - time_vec[0]
    #print(time_step)
    
    # plot the fft signal
    plot_original(freq, sig, 311, 'Force X ACE Solar Wind Data')

    # better frequency format
    sig_fft = fftpack.fft(sig)
    # The corresponding frequencies
    freqs = fftpack.fftfreq(len(sig), d=time_step)
    plot_fft(freqs[:N//2], np.abs(sig_fft[:N//2]), 312, 'FFT-Amplitude Spectrum of Data')
    # plot the fft, zoomed in
    plot_fft(freqs[:N//8], np.abs(sig_fft[:N//8]), 313, 'xzoom')

    ###labels code is made, but kind of ugly, so just title for now
    #ftypes=['jpg']
    ftypes=['png']
    saveplot(f'plots/ACE/Force_general_{fnamedat[10:-4]}_and_FFT', ftypes)
    plt.show()

######################################################################
############## recreating ACE data graph
    time_vec, sig = freq, f_gen
    assert(len(time_vec) == len(sig))
    N = len(time_vec)
    time_step = time_vec[1] - time_vec[0]
    #print(time_step)
    # better frequency format
    sig_fft = fftpack.fft(sig)
    # The corresponding frequencies
    freqs = fftpack.fftfreq(len(sig), d=time_step)    
    # plot the fft signal
    plot_original(np.abs(freqs), np.abs(sig_fft), 111, 'Force General ACE Solar Wind Data')

    ftypes=['jpg']
    #ftypes=['png']
    saveplot(f'plots/ACE/Force_general_{fnamedat[10:-4]}_and_FFT', ftypes)
    plt.show()


def plot_data(array, original, name1, name2):    
    figure, axis = plt.subplots(2,1)
    axis[0].plot(array)
    axis[0].set_title(f"ACE {name1} Data")

    axis[0].semilogy(array)
    
    #scale/unit of signal of time is currently unknown 
    plt.setp(axis[0], xlabel="Just Indecies(about 64 second sampling freq)")
    plt.setp(axis[0], ylabel=f"{name1}")

    
    axis[1].plot(array)
    axis[1].set_title(f"ACE {name2} Data")
    #axis[1].semilogy(freqs, sigfft)
    #scale/unit of signal of time is currently unknown 
    plt.setp(axis[1], xlabel="Just Indecies(about 64 second sampling freq)")
    plt.setp(axis[1], ylabel=f"{name2}")

    #saving plot
    #ftypes=['jpg']
    ftypes=['png']
    name1=name1.replace(" ", "_")
    name2=name2.replace(" ", "_")
    saveplot(f'plots/ACE/{fnamedat[10:-4]}_filtered_{name1}_{name2}', ftypes)
    
    plt.show()
    
    
def get_UTC_datetime(gps):
    utc = datetime(1980, 1, 6) + timedelta(seconds=gps - (37-18))#apparently leap seconds between gps and utc team need to be calculated
    print(utc)
    return utc

def saveplot(title, filetypes):
    for ftype in filetypes:
        filename=f'{title}.{ftype}'
        print(f'saving file {filename}')
        plt.savefig(filename)
        
def plot_original(times, sig, subp, ylab):
    plt.subplot(subp)
    plt.ylabel(ylab)
    #plt.semilogy(times, sig)
    #not the best way to make title and labels, will improve later
    #plt.title(ylab+"                           ", fontsize=13, ha="right")
    #plt.ylabel("signal")
    #plt.xlabel("frequency")
    plt.plot(times, sig, label=ylab)

def plot_fft(freqs, sigfft, subp, ylab):
    plt.subplot(subp)
    plt.ylabel(ylab)
    #plt.semilogy(freqs, sigfft)
    #plt.ylim()
    #plt.xlim()
    #not the best way to make the title and labels, will improve later
    #plt.title(ylab+"                           ", fontsize=13, ha="right")
    #plt.ylabel("signal strength")
    #plt.xlabel("frequency")
    markerline, stemlines, baseline = plt.stem(freqs, np.abs(sigfft), '-.', use_line_collection=True)
    plt.setp(stemlines, 'linewidth', 0.2)
    print("hello")
    plt.semilogy(np.abs(freqs), np.abs(sigfft))
    print("world")
    # plt.stem(freqs, np.abs(sigfft))    
    
if __name__ == '__main__':
    main()
