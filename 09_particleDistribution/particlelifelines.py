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

def system_state_transion(list_of_particles, Number_of_states):
    
    P = np.zeros((Number_of_states,Number_of_states)) 
    for particle in list_of_particles:
        P+=particle.state_transions
        
    for i in range(Number_of_states):
        if sum(P[i]) != 0:
            P[i] = P[i]/sum(P[i])
    
    return P

def long_term_steady_state(P):
    """
    Assuming Av=b where v is the steady-state-transion probability
    A is equal to the transposed state transion probability matrix with an added line to describe
    the n values where n is representing the number of states
    b is equal to a column vector of shape n+1 where all values are 0 but the last one which is equal to 1
    """
    
    A = np.append(np.transpose(P)-np.identity(len(P)),[[1,1,1]],axis=0)
    b = np.transpose(np.array([[0,0,0,1]]))
    
    v = np.linalg.solve(np.transpose(A).dot(A),np.transpose(A).dot(b))
    
    for state in range(len(P)):
        print(f'State {state}: {v[state]}')
    
    return v
                  
if __name__ == '__main__':
    

    print('Running Script')
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    
    print('\nReading files for zones, coordinates and particles')
    number_of_zones = num_zones('dangerzones')
    zones = read_zones('dangerzones')
    coordinates = read_locations('0/C')
    particles, particle_space = read_particledata('particle.data')
    
    print('\nMapping particles to nearest cell center location')
    #new_particles = map_particles_to_cells(particles,coordinates)
    new_particles = particles
    print('\nDetermine the lifelines of the particles')
    end_particles = particle_lifelines(new_particles,coordinates,zones,number_of_zones)
    end_particles = particle_state_transions(end_particles,number_of_zones)
    
    
    P = system_state_transion(end_particles,3)
    print(f'\nThe State transion matrix for this problem looks as follows:\n{P}')
    
    
    print('\n\nWhere the long-term steady-state-solution vector is:\n')
    steady_state = long_term_steady_state(P)
    
### To Do
### Modify the output in lines 79 to 102 --> progressbar or something
###