import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy import fftpack
from tqdm import tqdm


truncate=True
if truncate==True:
    file = open(f'datafiles/g2_huge_file_ifft.dat',"a")
    file.truncate(0)
    file.close()
'''

def main():
    #x = np.loadtxt(f'catalog/{j}')
    x = np.loadtxt('catalog/g2_z_1150680613_16384.txt')
    # rebuild the full real component of the spectrum: 0, positive frequencies, negative/flipped frequencies
    long_x1 = np.concatenate(([0.], x[:,1], np.flip(x[:,1]), [0.]))
    # rebuild the full imaginary component: 0, positive frequencies, complex conjugate of the negative/flipped freqs
    long_x2 = np.concatenate(([0.], x[:,2], -np.flip(x[:,2]), [0.]))
    # do the iFFT
    final=np.fft.ifft(long_x1 + long_x2*1j)

    #saving_original_data_to_dat_file(final)
    #x = np.loadtxt(f'catalog/{j}')
    x = np.loadtxt('catalog/g2_z_1150680613_16384.txt')
    # rebuild the full real component of the spectrum: 0, positive frequencies, negative/flipped frequencies
    long_x1 = np.concatenate(([0.], x[:,1], np.flip(x[:,1])))
    # rebuild the full imaginary component: 0, positive frequencies, complex conjugate of the negative/flipped freqs
    long_x2 = np.concatenate(([0.], x[:,2], -np.flip(x[:,2])))
    # do the iFFT
    final2=np.fft.ifft(long_x1 + long_x2*1j)

    #saving_original_data_to_dat_file(final)
    asdf=np.arange(final.size)
    asdf2=np.arange(final2.size)

    plt.plot(asdf, final.real, asdf2, final2.real, alpha=0.6)
    plt.legend()
    #lasdf.legend([final, final2], ['label1', 'label2'])

    plt.show()
'''

def main():
    global long_x1, long_x2
    with open('datafiles/catalog/filenames_g2_z.txt') as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]
        for j in lines:
            x = np.loadtxt(f'datafiles/catalog/{j}')
            #x = np.loadtxt('catalog/g2_z_1150680613_16384.txt')
            # rebuild the full real component of the spectrum: 0, positive frequencies, negative/flipped frequencies
            if x.size == 3276*3:
                long_x1 = np.concatenate(([0.], x[:,1], np.flip(x[:,1])))
                # rebuild the full imaginary component: 0, positive frequencies, complex conjugate of the negative/flipped freqs
                long_x2 = np.concatenate(([0.], x[:,2], -np.flip(x[:,2])))
                # do the iFFT
            elif x.size == 3275*3:
                #print("-------------------ANAMOLY------------------------------")
                long_x1 = np.concatenate(([0.], x[:,1], np.flip(x[:,1]) ))# , [0.]))
                # rebuild the full imaginary component: 0, positive frequencies, complex conjugate of the negative/flipped freqs
                long_x2 = np.concatenate(([0.], x[:,2], -np.flip(x[:,2]) ))# , [0.]))
                # do the iFFT
            else:
                #print(x.size, "??????????????????????????")
                long_x1 = np.concatenate(([0.], x[:,1], np.flip(x[:,1])))
                # rebuild the full imaginary component: 0, positive frequencies, complex conjugate of the negative/flipped freqs
                long_x2 = np.concatenate(([0.], x[:,2], -np.flip(x[:,2])))
                # do the iFFT

            final=np.fft.ifft(long_x1 + long_x2*1j)
            print(f'{j}', final)
            #for i in tqdm(range(final.size)):
            for i in range(final.size):
                if final.imag[i] > 1*10**-13:
                    #print(final.imag[i], i)
                    #print("________BAD IMAGINARY DETECTED_____\n\n\n\n", x.size, j)
                    input()
            saving_original_data_to_dat_file(final)


def saving_original_data_to_dat_file(co):
    #data file and appending data in a way so that its human-readable, not binary and its in 3 column format
    #truncate=False

    file = open('datafiles/g2_huge_file_ifft.dat',"a")
    for i in range(co.size):
        file.write(str(co.real[i]))
        #file.write(str("\t"))
        #file.write(str(co.imag[i]))
        file.write("\n")
    file.close()
main()
