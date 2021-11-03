# -*- coding: utf-8 -*-
"""
Created on Wed Oct 20 19:58:05 2021

@author: Matt Lacaire

Script that takes in timestamped .txt files and generates spectral density graphs. 
"""
import numpy as np
import os 
import matplotlib.pyplot as plt
from scipy.signal import lombscargle


class FLC100Analyzer():
    def __init__(self, path):
        self.path = path
        self.f = open(path,"r")
    def processdata(self):
        rawdata = self.f.readlines()
        arraylength = 2000
        timestamps = np.zeros(arraylength)
        values = np.zeros(arraylength)
        for x in range(arraylength):
            splitline = rawdata[x].split(" ",2) #no data longer than a day allowed
            times = splitline[1]
            times_split = times.split(":",3)
            hours = 3600*float(times_split[0])
            minutes = 60*float(times_split[1])
            seconds = float(times_split[2])
            timestamps[x] = hours + minutes + seconds
            data_value = splitline[2].split("nT",1)
            values[x] = data_value[0]
        self.values = values
        self.timestamps = timestamps - timestamps[0] #correcting for offset
        def plotdata(self):
            xaxis = range(0,len(values),1)
            plt.plot(self.timestamps,self.values)
            plt.ylabel("Magnetic Field Magnitude")
            plt.xlabel("Timestamp")
        #plotdata(self)
    def generateSpectralDensity(self):
        scale_factor = 2
        twopi = 2*np.pi
        Nyquist_frequency = 1
        Base_frequency = 1/((self.timestamps[-1]-self.timestamps[0])/2)
        frequencies = np.linspace(Base_frequency, Nyquist_frequency, 10000)*twopi
        offset_data = self.values - np.mean(self.values)
        amplitude_spectral_densities = [lombscargle(self.timestamps, offset_data, frequencies, normalize=False)]
        #plt.loglog(frequencies/twopi,amplitude_spectral_densities[0])
        #plt.xlim([1e-3,1])
        self.frequencies = frequencies / twopi
        self.spectral_density = amplitude_spectral_densities[0]
        

paths = []
numsamples = 5
for x in range(numsamples):
    paths.append(f"flc100_data\log{x}.txt")

objects = []
for y in range(numsamples):
    objects.append(FLC100Analyzer(paths[y]))
    objects[y].processdata()
    objects[y].generateSpectralDensity()
# =============================================================================
#     Ignore this code
#     
# path = "flc100_data\log.txt"
# flc100 = FLC100Analyzer(path)
# flc100.processdata()
# flc100.generateSpectralDensity()
# 
# path2 = "flc100_data\log2.txt"
# flc100_2 = FLC100Analyzer(path2)
# flc100_2.processdata()
# flc100_2.generateSpectralDensity()
# 
# path3 = "flc100_data\log3.txt"
# flc100_3 = FLC100Analyzer(path3)
# flc100_3.processdata()
# flc100_3.generateSpectralDensity()
# =============================================================================

# =============================================================================
# plt.loglog(flc100.frequencies, flc100.spectral_density)
# plt.loglog(flc100_2.frequencies, flc100_2.spectral_density)
# plt.loglog(flc100_3.frequencies, flc100_3.spectral_density)
# plt.show()
# plt.xlim([2e-3,1]) #valid for 1000s of data (2000 points)
# plt.xlabel("Frequency [Hz]")
# plt.ylabel("Noise Amplitude Spectral Density [nT]")
# plt.title("FLC-100 Noise Amplitude Spectral Density Graph")
# =============================================================================

averageASD = objects[0].spectral_density
averageFreq = objects[0].frequencies
for z in range(1,numsamples):
    averageASD = (objects[z].spectral_density + averageASD) / 2
    averageFreq = (objects[z].frequencies + averageFreq)/ 2
    print(averageASD)

plt.loglog(averageFreq, averageASD, color = "cyan")
plt.xlabel("Frequency [Hz]")
plt.ylabel("Noise Amplitude Spectral Density [nT]")
plt.title(f"FLC-100 Noise Amplitude Spectral Density Graph, {numsamples} Datasets")
plt.xlim([2e-3,1])

# =============================================================================
# averageFreq = (objects[0].frequencies + objects[1].frequencies + objects[2].frequencies + objects[3].frequencies + objects[4].frequencies) / numsamples 
# averageASD = (objects[0].spectral_density + objects[1].spectral_density + objects[2].spectral_density + objects[3].spectral_density + objects[4].spectral_density) / numsamples
# plt.loglog(averageFreq, averageASD, color = "orange")
# plt.xlim([2e-3,1])
# plt.xlabel("Frequency [Hz]")
# plt.ylabel("Noise Amplitude Spectral Density [nT]")
# plt.title("FLC-100 Noise Amplitude Spectral Density Graph, Five Datasets")
# 
# #is this scientifically valid to do?
# =============================================================================




