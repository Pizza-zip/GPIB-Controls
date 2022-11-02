import pyvisa as pv
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import scipy.stats as st
from scipy.optimize import curve_fit
import time 
import os
import pandas as pd


#Global Variables

a=pv.ResourceManager().list_resources()
OSA = pv.ResourceManager().open_resource('GPIB0::6::4::INSTR') #Sets up OSA 

def linConv(x):
    x2 =[]
    for i in x :
        P = 10.0**(i/10.0)
        x2.append(P)
        P = 0
    return np.array(x2)

def Gauss(x, A, B):
    y = A*np.exp(-1*B*x**2)
    return y

def GetData(x):
    
    #Declaring variables needed for later on
    Freq = [] #Final Frequency list
    dBm = [] #Final dBm List
    notFloat = 0 #conditional variable for if loops
    #Sending commands to OSA 
    time.sleep(1)
    A = OSA.query(f'SPDATAF{x}\n') #Send Read&Write for Frequency of selected Trace
    time.sleep(3)
    B = OSA.query(f'SPDATAD{x}\n') #Send Read&Write for dBm of selected Trace
    
    #Complinig data into Readable Array
    Asp = A.split() #Split long string from OSA
    Bsp = B.split()
    
    Aarr = np.array(Asp) #declare them arrays of strings
    Barr = np.array(Bsp)
    
    for i, f in enumerate(Aarr): #OSA sometimes returns Strage non float values (double .)
        for x in f:              # This nested loop checks for any strange strings and removes them
            if (x == '.'):
                notFloat+=1
            if notFloat == 2:
                Aarr[i]=Aarr[i-1]
        notFloat = 0
    
    for i, f in enumerate(Barr): #Similar as above but for dBm (which sometimes have double - or .)
        for x in f:
            if (x == '.'):
                notFloat+=1
            if notFloat == 2:
                Barr[i]=Barr[i-1]
        notFloat = 0
    
    AarrF = Aarr.astype(float) #Converts array of strings to floats
    BarrF = Barr.astype(float)
    
    #Cleaning up the Arrays, removing strange values and first index (which is number of data points)
    Barr3 = np.delete(BarrF,np.argwhere(BarrF >= 0))
    Barr4 = np.delete(Barr3,np.argwhere(Barr3 <= -100.0))
    Aarr1 = np.delete(AarrF,0)
                      
    for x in range(90000): #Creates 2 new lits of same length (sometimes strings are not same length)
        Freq.append(Aarr1[x])
        dBm.append(Barr4[x])
        
    Freq = np.array(Freq) #Casts to Arrays
    dBm = np.array(dBm)

    return Freq , dBm     #Returns our Data


#MAIN CODE

OSA.write('SPSWP1\n') #Take new trace
x1 , y1 = GetData(1)
#x2, y2 = GetData(2)


fig, axs = plt.subplots()#define plot

axs.plot(x1/1e3,y1,',', label ='Data')
#axs.plot(x2/1e3,y2,',',label = 'Yur')
axs.invert_yaxis
plt.xlim([193.310,193.400])
plt.ylim([0,-100])
#plt.axis([193.310,193.800,0,-100])
plt.legend(loc='best')
plt.show()        