import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy import fftpack

def main():
    with open('tmpParseFiles/g2_z_data_filenames.txt') as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]
        for j in lines:

            data=np.loadtxt(fname=f"catalog/{j}", usecols=range(3))
            print('yay i work:', {j})
            #load data
            frequency=np.array(data[0:, 0])
            real=np.array(data[0:, 1])
            imaginary=np.array(data[0:, 2])


            #splitting column data into individual arrays
            frequency=np.array(data[0:, 0])
            real=np.array(data[0:, 1])
            imaginary=np.array(data[0:, 2])

            #data parse check
            np.set_printoptions(suppress=True, precision=30)
            #print(frequency, real, imaginary)
            saving_original_data_to_dat_file(frequency, real, imaginary)

def saving_original_data_to_dat_file(frequency, real, imaginary):
    #creating 3 column data
    newdata=np.column_stack((frequency, real, imaginary))

    #making data printable
    originaldata=np.array2string(newdata, precision=30,suppress_small=True)
    #checking data
    #print(newdata)

    #data file and appending data in a way so that its human-readable, not binary and its in 3 column format
    file = open('datafiles/g2_huge_file.dat',"a")
    for i in range(real.size):
        file.write(str(frequency[i]))
        file.write("\t")
        file.write(str(real[i]))
        file.write("\t")
        file.write(str(imaginary[i]))
        file.write("\n")
    file.close()
main()
