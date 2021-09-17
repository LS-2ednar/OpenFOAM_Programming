# -*- coding: utf-8 -*-
"""
Generate the Particlelifelines and the state transion 
probability matricies for each particle as well as a 
long term steady state of the system.
"""
import os
import sys
import pickle
from get_Particles import Particle
import get_Particles
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

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

def particle_lifelines(particle_list,cell_list,zone_list,num_zones):
    """
    Generates the particles history in reagards to the values it had to endure.
    
    Parameters:
    particle_list --> list of Particle
    cell_list     --> list of lists
    zone_list     --> list of integers
    num_zones     --> integer
    
    Output:
    end_particles --> list of Particle
                      These Particles have now stroed information about there
                      value_history which shows where they where exposed to
                      the different zones.
    """
    #for each particle get the closest point from the list of cell centeres.
    end_particles = []
    
    #for progressbar
    c, pb = 0,0
    print('Mapping particles to cell-centers for zone determination')
    for particle in particle_list:
        c+= 1
        for i in range(len(particle.x)):
            points_ = []
            for point in cell_list:
                points_.append(((point[0]-particle.x[i])**2+(point[1]-particle.y[i])**2+(point[2]-particle.z[i])**2)**(1/2))
            particle.value_index.append(points_.index(min(points_)))
        end_particles.append(particle)
        
        if c == len(particle_list)//50:
                pb += 1
                sys.stdout.write('\r')
                sys.stdout.write("[%-50s] %d%%" % ('='*pb, 2*pb))
                sys.stdout.flush()
                c = 0
            
            
    #match indecies to zone values
    for particle in particle_list:
        for i in particle.value_index:
            particle.value_history.append(zone_list[i])
            
        # #might be used later
        # zone_dist = {}
        # for key in range(1,num_zones+1):
        #     zone_dist[key] = 0
        #     for element in particle.value_history:
        #         if element == key:
        #             zone_dist[key] += 1
        #     zone_dist[key] = zone_dist[key]/len(particle.x)
                    
        # particle.zone_dist = zone_dist
        
    return end_particles

def particle_state_transions(list_of_particles,num_states):
    """
    Given a list_of_particles and a number of available states (num_states) a state
    transion matrix can be caluclated and is added to each particle.
    """
    
    for particle in list_of_particles:
        #get the list of states for a particle
        list_of_states = particle.value_history
        
        #iniate a nxn zero matrix where n is equal to num_states
        out = np.zeros((num_states,num_states)) 
        
        #increment values in the nxn matrix 
        for i in range(len(list_of_states)-1):
            curr_ = list_of_states[i]
            next_ = list_of_states[i+1]
            out[curr_-1][next_-1] += 1
        
        # get percentages for each value in the system
        for n in range(len(out)):
            line_sum = sum(out[n])
            for m in range(len(out)):
                
                if out[n][m] != 0:
                    out[n][m] = out[n][m]/line_sum
        
        #add the state_transition_probability matrix to the particle
        particle.state_transions = out
    return list_of_particles

def system_state_transion(list_of_particles, Number_of_states):
    """
    Given a list_of_particles the systems average state-transion-probability-matrix (P) is calculated
    """
    P = np.zeros((len(list_of_particles[0].state_transions),len(list_of_particles[0].state_transions))) 
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
    
    A = np.append(np.transpose(P)-np.identity(len(P)),[np.ones(len(P))],axis=0)
    b = np.transpose(np.append(np.zeros(len(P)),1))
    
    v = np.linalg.solve(np.transpose(A).dot(A),np.transpose(A).dot(b))
    
    for state in range(len(P)):
        print(f'State {state}: {v[state]}')
    
    return v

def mc_process_plot(STPM,NumIter=50):
    """
    Given a STPM (state transition probability matrix), a number of cells (NumCells), 
    and a number of iterations (NumIter) the long therm steady state is visualized
    """
    num_states = len(STPM)
    lables = [f'State {i}' for i in range(num_states)]
    
    #state 0 is 100% of pop in the beginnnig
    state=np.array([np.append(1,np.zeros(num_states-1))])
    stateHist=state
    for x in range(NumIter):
        state=np.dot(state,STPM)
        stateHist=np.append(stateHist,state,axis=0)
        dfDistrHist0 = pd.DataFrame(stateHist,columns = lables)
    dfDistrHist0.plot(ylim=(0,1),
                      xlim=(-0.1,NumIter),
                      ylabel = 'Distribution [-]',
                      xlabel = 'State Changes [-]',
                      title = 'longterm steady state\nstarting from State 0')
    plt.show()
    
    #Even distribution of all states
    state=np.array([np.ones(num_states)/num_states])
    stateHist=state
    for x in range(NumIter):
        state=np.dot(state,STPM)
        stateHist=np.append(stateHist,state,axis=0)
        dfDistrHist1 = pd.DataFrame(stateHist,columns = lables)
    dfDistrHist1.plot(ylim=(0,1),
                      xlim=(-0.1,NumIter),
                      ylabel = 'Distribution [-]',
                      xlabel = 'State Changes [-]',
                      title = 'longterm steady state\nstarting from even distribution')
    plt.show()
    
    #state n is 100% of pop in the beginnnig
    state=np.array([np.append(np.zeros(num_states-1),1)])
    stateHist=state
    for x in range(NumIter):
        state=np.dot(state,STPM)
        stateHist=np.append(stateHist,state,axis=0)
        dfDistrHist2 = pd.DataFrame(stateHist,columns = lables)
    dfDistrHist2.plot(ylim=(0,1),
                      xlim=(-0.1,NumIter),
                      ylabel = 'Distribution [-]',
                      xlabel = 'State Changes [-]',
                      title = f'longterm steady state\nstarting from State {num_states-1}')
    plt.show()
    return dfDistrHist1
          
if __name__ == '__main__':
    
    print('Running Script')
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    
    print('\nReading files for zones, coordinates and particles')
    number_of_zones = num_zones('dangerzones')
    zones = read_zones('dangerzones')
    coordinates = read_locations(f'{get_Particles.get_latesttime()}/C')
    particles, particle_space = read_particledata('particle.data')
    
    print('\nDetermine lifelines of particles\n')
    end_particles = particle_lifelines(particles,coordinates,zones,number_of_zones)
    end_particles = particle_state_transions(end_particles,number_of_zones)
    
    
    P = system_state_transion(end_particles,3)
    print(f'\n\nThe State transion matrix for this system looks as follows:\n\n{P}')
    
    
    print('\n\nWhere the long-term steady-state-solution vector is:\n')
    steady_state = long_term_steady_state(P)
    dist = mc_process_plot(P)
    
### To Do
### Add the final values of the state distributions to the plots
###