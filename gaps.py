import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy import fftpack



def main():
 with open('datafiles/g2_huge_file_times.dat') as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]
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
main()
