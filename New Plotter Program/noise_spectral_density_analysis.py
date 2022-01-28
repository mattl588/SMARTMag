#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 19 09:10:16 2021

@author: stellarremnants
"""
# =============================================================================
# Imports
# =============================================================================
import datetime
import numpy as np
# import time
import matplotlib.pyplot as plt
from scipy.signal import lombscargle

from ldat_processor import load_ldat_datetime_search

# %%
# =============================================================================
# Input Paramters
# =============================================================================
verbose = True
UTC = datetime.timezone.utc
#start_datetime = datetime.datetime(2021, 8, 4, 2, 10, 0, tzinfo=UTC) # 2021, 7, 27, 1, 40
#end_datetime = datetime.datetime(2021, 8, 4, 2, 26, 40, tzinfo=UTC) # 2021, 7, 28, 19, 20
#start_datetime = datetime.datetime(2021, 7,29,2,10,0, tzinfo=UTC)
#end_datetime = datetime.datetime(2021, 7,29,2,26,40, tzinfo=UTC)
start_datetime = datetime.datetime(2021, 8, 28, 0, 0, 0, tzinfo=UTC)
end_datetime = datetime.datetime(2021, 8, 28, 0, 16, 40, tzinfo=UTC)

# %%
# =============================================================================
# Data Load-in
# =============================================================================
fglog_data_array = load_ldat_datetime_search(
    start_datetime=start_datetime, 
    end_datetime=end_datetime,
    start_dir = "./noise_test_fglog_ldats")

fglog_data_array = fglog_data_array.T
fglog_timestamps = fglog_data_array[0]
fglog_data = fglog_data_array[1:]
fglog_len = fglog_data.shape[1]
init_fglog_timestamp = fglog_timestamps[0]
fglog_time_elapsed = fglog_timestamps-init_fglog_timestamp

#%%
# =============================================================================
# Time Series Plot
# =============================================================================
naxes = 3
ndiff = 1
ntot = naxes+ndiff
ax_range = range(ndiff, ntot)

fig, axes = plt.subplots(nrows=ntot,ncols=1, sharex=True)
fig.set_size_inches(np.asarray([1920,1080])/fig.dpi)
fig.suptitle(f"TEST Station Noise Analysis Data\n{start_datetime.strftime('%Y-%m-%d %H:%M:%S')} -> {end_datetime.strftime('%Y-%m-%d %H:%M:%S')}")
# twinaxes = np.asarray([plt.twinx(ax) for ax in axes])
colors = [
    ["red", "green", "blue"], 
    # ["green", "blue", "purple"],
    # ["black", "black", "black"]
    ]
axis_labels = ["X", "Y", "Z"]

mean_adjusted_fglog_data = np.asarray([fglog_data[i] - np.mean(fglog_data[i]) for i in range(3)]) #noise-type data
axes[-1].set_xlabel("Time elapsed [s]")

for i in range(naxes):
    
    if ndiff == 1:
        axes[0].plot(fglog_time_elapsed, mean_adjusted_fglog_data[i], color=colors[0][i], alpha=0.75, label=f"fglog {axis_labels[i]} mean adj.")
    ax_index = ax_range[i] #plotting stuff 
    axes[ax_index].set_ylabel(f"{axis_labels[i]} Field [nT]")
    axes[ax_index].plot(fglog_time_elapsed, fglog_data[i], color=colors[0][i], alpha=0.75, label="fglog data")
    axes[ax_index].legend(loc="upper left")
if ndiff == 1: 
    axes[0].legend(loc="upper left")
    axes[0].set_ylabel("Delta from Mean [nT]")
    
# %%
# =============================================================================
# Frequency Analysis
# =============================================================================
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

#if False:
    #use_data = fglog_data
#else:
use_data = np.asarray([fglog_data[i]-np.mean(fglog_data[i]) for i in range(3)])

amplitude_spectral_densities = [lombscargle(fglog_time_elapsed, use_data[i], frequencies, normalize=False) for i in range(3)]

# %%
# =============================================================================
# Amplitude Spectral Density Plot
# =============================================================================


ampfig, ampaxes = plt.subplots(nrows=3, ncols=1) #good
ampfig.set_size_inches(np.asarray([1920,1080])/ampfig.dpi) #good 
ampfig.suptitle(f"TEST Station Noise Analysis Amplitude Spectral Density\n{start_datetime.strftime('%Y-%m-%d %H:%M:%S')} -> {end_datetime.strftime('%Y-%m-%d %H:%M:%S')}")
#good
ampaxes[-1].set_xlabel("Frequency [Hz]") #good
axis_labels = ["X", "Y", "Z"]  #good
amp_colors = ["red", "green", "blue"] #good
for i in range(3):
    ampaxes[i].set_ylabel(f"{axis_labels[i]} Axis ASD [nT]")
    ampaxes[i].loglog(frequencies/PI2, amplitude_spectral_densities[i], color=amp_colors[i])
    #ampaxes[i].set_ylim([10e-5,10e4])
# %%
# =============================================================================
# Power Spectral Density Plot
# =============================================================================


powfig, powaxes = plt.subplots(nrows=3, ncols=1)
powfig.set_size_inches(np.asarray([1920,1080])/powfig.dpi)
powfig.suptitle(f"Basement Sensor Noise Analysis Power Spectral Density\n{start_datetime.strftime('%Y-%m-%d %H:%M:%S')} -> {end_datetime.strftime('%Y-%m-%d %H:%M:%S')}")

powaxes[-1].set_xlabel("Frequency [Hz]")
axis_labels = ["X", "Y", "Z"]
pow_colors = ["red", "green", "blue"]
for i in range(3):
    powaxes[i].set_ylabel(f"{axis_labels[i]} Axis PSD [$nT^2$]")
    powaxes[i].loglog(frequencies/PI2, amplitude_spectral_densities[i]**2, color=pow_colors[i])
    #powaxes[i].set_ylim([10e-8,10e-1])