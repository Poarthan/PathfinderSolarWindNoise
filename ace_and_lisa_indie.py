import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy import fftpack

def main():
    global aces, big, at, lt, l, lisas, a, freqa, freql, freql2, lisas2
    filea='datafiles/ACE_data_concise_Filtered_Data_calculated_data.txt'
    fileb='datafiles/g2_alldat_neg1001_Filtered_Data.txt'
    filec='datafiles/ACE_time_seconds.txt'
    filed='datafiles/LISA_full_25_gf.txt'
    colsa= 3
    colsb=1
    colsc=1
    colsd=2
    dataa=np.loadtxt(fname=filea, usecols=range(colsa))
    datab=np.loadtxt(fname=fileb, usecols=range(colsb))
    datac=np.loadtxt(fname=filec, usecols=range(colsc))
    datad=np.loadtxt(fname=filed, usecols=range(colsd))
    a=np.array(dataa[0:, 1])
    l=np.array(datab)
    at=np.array(datac)
    lt=np.array(datad[0:, 0])
    for i in range(at.size):
        if at[i]>lt[0]-1:
            at=at[i-1:]
            a=a[i-1:]
            break
    for i in range(at.size):    
        if at[i] > lt[-1] + 1:
            at=at[:i]
            a=a[:i]
            break
    ace=np.fft.fft(a)
    aces=ace
    lisa=np.fft.fft(l)
    lisas= lisa
    siga = at
    sigb = lt
    time_stepa = (16384/3276)/2
    time_stepb = 64
    freqc = fftpack.fftfreq(len(siga), d=time_stepb)
    freqb = fftpack.fftfreq(len(sigb), d=time_stepa)
    freql= (freqb)*2
    freqa = (freqc)*2
    for i in range(freql.size):    
        if abs(freql[i]) > abs(freqa[freqa.size//2]) + 0.0001:
            freql2=freql[:i]
            lisas2=lisas[:i]
            break
    big= lisas2 *10**-20 
    plt.rcParams["figure.figsize"] = (16,11)
    plot_(aces, big, at, lt, l, lisas, a, freqa, freql, freql2, lisas2)
    #saving plot
    #ftypes=['jpg']
    ftypes=['png']
    saveplot(f'plots/ACE_and_LISA_frequency_together', ftypes)
    
    plt.show()
    
def plot_(aces, big, at, lt, l, lisas, a, freqa, freql, freql2, lisas2):
    figure, axis = plt.subplots(3,1)
    #axis[0].plot(array)
    axis[0].set_title(f"ACE & LISA Data")
    axis[1].set_title(f"LISA Data")
    axis[2].set_title(f"ACE Data")
    
    #scale/unit of signal of frequency is currently unknown 
    plt.setp(axis[0], xlabel="frequency (Hz)")
    plt.setp(axis[0], ylabel=f"signal")
    plt.setp(axis[1], xlabel="frequency (Hz)")
    plt.setp(axis[1], ylabel=f"signal(m/s)")
    plt.setp(axis[2], xlabel="frequency (Hz)")
    plt.setp(axis[2], ylabel=f"signal(N)")
    
    print(freql2)
    print(lisas)
    axis[0].semilogy(abs(freqa), abs(aces), abs(freql2), abs(big), alpha=0.5)
    axis[1].semilogy(abs(freql), abs(lisas))
    axis[2].semilogy(abs(freqa), abs(aces))


def saveplot(title, filetypes):
    for ftype in filetypes:
        filename=f'{title}.{ftype}'
        print(f'saving file {filename}')
        plt.savefig(filename)
        
main()
