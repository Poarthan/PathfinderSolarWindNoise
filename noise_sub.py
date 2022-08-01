import sys
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.mlab import psd, csd
from scipy import fftpack, signal
from tqdm import tqdm
def main():
    ACE='datafiles/ACE_data_concise_Filtered_Data_calculated_data.txt'
    LPF='datafiles/g2_alldat_neg1001_Filtered_Data.txt'
    LPF2='datafiles/LISA_full_25_gf.txt'
    acetimes='datafiles/ACE_time_seconds.txt'
    aced=np.loadtxt(fname=ACE, usecols=range(3))
    LPFd=np.loadtxt(fname=LPF)
    LPFt=np.loadtxt(fname=LPF2, usecols=range(2))
    acetimesd=np.loadtxt(fname=acetimes)
    a=np.array(aced[0:, 1])
    l=np.array(LPFd)
    lt=np.array(LPFt[0:, 0])
    at=np.array(acetimesd)

    plt.rcParams["figure.figsize"] = (16,11)
    ##We cut a little extra time before and after LPF starts and ends in the ACE data and here its cut to as close as possible to the LPF data while still being possibly slight bigger, because we have a longer time period of ACE than LPF data.
    for i in tqdm(range(at.size)):
        if at[i]>lt[0]-1:
            at=at[i-1:]
            a=a[i-1:]
            break
    for i in tqdm(range(at.size)):    
        if at[i] > lt[-1] + 1:
            at=at[:i]
            a=a[:i]
            break
    #print(at[-1], lt[-1], at[-1]-lt[-1])
    a=np.interp(lt, at, a)
    l=l
    ace=np.fft.fft(a) # *10**x
    LPF=np.fft.fft(l)
    time_stepa = 16384/(3276*2)
    time_stepb = 64
   # print(ace.size, LPF.size)
    freqa = fftpack.fftfreq(ace.size, d=time_stepb)*2
    freql = fftpack.fftfreq(LPF.size, d=time_stepa)*2

    #print(ace.size, freqa.size, freql.size, LPF.size)
    
    #print(f.size, Cxy.size)

###############################################################################
    fs=2*1/(16384/3726*2)
    nn=lt.size//2  
    f, Cxy = signal.coherence(a, l, fs, nperseg=nn)
    Cxy=np.interp(lt, f, Cxy)
    ###PSDsub Calculations
    Pxx=np.abs(LPF)**2 #LPF = LPF(f), so LPF = fft(LPF)
    Pyy=np.abs(ace)**2 #ace = ACE(f)
    Pxy=np.sqrt(Cxy*Pxx*Pyy)
    #Pxy=(ace.real-ace.imag)*LPF #CPSD
    Hstf=LPF/ace  #Transfer Function
    Tfest=Hstf
    Tff=np.abs(Tfest)**2
    PSDsub = Pxx+Tff*Pyy-2*(Tff*Pxy).real
    ##final=np.sqrt(PSDsub)
##############################################################################
    plt.rcParams["figure.figsize"] = (16,11)
    #plot_noise_cancellation(PSDsub, LPF, final, freql)
    plot_noise_cancellation(PSDsub, LPF, freql)
    ftypes=['png']
    saveplot(f'plots/LPF_Noise_Cancellation', ftypes)
    
    plt.show() 
    
def plot_noise_cancellation(psub, Ll, freqs): #(psub, Ll, fin, freqs):
    #plt.plot(array)
    plt.title(f"LPF and PSDsub Data")
    blue_patch = mpatches.Patch(color='blue', label='PSDsub')
    orange_patch = mpatches.Patch(color='orange', label='LPF')
    #green_patch = mpatches.Patch(color='green', label='sqrt(PSDsub)')
    plt.legend(handles=[blue_patch, orange_patch])#, green_patch])
    plt.grid()
    plt.xlabel("Frequency(Hz)")
    plt.ylabel("Signal(N)")
    plt.loglog(abs(freqs), abs(psub), abs(freqs), abs(Ll), alpha=0.5)

    #plt.loglog(abs(freqs), abs(psub), abs(freqs), abs(Ll), abs(freqs), abs(fin), alpha=0.5)



def saveplot(title, filetypes):
    for ftype in filetypes:
        filename=f'{title}.{ftype}'
        print(f'saving file {filename}')
        plt.savefig(filename)
        
main()
