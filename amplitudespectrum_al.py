import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy import fftpack

def main():
    filea='datafiles/ACE_data_concise_Filtered_Data_calculated_data.txt'
    fileb='datafiles/g2_huge_file_ifft_radians_gap_filled_data_ifft.txt'
    filec='datafiles/ACE_time_seconds.txt'
    colsa= 3
    colsb=2
    colsc=1
    dataa=np.loadtxt(fname=filea, usecols=range(colsa))
    datab=np.loadtxt(fname=fileb, usecols=range(colsb))
    datac=np.loadtxt(fname=filec, usecols=range(colsc))
    a=np.array(dataa[0:, 0])
    l=np.array(datab[0:, 1])
    lt=np.array(datab[0:, 0])
    at=np.array(datac)
    ace=np.fft.fft(a)
    lisa=np.fft.fft(l)
    big= lisa * (10**9)
    l=l*10**7
#    plot_(ace, big, at, lt)

    ############## plot2 comparison of LISA and ACE data
    
    
    sig = a
    time_step = 16384/3276
    N=sig.size
    #print(time_step)
    # just amplitude spectrum
    # better frequency format
    sig_fft = fftpack.fft(sig)
    # The corresponding frequencies
    freqs = fftpack.fftfreq(len(sig), d=time_step)
    plot_fft(freqs[:N//2], np.abs(sig_fft[:N//2]), 311, 'ACE Data')
    # plot the fft, zoomed in
    freq1=freqs
    sig_fft1=sig_fft
    
    sig = big
    N=sig.size
    time_step = 64
    #print(time_step)
    # just amplitude spectrum
    # better frequency format
    sig_fft = fftpack.fft(sig)
    # The corresponding frequencies
    freqs = fftpack.fftfreq(N, d=time_step)
    #print(freqs.size, sig_fft.size)
    plot_fft(freqs[:N//2], np.abs(sig_fft[:N//2]), 312, 'LPF G2 Data')

    
    
    plt.subplot(313)
    plt.ylabel("ACE vs LPF data")
    #not the best way to make the title and labels, will improve later
    #plt.title(ylab+"                           ", fontsize=13, ha="right")
    #plt.ylabel("signal strength")
    #plt.xlabel("frequency")
    #newfreq=freqs[:N//2]+freq1[:N//2]
    #new_sig=sig_fft[:N//2]+sig_fft1[:N//2]
    markerline, stemlines, baseline = plt.stem(freqs[:N//2], np.abs(sig_fft[:N//2]), '-')
    N=sig_fft1.size
    markerline, stemlines, baseline = plt.stem(freq1[:N//2], np.abs(sig_fft1[:N//2]), '-')
    plt.setp(stemlines, 'linewidth', 0.2)
    
    ###labels code is made, but kind of ugly, so just title for now
    ftypes=['jpg']
    #ftypes=['png']
    saveplot(f'plots/Comparison_{filea[10:-4]}_and_{fileb[10:-4]}', ftypes)
    plt.show()



    
def plot_(ace, big, at, lt): 
    figure, axis = plt.subplots(3,1)
    #axis[0].plot(array)
    axis[0].set_title(f"ACE & LISA Data")
    axis[1].set_title(f"LISA Data")
    axis[2].set_title(f"ACE Data")
    
    #scale/unit of signal of time is currently unknown 
    plt.setp(axis[0], xlabel="time")
    plt.setp(axis[0], ylabel=f"signal")
    plt.setp(axis[1], xlabel="time")
    plt.setp(axis[1], ylabel=f"signal")
    plt.setp(axis[2], xlabel="time")
    plt.setp(axis[2], ylabel=f"signal")
    
    axis[0].plot(at, ace, lt, big)
    axis[1].plot(lt, big)
    axis[2].plot(at, ace)
    #saving plot
    #ftypes=['jpg']
    ftypes=['png']
    saveplot(f'plots/ACE_and_LISA', ftypes)
    
    plt.show()

def saveplot(title, filetypes):
    for ftype in filetypes:
        filename=f'{title}.{ftype}'
        print(f'saving file {filename}')
        plt.savefig(filename)
        
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


main()
