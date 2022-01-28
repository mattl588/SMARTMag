# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 12:17:28 2021

@author: Matt Lacaire

Noise Spectral Density grapher using UCLA GMAG data. Takes in any given magnetometer axis array
(here, scaled_diff_data[n]) and generates a numerical noise spectral density graph. 

"""

import matplotlib.pyplot as plt 
import numpy as np
from scipy import signal

freq = 2 #2Hz data collection 


#for i in range(len(scaled_diff_data)):
def noise_spectral_density(data):
    
    plt.subplot(3, 1, 1)
    
    f_x, Pxx_den_x = signal.welch(data[0], fs = freq, window = 'hann')
    Pxx_den_x_corrected = np.sqrt(Pxx_den_x) #in nT/sqrt(Hz)
    plt.semilogx(f_x, Pxx_den_x_corrected)
    plt.yscale("log")
    plt.xlim([10**-3,1])
    plt.title("Noise Spectrum in X")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("nT/sqrt(Hz)")
    
    plt.subplot(3, 1, 2)
    f_y, Pxx_den_y = signal.welch(data[1], fs = freq, window = 'hann')
    Pxx_den_y_corrected = np.sqrt(Pxx_den_y)
    plt.semilogx(f_y, Pxx_den_y_corrected)
    plt.yscale("log")
    plt.xlim([10**-3,1])
    plt.title("Noise Spectrum in Y")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("nT/sqrt(Hz)")
    
    
    plt.subplot(3, 1, 3)
    f_z, Pxx_den_z = signal.welch(data[2], fs = freq, window = 'hann')
    Pxx_den_z_corrected = np.sqrt(Pxx_den_z)
    plt.semilogx(f_z, Pxx_den_z_corrected)
    plt.yscale("log")
    plt.xlim([10**-3,1])
    plt.title("Noise Spectrum in Z")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("nT/sqrt(Hz)")
    
    
    plt.subplots_adjust(hspace = 1.2)
