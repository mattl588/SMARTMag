# -*- coding: utf-8 -*-
"""
Created on Thu Jul 29 17:10:23 2021

@author: Matt Lacaire

File that takes in magnetometer data from Joseph Merrill's ldat_processor.py, splits arrays into a number
of pieces, calculates maximum values, and averages them. This is used in UCLA GMAG magnetometer 
noise analysis.
"""

import numpy as np
import ldat_processor 
import math

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
#%%
if __name__ == "__main__":

    xaxis = scaled_diff_data[0]
    yaxis = scaled_diff_data[1]
    zaxis = scaled_diff_data[2]
    
    numsplits = 24 #number of arrays each axis is split into. Roughly equal to hours in the can.
    axis_array_size = len(scaled_diff_data[0])
    
    xresult = axis_noise_analysis(numsplits, xaxis)
    yresult = axis_noise_analysis(numsplits, yaxis)
    zresult = axis_noise_analysis(numsplits, zaxis)

    print(f"Average Max Noise in X, Y, Z: {xresult:.3f}nT, {yresult:.3f}nT, {zresult:.3f}nT")

    #last_index = axis_array_size - (numsplits - 1) * mean_index #last remainder index length. Not actually necessary.