import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy import fftpack

def main():
    global aces, big, at, lt, l, lisas, a, freqa, freql, freql2, lisas2
    filea='datafiles/force_data.txt'
    fileb='datafiles/lisa_data.txt'
    filec='datafiles/a_time.txt'
    filed='datafiles/lisa_time.txt'
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
=======
from scipy import fftpack, signal
from tqdm import tqdm
def main():
    ACE='datafiles/ACE_data_concise_Filtered_Data_calculated_data.txt'
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

    plt.rcParams["figure.figsize"] = (16,11)

    for i in tqdm(range(at.size)):
        if at[i]>lt[0]-1:
            at=at[i-1:]
            a=a[i-1:]
            break
    for i in range(at.size):    
        if at[i] > lt[-1] + 1:
            at=at[:i]
            a=a[:i]
            break
    #print(at[-1], lt[-1], at[-1]-lt[-1])
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
    plot_()
    #saving plot
    #ftypes=['jpg']
    ftypes=['png']
    saveplot(f'plots/ACE_and_LISA_', ftypes)
    
    plt.show()
    
def plot_():
    global aces, big, at, lt, l, lisas, a, freqa, freql, freql2, lisas2
    print(freqa)
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
    
    print(freql2)
    print(lisas)
    axis[0].loglog(abs(freqa), abs(aces), abs(freql2), abs(lisas2), alpha=0.5)
    axis[1].loglog(abs(freql), abs(big))
    axis[2].loglog(abs(freqa), abs(aces))
    ace=np.fft.fft(a) # *10**x
    lisa=np.fft.fft(l)
    time_stepa = 16384/(3276*2)
    time_stepb = 64
    print(ace.size, lisa.size)
    freqa = fftpack.fftfreq(ace.size, d=time_stepb)*2
    freql = fftpack.fftfreq(lisa.size, d=time_stepa)*2

    print(ace.size, freqa.size, freql.size, lisa.size)

    for i in tqdm(range(freql.size)):    
        if abs(freql[i]) > abs(freqa[freqa.size//2]) + 0.0001:
            freql2=freql[:freqa.size//2]
            lisa2=lisa[:freqa.size//2]
            break
    print(ace.size, freqa.size, freql2.size, lisa2.size)

    f, Cxy = signal.coherence(ace[:freqa.size//2], lisa2)
    plt.semilogy(f, Cxy)
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('coherence')
    plt.show()
    #l= l * (5*10**9)
    #

    #saving plot
    #ftypes=['jpg']
    ftypes=['png']
    #saveplot(f'plots/TimeDomain_Comparison_ACEvLISA', ftypes)
    #plt.plot( alpha=0.5)
    #plt.show()

    
def plot_(): 
    plt.plot()
    plt

    plt.semilogx(w, mag)    # Bode magnitude plot

    plt.figure()

    plt.semilogx(w, phase)  # Bode phase plot

    plt.show()


def saveplot(title, filetypes):
    for ftype in filetypes:
        filename=f'{title}.{ftype}'
        print(f'saving file {filename}')
        plt.savefig(filename)
        
main()
