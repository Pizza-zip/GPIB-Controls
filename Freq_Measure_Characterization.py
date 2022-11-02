import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import scipy.stats as st
from scipy.optimize import curve_fit, minimize_scalar
import time 
import os
import pandas as pd
import scipy.io

from scipy.optimize import curve_fit
from scipy.interpolate import interp1d
from scipy.signal import find_peaks

NormInt = scipy.io.loadmat('Intensity_normalized_value.mat')
WaveLen = scipy.io.loadmat('wavelength_range.mat')


Intensity = NormInt.get('Normalized_Y_mea')
Wavelength = WaveLen.get('wavelength_values_in_the_window_range')

y = Intensity[0]
x = Wavelength[0]

y1 = y[2480000:2515000]
x1 = x[2480000:2515000]

peak = find_peaks(y1, height = 0.8)

# cen = x[peak]
# amp = y[peak]
# sig = 1



f1 = interp1d(x1, y1, kind='nearest')
f2 = interp1d(x1, y1, kind='linear')
f3 = interp1d(x1, y1, kind='cubic')
xx = np.linspace(min(x1),max(x1))



plt.figure
plt.plot(x1,y1,',r')
# plt.plot(x1, y1, 'r,', xx, f1(xx), '--')
# plt.plot(x1, y1, 'b,', xx, f2(xx), '--')
plt.plot(x1, y1, 'g,', xx, f3(xx), '--')
plt.show()