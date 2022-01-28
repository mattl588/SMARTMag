# -*- coding: utf-8 -*-
"""
Created on Sun Nov  7 15:48:49 2021

@author: Matt Lacaire
"""

import datetime
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import lombscargle
from ldat_processor import load_ldat_datetime_search

UTC = datetime.timezone.utc
#start_datetime = datetime.datetime(2021, 8, 4, 2, 10, 0, tzinfo=UTC) # 2021, 7, 27, 1, 40
#end_datetime = datetime.datetime(2021, 8, 4, 2, 26, 40, tzinfo=UTC) # 2021, 7, 28, 19, 20
#start_datetime = datetime.datetime(2021, 7,29,2,10,0, tzinfo=UTC)
#end_datetime = datetime.datetime(2021, 7,29,2,26,40, tzinfo=UTC)
start_datetime = datetime.datetime(2021, 8, 28, 0, 0, 0, tzinfo=UTC)
end_datetime = datetime.datetime(2021, 8, 28, 0, 16, 40, tzinfo=UTC)


def LDAT_ASD(start_datetime, end_datetime):
    fglog_data_array = load_ldat_datetime_search(
    start_datetime=start_datetime, 
    end_datetime=end_datetime)
    start_dir = "."
    fglog_data_array = fglog_data_array.T
    fglog_timestamps = fglog_data_array[0]
    fglog_data = fglog_data_array[1:]
    fglog_len = fglog_data.shape[1]
    init_fglog_timestamp = fglog_timestamps[0]
    fglog_time_elapsed = fglog_timestamps-init_fglog_timestamp
    
    SCALE_FACTOR = 2 #what is this? 
    PI2 = 2*np.pi
    #Nyquist_frequency = (1/(np.mean(np.diff(fglog_time_elapsed))))/2   #fixed.
    Base_frequency = 1/((fglog_time_elapsed[-1]-fglog_time_elapsed[0])/2)+0.002 #total time is in parentheses.
    Nyquist_frequency = 1
    #Base_frequency = 10e-4
    #the base frequency is the lowest measurable frequency. 
    #frequencies = np.linspace(Base_frequency,
                              #Nyquist_frequency/SCALE_FACTOR, 
                              #10000)*PI2
    frequencies = np.linspace(Base_frequency, Nyquist_frequency, 10000)*PI2

    use_data = np.asarray([fglog_data[i]-np.mean(fglog_data[i]) for i in range(3)])
    
    amplitude_spectral_densities = [lombscargle(fglog_time_elapsed, use_data[i], frequencies, normalize=False) for i in range(3)]
    
    return frequencies, amplitude_spectral_densities
