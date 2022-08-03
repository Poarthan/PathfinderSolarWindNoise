import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy import fftpack

def main():
    global aces, big, at, lt, l, lisas, a, freqa, freql, freql2, lisas2
    ACE='datafiles/ACE_data_Filtered_Data_calculated_data.txt'
    lisa='datafiles/g2_alldat_neg1001_Filtered_Data.txt'
    lisa2='datafiles/LISA_full_25_gf.txt'
    acetimes='datafiles/ACE_time_seconds.txt'
    aced=np.loadtxt(fname=ACE, usecols=range(3))
    lisad=np.loadtxt(fname=lisa)
    lisat=np.loadtxt(fname=lisa2, usecols=range(2))
    acetimesd=np.loadtxt(fname=acetimes)
    a=np.array(aced[0:, 1])
    l=np.array(lisad)
    lt=np.array(lisat[0:, 0])
    at=np.array(acetimesd)
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
    big= lisas2
    plt.rcParams["figure.figsize"] = (16,11)
    plot_(aces, big, at, lt, l, lisas, a, freqa, freql, freql2, lisas2)
    #saving plot
    #ftypes=['jpg']
    ftypes=['png']
    saveplot(f'plots/ACE_and_LPF_Loglog', ftypes)

    plt.show()

def plot_(aces, big, at, lt, l, lisas, a, freqa, freql, freql2, lisas2):
    figure, axis = plt.subplots(3,1)
    #axis[0].plot(array)
    axis[0].set_title(f"ACE & LPF Data")
    axis[1].set_title(f"LPF Data")
    axis[2].set_title(f"ACE Data")
    blue_patch = mpatches.Patch(color='blue', label='ACE')
    orange_patch = mpatches.Patch(color='orange', label='LPF')
    axis[0].legend(handles=[blue_patch, orange_patch])
    axis[0].grid()
    axis[1].grid()
    axis[2].grid()
    axis[0].set_ylim(10**-9,10**-2)
    axis[1].set_ylim(10**-9,10**-2)
    axis[2].set_ylim(10**-9,10**-2)
    #scale/unit of signal of frequency is currently unknown
    #plt.setp(axis[0], xlabel="Frequency(Hz)")
    #plt.setp(axis[0], ylabel=f"Signal(N)")
    #plt.setp(axis[1], xlabel="Frequency(Hz)")
    #plt.setp(axis[1], ylabel=f"Signal(N)")
    plt.setp(axis[2], xlabel="Frequency(Hz)")
    plt.setp(axis[2], ylabel=f"Signal(N)")

    print(freql2)
    print(lisas)
    axis[0].loglog(abs(freqa), abs(aces), abs(freql2), abs(big), alpha=0.5)
    axis[1].loglog(abs(freql2), abs(big))
    axis[2].loglog(abs(freqa), abs(aces))


def saveplot(title, filetypes):
    for ftype in filetypes:
        filename=f'{title}.{ftype}'
        print(f'saving file {filename}')
        plt.savefig(filename)

main()
