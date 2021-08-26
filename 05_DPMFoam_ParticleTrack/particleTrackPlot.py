# -*- coding: utf-8 -*-
"""
Created on Thu Aug 26 08:34:10 2021

@author: wiese
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def str2list(string_as_list):
    r_list = []
    list_ = string_as_list.replace(",","").replace("'", "").replace("[", "").replace("]", "").split(' ')   
    for element in list_:
        r_list.append(float(element))
    return r_list

if __name__ == '__main__':

    print('\nRunning Script')
    #set correct environment
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    print('\nLoading Data')
    #load data
    data = pd.read_csv('Particles.csv')

    print('\nStarting Ploting')
    #generate plot
    fig = plt.figure(figsize=(7, 7))
    ax = fig.add_subplot(111, projection='3d')

    #set number of particles tracked
    counter = 50 
    keys = np.random.randint(len(data.columns)-1, size=counter)
    
    num_particles = counter
    for key in keys:
        try:
            ax.plot(str2list(data[f'P{key}'][0]),str2list(data[f'P{key}'][1]),str2list(data[f'P{key}'][2]),'-s',markersize=2)
            counter -= 1
            print(f'\n{counter: >7} Particles to go')
        except:
            print(f'\nSomething did not work with key: {key}')
        if counter == 0:
            break
    print('\nFinishing Plot')
    plt.title(f'{num_particles} random Particlepaths\nplotted over {len(str2list(data["P0"][0]))} timesteps',fontsize=16)
    print('\nSaving Plot')
    plt.savefig('ExamplePlot.png',bbox_inches='tight')
    print('\nDone! Check the png image in the folder')
