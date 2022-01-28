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
        arraylength = 7200
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
 
        
def FLC_Info():
    path = "flc100_data\log0.txt" #the location of the data to be analyzed
    data = FLC100Analyzer(path)
    data.processdata()
    data.generateSpectralDensity()
    ASD = data.spectral_density
    freq = data.frequencies


    plt.loglog(freq, ASD, color = "cyan")
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("Noise Amplitude Spectral Density [nT]")
    title = f"FLC-100 Noise Amplitude Spectral Density, One Long Dataset"
    plt.title(title)
    plt.xlim([2e-3,1])
    
    return ASD, freq, title 

def FLC_Info_Multiple_Sets():
    paths = []
    numsamples = 6
    for x in range(numsamples):
        paths.append(f"flc100_data\log{x}.txt")

    objects = []
    for y in range(numsamples):
         objects.append(FLC100Analyzer(paths[y])) #putting object into array 
         objects[y].processdata()
         objects[y].generateSpectralDensity()

    averageASD = objects[0].spectral_density
    averageFreq = objects[0].frequencies
    for z in range(1,numsamples):
        averageASD = (objects[z].spectral_density + averageASD) / 2 #complex means of averaging data sets. 
        averageFreq = (objects[z].frequencies + averageFreq)/ 2
        print(averageASD)

    plt.loglog(averageFreq, averageASD, color = "cyan")
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("Noise Amplitude Spectral Density [nT]")
    title = f"FLC-100 Noise Amplitude Spectral Density Graph, {numsamples} Datasets"
    plt.title(title)
    plt.xlim([2e-3,1])
    
    return averageASD, averageFreq, title 


def FLCNoiseVal():
    file = "flc100_data\log1.txt"
    data = FLC100Analyzer(file)
    data.processdata()
    noiseval = np.diff(data.values)
    noiseval = np.mean(np.abs(noiseval))
    print(noiseval)
    
    

#FLCInfo()


