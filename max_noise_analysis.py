# -*- coding: utf-8 -*-
"""
Created on Thu Jul 29 17:10:23 2021

@author: Matt Lacaire

File that takes in magnetometer data from Joseph Merrill's ldat_processor.py, splits arrays into a number
of pieces, calculates maximum values, and averages them. This is used in UCLA GMAG magnetometer 
noise analysis.
"""

import numpy as np
from ldat_processor import load_ldat_datetime_search
import math
import datetime

#%%
def axis_noise_analysis(numsplits, axisarray): #input the number of times the array is split (how often means are taken) and the array of changing mag. field..)
    mean_index = math.floor(len(axisarray) / numsplits)
    output_array = np.zeros(numsplits) #array that stores maximum  noise values found
    for x in range (numsplits - 1):
        chopped_array = axisarray[(x*mean_index):(x+1)*mean_index]
        output_array[x] = np.max(chopped_array)
    output_array[numsplits-1] = np.max(axisarray[(numsplits - 1)*mean_index:])
    true_mean_noise = np.mean(output_array)
    return true_mean_noise
#%%if __name__ == "__main__":
    
    start_datetime = datetime.datetime(2021,8,28,00,tzinfo=UTC)
    end_datetime = datetime.datetime(2021,8,28,23,tzinfo=UTC)
    ldat_data_array = load_ldat_datetime_search(
    start_datetime=start_datetime, 
    end_datetime=end_datetime,
    start_dir = "./noise_test_fglog_ldats")    
    ldat_data_array = ldat_data_array.T #transpose array
    ldat_data = ldat_data_array[1:] #removing timestamps
    numsplits = 24
    result = np.zeros(3)
    for x in range(3):
        difference_data = np.asarray(ldat_data[x] - np.mean(ldat_data[x]))
        print(difference_data)
        result[x] = axis_noise_analysis(numsplits, difference_data)


    print(f"Average Max Noise in X, Y, Z: {result[0]:.3f}nT, {result[1]:.3f}nT, {result[2]:.3f}nT")

    #last_index = axis_array_size - (numsplits - 1) * mean_index #last remainder index length. Not actually necessary.