import sys
import numpy as np
import matplotlib.pyplot as plt

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
    #ace=np.fft.fft(a)
    a=np.interp(lt, at, a)
    #lisa=np.fft.fft(xxx)
    #print(lisa.size, ace.size)
    plt.rcParams["figure.figsize"] = (16,11)
    #figure, axis = plt.subplots(2,1)
    #axis[0].plot(array)
    fs=2*1/(16384/(3276*2))
    nn=lt.size//2
    print(nn)
    plt.title("Coherence of ACE and LPF")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Coherence")
    plt.grid()
    #
    for i in range(15):
        nn=lt.size//2
        nn=nn//(2**i)
        nn=int(nn)
        print(nn, i, "WHAT IS THE PROBLEM")
        f, Cxy = signal.coherence(a, l, fs, nperseg=int(nn))
        print(f.size, Cxy.size)
        print(Cxy)
        #plt.plot(f, Cxy)
        plt.legend()
        plt.loglog(f, Cxy)

        ftypes=['png']
        saveplot(f'plots/co_tests2/ACE_and_LPF_co_2xx{i+1}', ftypes)
        plt.show()
        
    #plt.xlabel('frequency [Hz]')
    nn=lt.size//32
    f, Cxy = signal.coherence(a, l, fs, nperseg=nn)
    print(f.size, Cxy.size)
    print(Cxy)
    #plt.plot(f, Cxy)
    #plt.show()
    plt.loglog(f, Cxy)
    #plt.ylabel('Coherence')

    #plt.show()
    '''
    Cxy, freqs=plt.cohere(xxx, a)
    plt.show()
    print(Cxy, freqs)
    plt.plot(Cxy, freqs)
    '''
    
    #saving plot
    #ftypes=['jpg']
    ftypes=['png']
    saveplot(f'plots/co_tests2/ACE_and_LPF_co', ftypes)
    
    plt.show()


def saveplot(title, filetypes):
    for ftype in filetypes:
        filename=f'{title}.{ftype}'
        print(f'saving file {filename}')
        plt.savefig(filename)
        
main()





