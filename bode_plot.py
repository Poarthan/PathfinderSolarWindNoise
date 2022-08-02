import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.mlab import psd, csd
from scipy import fftpack, signal
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
    for i in tqdm(range(at.size)):
        if at[i] > lt[-1] + 1:
            at=at[:i]
            a=a[:i]
            break
    #print(at[-1], lt[-1], at[-1]-lt[-1])
    ace=np.fft.fft(np.interp(lt, at, a)) # *10**x
    lisa=np.fft.fft(l)
    time_stepa = 16384/(3276*2)
    time_stepb = 64
    print(ace.size, lisa.size)
    freqa = fftpack.fftfreq(ace.size, d=time_stepb)*2
    freql = fftpack.fftfreq(lisa.size, d=time_stepa)*2

    print(ace.size, freqa.size, freql.size, lisa.size)

    Hstf=lisa/ace

    print(np.interp(at, lt, l).size, a.size, freqa.size, "adsfasdfasdfasdf")

    magnitude=np.abs(Hstf)
    phase=np.angle(Hstf)
#
#    w, mag, phase = signal.bode(Hstf)
#
#    plt.figure()
#    plt.semilogx(w, mag)    # Bode magnitude plot
#    plt.figure()
#    plt.semilogx(w, phase)  # Bode phase plot
#    plt.show()
#
#
#    plt.figure()
#    plt.loglog(np.abs(freqa), magnitude)
#    #plt.loglog(freqa, magnitude)    # Bode magnitude plot
#    plt.title("Bode Magnitude Plot")
#    plt.xlabel("Frequency (Hz)")
#    plt.ylabel("Magnitude (dB)")
#    plt.grid()
###  #
#    plt.figure()
#    plt.loglog(freqa, phase)
#    plt.title("Bode Phase Plot")
#    plt.xlabel("Frequency (Hz)")
#    plt.ylabel("Phase (Radians)")
#
#    plt.figure()
    plt.semilogx(phase)  # Bode phase plot
    plt.title("Bode Phase Plot")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Phase (Radians)")
    plt.grid()
#    plt.legend()
##    #plt.figure()
    #plt.semilogx(magnitude)    # Bode magnitude plot
    #plt.figure()
    #plt.semilogx(phase)  # Bode phase plot


    ftypes=['jpg']
    #ftypes=['png']yes

    saveplot(f'plots/Bode_Phase_Plot', ftypes)

    plt.show()

#    for i in tqdm(range(freql.size)):
#        if abs(freql[i]) >= abs(freqa[freqa.size//2]):
#            freql2=freql[0:freqa.size//2]
#            lisa2=lisa[0:freqa.size//2]
#            break
#    print(ace.size//2, freqa.size//2, freql2.size, lisa2.size)
#
#

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

if __name__ == "__main__":
    main()
