# -*- coding: utf-8 -*-
"""
Created on Wed Aug 11 13:28:16 2021

@author: Matt Lacaire

Script that is intended to display commercial magnetometer axis readings in real-time.

"""
from WitMotionCode.py import Hx, Hy, Hz
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np


def shift_1D_array(array, new_val):
    new_array = np.zeros_like(array)
    new_array[:-1] = array[1:]
    new_array[-1] = new_val
    return new_array

def my_animation(
        min = -20000,
        max = 20000,
        data_set_length = 150,
        delay = 50): #in ms
    
    data_set = (np.zeros(data_set_length)) #plotter starts with zeroes 
    x_range = np.arange(150)
    fig,ax=plt.subplots(nrows=1, ncols=1) #subplots. Why?
    
    line, = ax.plot(x_range, data_set, color="blue", ls="-", marker=".", ms=5) #output is object and not tuple
    
    ax.set_ylim([min, max])
    ax.set_xlim([0, data_set_length-1]) #fix later. 
    
    def update_plot(index):
        nonlocal data_set #referencing objects immediately outside of function scope
        nonlocal line 
        new_val = Hx
        data_set = shift_1D_array(data_set, new_val)
        line.set_ydata(data_set)
        
        fig.canvas.draw_idle()
        
        return [line] #returns a list of the line. brackets not necessary.
        
    ani = animation.FuncAnimation(fig, update_plot, interval=delay)
    '''Contains all of the while loops that keep the thing going. '''
    return fig, ax, ani


if __name__ == "__main__":
    fig, ax, ani = my_animation() #these objects need to stay, or they're cleaned up. 
    plt.show()
    