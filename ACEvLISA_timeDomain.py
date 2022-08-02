import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy import fftpack
from tqdm import tqdm

def main():
    ACE='datafiles/ACE_data_Filtered_Data_calculated_data.txt'
    lisa='datafiles/g2_alldat_neg1001_Filtered_Data.txt'
    lisa2='datafiles/LISA_full_25_gf.txt'
    acetimes='datafiles/ACE_time_seconds.txt'
    aced=np.loadtxt(fname=ACE, usecols=range(3))
    lisad=np.loadtxt(fname=lisa)
    lisat=np.loadtxt(fname=lisa2, usecols=range(2))
    acetimesd=np.loadtxt(fname=acetimes)
    a=np.array(aced[0:, 1])##*2*10**12
    l=np.array(lisad)
    lt=np.array(lisat[0:, 0])
    at=np.array(acetimesd)

    plt.rcParams["figure.figsize"] = (16,11)
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

    #l= l * (5*10**9)
    plot_(a, l, at, lt)
    #saving plot
    #ftypes=['jpg']
    ftypes=['png']
    saveplot(f'plots/TimeDomain_Comparison_ACEvLPF', ftypes)
    #plt.plot( alpha=0.5)
    plt.show()


def plot_(aa, ll, ati, lti):
    figure, axis = plt.subplots(3,1)
    #axis[0].plot(array)
    axis[0].set_title(f"ACE & LPF Data")
    axis[1].set_title(f"LPF Data")
    axis[2].set_title(f"ACE Data")

    #scale/unit of signal of time is currently unknown

    plt.setp(axis[0], xlabel="  ")
    plt.setp(axis[0], ylabel=f"Force(N)")
    axis[0].grid()
    plt.setp(axis[1], xlabel=" ")
    plt.setp(axis[1], ylabel=f"Force(N)")
    axis[1].grid()
    plt.setp(axis[2], xlabel="time(gps seconds)")
    plt.setp(axis[2], ylabel=f"Force(N)")
    plt.grid()

    axis[0].plot(ati, aa, lti, ll, alpha=0.5)
    blue_patch = mpatches.Patch(color='blue', label='ACE')
    orange_patch = mpatches.Patch(color='orange', label='LPF')
    axis[0].legend(handles=[blue_patch, orange_patch])
    axis[1].plot(lti, ll)
    axis[2].plot(ati, aa)

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
    plt.setp(stemlines, 'linewidth', 1)
    np.semilogy(np.abs(freqs), np.abs(sigfft))
# plt.stem(freqs, np.abs(sigfft))


main()
