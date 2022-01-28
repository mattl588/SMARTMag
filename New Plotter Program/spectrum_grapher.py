# -*- coding: utf-8 -*-
"""
Created on Tue Nov  2 23:51:33 2021

@author: Matt Lacaire 
"""
import matplotlib.pyplot as plt
import flc100_processor
import ldat_processor_new
import numpy as np
import datetime
import rm3100_processor

if __name__ == "__main__":

    flc100data, flc100freq, flc100title = FLC_Info()
    rm3100data, rm3100freq = RM3100_Analyzer(path = "rm3100_data/rm_data.txt")
    UTC = datetime.timezone.utc
    sensor_07043= (datetime.datetime(2021, 8, 4, 2, 10, 0, tzinfo=UTC),datetime.datetime(2021, 8, 4, 3, 26, 40, tzinfo=UTC))
    #replace with a few hours of info
    sensor_07028 = (datetime.datetime(2021, 7, 29, 2, 10, 0, tzinfo=UTC),datetime.datetime(2021, 7, 29, 3, 26, 40, tzinfo=UTC))
    black_sensor = (datetime.datetime(2021, 8, 28, 0, 0, 0, tzinfo=UTC),datetime.datetime(2021, 8, 28, 3, 16, 40, tzinfo=UTC))
    test_sensor = (datetime.datetime(2021, 8, 19, 0, 0, 0, tzinfo=UTC),datetime.datetime(2021, 8, 19, 3, 16, 40, tzinfo=UTC))
    freq_07043, amplitude_07043 = LDAT_ASD(sensor_07043)
    freq_07028, amplitude_07028 = LDAT_ASD(sensor_07028)
    freq_black, amplitude_black = LDAT_ASD(black_sensor) 
    freq_test, amplitude_test = LDAT_ASD(test_sensor)
    
    fig, ax = plt.subplots(3,2)
    ax[0,0].loglog(flc100freq,flc100data, color = "red")
    ax[0,0].set_title("FLC-100")
    ax[0,1].loglog(freq_07043, amplitude_07043[0])
    ax[0,1].set_title("07043")
    ax[1,1].loglog(freq_07028, amplitude_07028[0])
    ax[1,1].set_title("07028")
    ax[2,1].loglog(freq_black, amplitude_black[0])
    ax[2,1].set_title("Unlabeled Sensor")
    ax[1,0].loglog(rm3100freq, rm3100data, color = "green")
    ax[1,0].set_title("RM3100 Y-Axis")
    ax[2,0].loglog(freq_test, amplitude_test[0])
    ax[2,0].set_title("Test Sensor")

    fig.set_size_inches(np.asarray([1920,1080])/fig.dpi)

    fig.suptitle("Lab ASD Graphs", size = 36)
    
    
