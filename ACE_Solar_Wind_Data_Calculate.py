#!/usr/bin/env python3

import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy import fftpack
from datetime import datetime, timedelta
import time 
import math
from tqdm import tqdm

#load data
fnamedat='datafiles/ACE_data_concise_Filtered_Data.txt'
cols=9
truncate=True

if len(sys.argv) == 2:
    fnamedat = sys.argv[1]
elif len(sys.argv) == 3:
    fnamedat = sys.argv[1]
    cols = sys.argv[2]
elif len(sys.argv) == 4:
    fnamedat = sys.argv[1]
    cols = sys.argv[2]
    truncate = False
elif len(sys.argv) == 1:
    print("_testing, 2000 data_")
else:
    sys.stderr.write(f'usage: {sys.argv[0]} [--gps] file.dat\n')

#truncate=False
if truncate==True:
    file = open(f'{fnamedat[:-4]}_calculated_data.txt',"a")
    file.truncate(0)
    file.close()

data=np.loadtxt(fname=fnamedat, usecols=range(int(cols)))

#splitting data into individual colums
proton_density=np.array(data[0:, 0])
alpha_particle_ratios=np.array(data[0:, 1])
proton_speed=np.array(data[0:, 2])
x_dot_GSE=np.array(data[0:, 3])
y_dot_GSE=np.array(data[0:, 4])
z_dot_GSE=np.array(data[0:, 5])
pos_gse_x=np.array(data[0:, 6])
pos_gse_y=np.array(data[0:, 7])
pos_gse_z=np.array(data[0:, 8])

##2.9 meters diameter
ar=((2.9)/2)**2
ar=ar*math.pi
print(ar)


def main():    
    #particle_x_force=np.array([])
    #particle_z_force=np.array([])
    f_gen=np.array([])
    start=time.perf_counter()
    for i in tqdm(range(len(proton_speed))):
        fx, fz=calculate_force(proton_speed[i], proton_density[i], ar, math.radians(2), alpha_particle_ratios[i], y_dot_GSE[i], x_dot_GSE[i], z_dot_GSE[i])
        #print(fx, fz)
        write_file(fx, fz, magnitude(fx, fz))
    end=time.perf_counter()
    final=end-start
    print(final)
    
def calculate_force(sp, de, ar, an, he4, vy, vx, vz):
    #converting g/cm^3 to g/km^3
    #de=de*10**15
    #sp=speed
    #de=desnity
    #he4=helliumtoprotonratio
    #ar=area of solar array
    #an=angle between norm of the array and the orbital plane
    #vx is particle velocity in GSE
    #vz is particle velocity in GSE
    sp=float(sp)
    de=float(de)
    ar=float(ar)
    an=float(an)
    he4=float(he4)
    hitsurface=ar*math.cos(an)
    Np=(de*10**6)*(sp*10**3)*hitsurface
    Na=he4*Np
    
    F1=Np*(1.67262192*10**-27)+Na*(6.6446573357 * 10**-27)
    F2=(1+math.cos(2*an))*(vx*10**3)+math.sin(2*an)*(vz*10**3)
    FX=F1*F2

    F2=(1+math.cos(2*an))*(vz*10**3)+math.sin(2*an)*(vx*10**3)
    FZ=F1*F2
    return float(FX), float(FZ)    

def magnitude(f_x, f_z):
    #sqrt(f_x^2+f_y^2+f_z^2) = f_total
    f_total=math.sqrt(f_x**2+f_z**2)
    return f_total

def write_file(pxf, pzf, pgf):
    #print("writing to", f'{fnamedat[:-4]}_calculated_data.txt')
    file = open(f'{fnamedat[:-4]}_calculated_data.txt',"a")
    file.write(str(pxf))
    file.write("\t")
    file.write(str(pzf))
    file.write("\t")
    file.write(str(pgf))
    file.write("\n")
    file.close()


if __name__ == '__main__':
    main()
