# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 19:34:33 2021

@author: Matt Lacaire
"""

import numpy as np
import os 
from scipy.signal import lombscargle




def RM3100_Analyzer(path):
    f = None
    try:
        f = open(path,"r")
    except:
        print("RM3100 file opening failure.")

    Content = f.read()
    CoList = Content.split("\n")
    numlines = 0
    for i in CoList:
        if i:
            numlines += 1

    timestamps = np.zeros(numlines)
    values = np.zeros(numlines)
    for x in range(1,numlines):
        splitline = CoList[x].split(",") #no data longer than a day allowed
        times = splitline[0]
        times = times.split()
        times = times[1]
        times_split = times.split(":",3)
        hours = 3600*float(times_split[0])
        minutes = 60*float(times_split[1])
        seconds = float(times_split[2])
        print(seconds)
        timestamps[x] = hours + minutes + seconds
        data_value = splitline[3]
        values[x] = data_value
        print(timestamps)
    
    scale_factor = 2
    twopi = 2*np.pi
    samp_rate = (1/17)
    Nyquist_frequency = samp_rate / 2
    Base_frequency = 1/((timestamps[-1]-timestamps[0])/2)
    frequencies = np.linspace(Base_frequency, Nyquist_frequency, 10000)*twopi
    offset_data = values - np.mean(values)
    amplitude_spectral_densities = [lombscargle(timestamps, offset_data, frequencies, normalize=False)]
    ASD = amplitude_spectral_densities[0]
    
    return ASD, frequencies 
        
        
        
        
        
        
        
        
        
        
        
        
        
        
