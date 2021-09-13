# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 12:58:46 2021

@author: Lukas Schaub
"""
import os
import pickle
from get_Particles import Particle
import numpy as np

def num_zones(dangerzones_file):
    """
    Determine the unique values in a list of dangerzones
    """
    values = []
    
    with open(dangerzones_file,'r') as file:
        
        # readfile
        a = file.read()
        b = a.split('\n')
        file.close()
        # loop until
        loop = int(b[20])+22
        
        for i in range(22,loop):
            if b[i] not in values:
                values.append(b[i])
    
    return len(values)

def read_zones(path):
    """
    Read information about cells form a file
    """
    values = []
    with open(path,'r') as file:
        
        # readfile
        a = file.read()
        b = a.split('\n')
        
        # loop until
        loop = int(b[20])+22
        
        for i in range(22,loop):
            values.append(int(b[i]))
                 
    return values
def read_locations(path):
    """
    Read coordinates of cell centres form a file
    """
    locations = []
    with open(path,'r') as file:
        
        # readfile
        a = file.read()
        b = a.split('\n')
        
        # loop until
        loop = int(b[20])+22
        
        for i in range(22,loop):
            c = b[i].replace('(','').replace(')','').split(' ')
            loc = [float(c[0]), float(c[1]), float(c[2])]
            locations.append(loc)
                 
    return locations

def read_particledata(particledata):
        with open('particle.data', 'rb') as filehandle:
        #read the data from binary data stream
            particles,particle_space = pickle.load(filehandle)
            filehandle.close()
            return particles, particle_space
        
"""def map_particles_to_cells(particle_list,cell_list):
    """
    Mapping the particle locations to the nearest cell location for further 
    determination of lifelines.
    """
    #get new lists from list of cell locations
    x_list, y_list, z_list, new_particles = [], [], [], []
    
    for cell in cell_list:
        x_list.append(cell[0])
        y_list.append(cell[1])
        z_list.append(cell[2])
        
    #define a function to search the nearset value in a list by determing the 
    #smallest absolute difference between a given value and values in a list
    absolute_difference = lambda list_value : abs(list_value - particle_value)
    
    for particle in particle_list:
        for i in range(len(particle.x)):
            particle_value = particle.x[i]
            particle.x[i] = min(x_list,key=absolute_difference)
            particle_value = particle.y[i]
            particle.y[i] = min(y_list,key=absolute_difference)
            particle_value = particle.z[i]
            particle.z[i] = min(z_list,key=absolute_difference)
        new_particles.append(particle)
    return new_particles"""

def particle_lifelines(particle_list,cell_list,zones,num_zones):
    
    end_particles = []
    for particle in particle_list:
        for i in range(len(particle.x)):
            points_ = []
            for point in cell_list:
                points_.append(((point[0]-particle.x[i])**2+(point[1]-particle.y[i])**2+(point[2]-particle.z[i])**2)**(1/2))
            particle.value_index.append(points_.index(min(points_)))
        end_particles.append(particle)
    
    for particle in particle_list:
        for i in particle.value_index:
            particle.value_history.append(zones[i])
        
        zone_dist = {}
        for key in range(1,num_zones+1):
            zone_dist[key] = 0
            for element in particle.value_history:
                if element == key:
                    zone_dist[key] += 1
            zone_dist[key] = zone_dist[key]/len(particle.x)
                    
        particle.zone_dist = zone_dist
        
    return end_particles

def particle_state_transions(list_of_particles,num_states):
    
    for particle in list_of_particles:
        # print(particle)
        #get the list of states for a particle
        list_of_states = particle.value_history
        out = np.zeros((num_states,num_states)) #numpy
        
        for i in range(len(list_of_states)-1):
            curr_ = list_of_states[i]
            next_ = list_of_states[i+1]
            out[curr_-1][next_-1] += 1
        
        for n in range(len(out)):
            line_sum = sum(out[n])
            for m in range(len(out)):
                
                if out[n][m] != 0:
                    out[n][m] = out[n][m]/line_sum
                
        particle.state_transions = out
    return list_of_particles


if __name__ == '__main__':
    
    print('Running Script')
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    
    print('\nReading files for zones, coordinates and particles')
    number_of_zones = num_zones('dangerzones')
    zones = read_zones('dangerzones')
    coordinates = read_locations('C')
    particles, particle_space = read_particledata('particle.data')
    
    print('\nMapping particles to nearest cell center location')
    #new_particles = map_particles_to_cells(particles,coordinates)
    new_particles = particles
    print('\nDetermine the lifelines of the particles')
    end_particltes = particle_lifelines(new_particles,coordinates,zones,number_of_zones)
    end_particltes = particle_state_transions(end_particltes,number_of_zones)
    state_trans = np.zeros((3,3))
    for particle in end_particltes:
        state_trans+=particle.state_transions
        
    if sum(state_trans[0]) != 0:
        state_trans[0] = state_trans[0]/sum(state_trans[0])
    if sum(state_trans[1]) != 0:
        state_trans[1] = state_trans[1]/sum(state_trans[1])
    if sum(state_trans[2]) != 0:
        state_trans[2] = state_trans[2]/sum(state_trans[2])
    
    print('\nThe State transion matrix for this problem looks as follows:')
    print(state_trans)
    
    print('Where the long-term steady-state-solution vector is:')
    print()
    
"""
ToDO:
-----
Check lines 79 to 105 as they might be redundant!
"""  
