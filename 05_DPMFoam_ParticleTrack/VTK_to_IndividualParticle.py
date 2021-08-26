"""
Extract individual particles from particleTracks.vtk file originated
from OpenFOAMv8 by storing them in a pandas dataframe
"""

import os
import pandas as pd
import matplotlib.pyplot as plt


def list2intList(a_list):
    r_list = []
    for element in a_list:
        r_list.append(int(element))
    return r_list


# """
# Run the script:
# """

if __name__ == '__main__':

    print('Running Script')
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    all_data=[]
    particles = {}
    
    tracks = open('VTK/particleTracks.vtk')
    
    #transform vtk to particle table
    counter = 0
    key = 0
    loop = 999 
    for line in tracks:
        counter += 1
        if counter == 5: 
            loop = line.split(' ')[1]
            print(f'Looping {loop} Datapoints')
        
        if counter > 5 and counter <= int(loop)+5:
            line = line.replace('\n','').split(' ')
            all_data.append([float(line[0]),float(line[1]),float(line[2])])
            # print(line)
            
        if counter == int(loop)+6:
            loop2 = line.split(' ')[1]
        
        if counter > int(loop)+6 and counter <= int(loop)+6+int(loop2):
            line = list2intList(line.replace('\n','').split(' '))
            
            track_list = []
            for i in range(0,line.pop(0)):
                track_list.append(all_data[line[i]])
            particles[f'P{key}'] = track_list
            key += 1
        if counter % 50 == 0 and counter < int(loop):
            print(f'\nPrepareded {counter} of {loop} Particles')
    
    #create dictionary
    names = ['x','y','z']
    for particle in particles:
        x = []
        y = []
        z = []
        for i in range(len(particles[particle])):
            x.append(particles[particle][i][0])
            y.append(particles[particle][i][1])
            z.append(particles[particle][i][2])
        data = [x,y,z]
        particles[particle] = dict(zip(names,data)) 
    
    
    # convert to pandas dataframe
    data = pd.DataFrame.from_dict(particles)

    print(data)
    # save data to excel/csv file
    try:
        data.to_excel('Particles.xlsx')
    except:
        data.to_csv('Particles.csv')
    #functionality test:    
    #fig = plt.figure()
    #ax = fig.add_subplot(111, projection='3d')
    #ax.plot(data.P9.x,data.P9.y,data.P9.z)
    #plt.show()
