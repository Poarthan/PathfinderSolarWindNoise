#!/usr/bin/env python3

import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy import fftpack
from datetime import datetime, timedelta
import time 
import random
import math
from tqdm import tqdm

#load data
fnamedat='datafiles/g2_alldat_neg1001.txt'
cols=1
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
    file = open(f'datafiles/{fnamedat[10:-4]}_Filtered_Data.txt',"a")
    file.truncate(0)
    file.close()

data=np.loadtxt(fname=fnamedat, usecols=range(int(cols)))

#splitting data into individual colums
proton_density=np.array(data)


def main():
    plt.rcParams["figure.figsize"] = (16,11)
   
    global LISA_Data
    prde_original=np.array(proton_density)
    prde=filter_data(proton_density, 1)
    plot_check_filtered_data(prde, prde_original, "LISA Data")

    write_file(prde)

'''
def filter3(the_array):
    bad_dataL=[]
    for i in tqdm(range(the_array.size)):
        if the_array[i] < 0:
            bad_dataL.append(i)
    return bad_dataL
'''
def filter1(the_array):
    bad_dataL=[]
    for i in tqdm(range(the_array.size)):
        if the_array[i] < -1000:
            bad_dataL.append(i)
    return bad_dataL

def filter2(the_array):
    bad_dataL=[]
    for i in tqdm(range(the_array.size-2)):
        valdiff=((the_array[i]+the_array[i+2])/2-the_array[i+1])
        if valdiff<-1000 or valdiff > 1000:
            bad_dataL.append(i)
    return bad_dataL

def cValid(test_array, bstart, bcl2, filterval):
    if filterval ==1:
        for i in range(25):
            what=25-i
            if test_array[1+i+bstart+bcl2] < -1000:
                return False
            if test_array[bstart-what] < -1000:
                return False
    elif filterval ==2:
        return True
    return True

def bValid(test_array, bstart, bcl2, filterval):
    if filterval ==1:
        for i in range(bcl2):
            what=bcl2-i
            if test_array[1+i+bstart+bcl2] < -1000:
                return False
            if test_array[bstart-what] < -1000:
                return False
    elif filterval ==2:
        return True
    return True

def pop_bad(bd, bcl):
    for i in range(bcl):
        bd.pop(0)
    return bd


def gap_fill(array, bad_data, done, filterv):
    extra_bad=False
    while len(bad_data)>0:
        n=1
        bad_chunk_length=1
        while len(bad_data)>n:
            if bad_data[n-1]+1==bad_data[n]:
                bad_chunk_length+=1
                n+=1
            else:
                break
#        if bad_data[0]>52000 and bad_data[0]<52500:
#            if bad_chunk_length>1:
#                print(bad_chunk_length, bad_data[0])
#        if bad_data[0]>63000 and bad_data[0]<66000:
           # print[]
            #print(bad_chunk_length, bad_data[0])
#            if bad_chunk_length>1:
#                print(bad_chunk_length, bad_data[0])
        if array.size > bad_data[0]+bad_chunk_length:
            if bad_chunk_length == 1:
                array=TypeA_gap(bad_data[0], array, bad_chunk_length)
                bad_data=pop_bad(bad_data, bad_chunk_length)
            elif bad_chunk_length<25 and bad_chunk_length>1:
                bCheck=bValid(array, bad_data[0], bad_chunk_length, filterv)
                if bCheck:
                    array=TypeB_gap(bad_data[0], array, bad_chunk_length)
                    bad_data=pop_bad(bad_data, bad_chunk_length)
                else:
                    #print("YEAH")
                    if done:
                        array=TypeA_gap(bad_data[0], array, bad_chunk_length)
                        bad_data=pop_bad(bad_data, bad_chunk_length)
                    else:
                        extra_bad=True
                        bad_data=pop_bad(bad_data, bad_chunk_length)
            elif bad_chunk_length>25 and array.size > bad_data[0]+bad_chunk_length+25 and bad_data[0]-25>0:
                cCheck=cValid(array, bad_data[0], bad_chunk_length, filterv)
                if cCheck:
                    array=TypeC_gap(bad_data[0], array, bad_chunk_length)
                    bad_data=pop_bad(bad_data, bad_chunk_length)
                else:
                    if done:
                        bCheck=bValid(array, bad_data[0], bad_chunk_length, filterv)
                        if bCheck:
                            array=TypeB_gap(bad_data[0], array, bad_chunk_length)
                            bad_data=pop_bad(bad_data, bad_chunk_length)
                        else:
                            TypeA_gap(bad_data[0], array, bad_chunk_length)
                            bad_data=pop_bad(bad_data, bad_chunk_length)
                    else:
                        extra_bad=True
                        bad_data=pop_bad(bad_data, bad_chunk_length)
            else:
                bCheck=bValid(array, bad_data[0], bad_chunk_length, filterv)
                if bCheck:
                    array=TypeB_gap(bad_data[0], array, bad_chunk_length)
                    bad_data=pop_bad(bad_data, bad_chunk_length)
                else:
                    #print("YEAH")
                    if done:
                        array=TypeA_gap(bad_data[0], array, bad_chunk_length)
                        bad_data=pop_bad(bad_data, bad_chunk_length)
                    else:
                        extra_bad=True
                        bad_data=pop_bad(bad_data, bad_chunk_length)
        else:
            x1=array[bad_data[0]-1]
            for i in range(bad_chunk_length):
                array[bad_data[0]]=x1
                bad_data.pop(0)
    return array, extra_bad
    
def filter_data(original_array, num):
    bd=[]
    bad=0
    n=1
    #print(original_array)
    if num == 1:
        bd=filter1(original_array)
    elif num == 2:
        bd=filter2(original_array)
    even_worse=False
    terrible=False

    #for i in range(3000):
        #print(original_array[63000+i])
#    for i in range(25):
#        asdf=25-i
#        print(original_array[63148-asdf])
#    for i in range(25):
#        print(original_array[65683+i])

    new_array, terrible=gap_fill(original_array, bd, False, num)
#    print("TEST___________________------____")
    if terrible==True:
        if num == 1:
            bd=filter1(new_array)
        elif num == 2:
            bd=filter2(new_array)
        
        newer_array, even_worse=gap_fill(new_array, bd, False, num)
    else:
        newer_array=new_array

    if even_worse==True:
        if num == 1:
            bd=filter1(newer_array)
        elif num == 2:
            bd=filter2(newer_array)        
        final, dc=gap_fill(newer_array, bd, True, num)
    else:
        final=newer_array
    #print(array)
    #numpy.interp


    return final

def TypeA_gap(badstart, gap_array, bad_cl):
    x1=gap_array[badstart-1]
    x2=gap_array[badstart+bad_cl]
    z=(x2-x1)/bad_cl
    for i in range(bad_cl):
        gap_array[badstart+i]=x1+z*(1+i)
    return gap_array
        
def TypeB_gap(badstart, gap_array, bad_cl):
    x1=gap_array[badstart-1]
    x2=gap_array[badstart+bad_cl]
    z=(x2-x1)/bad_cl
    sd1=np.array([])
    sd2=np.array([])
    popsize=bad_cl
    for i in range(bad_cl):
        hwat=bad_cl-i
        sd1=np.append(sd1, float(gap_array[badstart-hwat]))
        sd2=np.append(sd2, float(gap_array[badstart+bad_cl+i]))
    sd1=np.std(sd1)
    sd2=np.std(sd2)
    for i in range(bad_cl):    
        filler=sd1*(bad_cl-i)/(bad_cl+1)+sd2*(i+1)/(bad_cl+1)
        gap_array[badstart+i]=x1+z*(1+i)+filler
    return gap_array

def TypeC_gap(badstart, gap_array, bad_cl):
    x1=gap_array[badstart-1]
    x2=gap_array[badstart+bad_cl]
    z=(x2-x1)/bad_cl
    gap_filler=np.array([])
    hanningWin=np.hanning(50)
    nnj=1
    if bad_cl>50:
        nnj=bad_cl//50
        if nnj < 1:
            nnj=1
        if nnj > 30:
            nnj=30
    hanningWin=np.hanning(nnj*50+1)
    hanningWin=hanningWin[1:]
    #print(hanningWin.size)
    #if badstart>63000 and badstart<66000:
    #    print("\n\n\n\n\n_______________________")
    #    for i in range(50):
    #        print(hanningWin[i], end = " ")
    #    print("__________________________\n\n\n\n\n")
    for extra in range(nnj):
        add=extra*50
        for i in range(25):
            tmpval=25-i
            filler=0.5*gap_array[badstart-tmpval]*float(hanningWin[i+add])
            gap_filler=np.append(gap_filler, filler)
        for i in range(25):
            j=25+i
            filler=0.5*gap_array[badstart+bad_cl+1+i]*float(hanningWin[j+add])
            gap_filler=np.append(gap_filler, filler)
    for i in range(bad_cl):
        gap_array[badstart+i]=gap_filler[i%len(gap_filler)]##+x1+z*(1+i) #AAAAAAAAAAAAAAAAAAAAAAAAH
    return gap_array
'''
    if badstart>63000 and badstart<66000:
        # print[]
        #print(bad_chunk_length, bad_data[0])
        
        if bad_cl>1:
            for i in range(25):
                tmpval=25-i
                filler=0.5*gap_array[badstart-tmpval]*float(hanningWin[i+add])
                print(filler, end=" ")
            print("\n")
            for i in range(25):
                j=25+i
                filler=0.5*gap_array[badstart+bad_cl+1+i]*float(hanningWin[j+add])
                print(filler, end=' ')
'''            
            #print(bad_cl, badstart) 

    
def saveplot(title, filetypes):
    for ftype in filetypes:
        filename=f'{title}.{ftype}'
        print(f'saving file {filename}')
        plt.savefig(filename)

def plot_check_filtered_data(array, original, name):    
    figure, axis = plt.subplots(2,1)
    axis[0].plot(array)
    axis[0].set_title(f"ACE Filtered {name} Data")
    
    #scale/unit of signal of time is currently unknown 
    plt.setp(axis[0], xlabel="Just Indecies(about 64 second sampling freq)")
    plt.setp(axis[0], ylabel=f"{name}")
    
    axis[1].plot(original)
    axis[1].set_title(f"ACE UnFiltered {name} Data")

    #scale/unit of signal of time is currently unknown 
    plt.setp(axis[1], xlabel="Just Indecies(about 64 second sampling freq)")
    plt.setp(axis[1], ylabel=f"{name}")

    #saving plot
    ftypes=['jpg']
    #ftypes=['png']
    name=name.replace(" ", "_")

    saveplot(f'plots/filtertest/{fnamedat[10:-4]}_filtered_{name}', ftypes)
    
    plt.show()

def write_file(pd):
    print("writing to", f'datafiles/{fnamedat[10:-4]}_Filtered_Data.txt')
    file = open(f'datafiles/{fnamedat[10:-4]}_Filtered_Data.txt',"a")
    #file.write("pd, apr, ps, xdGSE, ydGSE, zdGSE, xpGSE, ypGSE, zpGSE")
    #file.write("\n")
    for i in tqdm(range(pd.size)):
        file.write(str(pd[i]))
        file.write("\n")
    file.close()
    
if __name__ == '__main__':
    main()
