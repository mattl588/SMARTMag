# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 12:17:28 2021

@author: Matt Lacaire

Noise Spectral Density grapher using UCLA GMAG data. 

"""

import matplotlib as plt 
from scipy import signal


freq = 2 #2Hz data collection 


#for i in range(len(scaled_diff_data)):

    
f, Pxx_den = signal.periodogram(scaled_diff_data[i], freq)
plt.pyplot.semilogx(f, Pxx_den)
plt.pyplot.title("Noise Spectrum for Sensor 07043")
plt.pyplot.xlabel("Frequency (Hz)")
