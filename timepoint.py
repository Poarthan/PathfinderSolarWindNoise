import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy import fftpack

def main():
    with open('datafiles/g2_z__16384.txt') as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]
        for j in lines:
            time=j.split(" ")
            d=int(time[])

            k=int()
            i= d + (5.00122100122*k)
            
            file = open('datafiles/timepoint_.txt',"a")
            file.write(str(i))
            file.write("\n")
            file.close()

main()

for j in  range(len(lines)):
            dif = float(lines[j+1])-float(lines[j])
            lev = float(dif*0.19995117187)

            if dif > 6:
                file = open('datafiles/g2_gaps_with_lev.txt', "a")
                file.write('start:')
                file.write(lines[j-3275])
                file.write(' end:')
                file.write(lines[j+1])
                file.write(' dif:')
                file.write(str(dif))
                file.write(" lev:")
                file.write(str(lev))
                file.write("\n")
                file.close()              



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
