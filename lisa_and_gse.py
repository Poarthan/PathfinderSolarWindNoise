import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy import fftpack

def main():
    fileb='datafiles/lisa_data.txt'
    filed='datafiles/lisa_time.txt'
    colsb=1
    colsd=2
    datab=np.loadtxt(fname=fileb, usecols=range(colsb))
    datad=np.loadtxt(fname=filed, usecols=range(colsd))
    l=np.array(datab)
    lt=np.array(datad[0:, 0])
    lisa=np.fft.fft(l)
    lisas= lisa
    sigb = lt
    time_stepa = 16384/3276
    freqb = fftpack.fftfreq(len(sigb), d=time_stepa)
    freql= (freqb)*2
    big= lisas  

    filea='datafiles/ACE_data_concise_Filtered_Data.txt'
    filec='datafiles/ACE_time_seconds.txt'
    colsa= 9
    colsc=1
    dataa=np.loadtxt(fname=filea, usecols=range(colsa))
    datac=np.loadtxt(fname=filec, usecols=range(colsc))
    a=np.array(dataa[0:, 3])
    at=np.array(datac)
    ace=np.fft.fft(a)
    siga = at
    time_stepa = 64
    freqa = fftpack.fftfreq(len(siga), d=time_stepa)
    freqx = freqa
    print(a)
    plt.rcParams["figure.figsize"] = (16,11)

    plot_(ace, big, at, lt, l, lisas, a, freqx, freql)
    saveplot(title, filetypes)
    
def plot_(ace, big, at, lt, l, lisas, a, freqx, freql): 
    figure, axis = plt.subplots(3,1)
    #axis[0].plot(array)
    axis[0].set_title(f"ACE & LISA Data")
    axis[1].set_title(f"LISA Data")
    axis[2].set_title(f"ACE Data")
    
    #scale/unit of signal of frequency is currently unknown 
    plt.setp(axis[0], xlabel="frequency")
    plt.setp(axis[0], ylabel=f"signal")
    plt.setp(axis[1], xlabel="frequency")
    plt.setp(axis[1], ylabel=f"signal")
    plt.setp(axis[2], xlabel="frequency")
    plt.setp(axis[2], ylabel=f"signal")

    axis[0].semilogy(abs(freqx[:freqx.size]), abs(ace[:ace.size]), abs(freql[:freql.size]), abs(big[:big.size]), alpha=0.5)
    axis[1].semilogy(abs(freql[:freql.size]), abs(big[:big.size]))
    axis[2].semilogy(abs(freqx[:freqx.size]), abs(ace[:ace.size]))
    #saving plot
    #ftypes=['jpg']
    ftypes=['png']
    saveplot(f'plots/lisa_and_gse', ftypes)
    
    plt.show()

def saveplot(title, filetypes):
    for ftype in filetypes:
        filename=f'{title}.{ftype}'
        print(f'saving file {filename}')
        plt.savefig(filename)
        
main()
