"""
Particle Object to store a Particles travelroute and its age
"""
import pickle

class Particle:
    """
    Position descibed by x, y, z
    Age described by timesteps which are currently updated later
    """
    def __init__(self,x,y,z,name=None):
        #location
        self.name = name
        self.x = x
        self.y = y
        self.z = z
        self.age = 0
        
    def __str__(self):
        if self.name != None:
            try:
                return f'{self.name}\nx: {self.x}\ny: {self.y}\nz: {self.z}\nage: {self.age}'
            except:
                return f'{self.name}\nx: {self.x}\ny: {self.y}\nz: {self.z}'
        else:
            try:
                return f'x: {self.x}\ny: {self.y}\nz: {self.z}\nage: {self.age}'
            except:
                return f'x: {self.x}\ny: {self.y}\nz: {self.z}'
    
    def update_age(self,dt):
        self.age = len(self.x)*dt
    
#Helper Functions      
import os

def list2intList(a_list):
    """
    Function turns a list of strings to a list of integers
    """
    r_list = []
    for element in a_list:
        r_list.append(int(element))
    return r_list

def get_particle_positions(filename,ps = False):
    """
    Function generates list of Particles given a vtk datafile. Using the Keyword
    Argument ps it is posible to get the particle space.
    """
    
    #initialize lists and variables
    x,y,z, particle_length,particle_list = [],[],[],[],[]
    last, new, particle_number = 0,0,0
    
    #opening given vtk file
    print(f'\nOpening file: {filename:>20}')
    tracks = open(f'{filename}')
    
    #transform vtk to list of particles
    counter = 0
    loop = 0 
    for line in tracks:
        counter += 1
        if counter == 5: 
            loop = line.split(' ')[1]
            print(f'\nReading Datapoints: {loop:>9}')
        
        if counter > 5 and counter <= int(loop)+5:
            line = line.replace('\n','').split(' ')
            # print(line)
            x.append(float(line[0]))
            y.append(float(line[1]))
            z.append(float(line[2]))
            
        if counter == int(loop)+6:
            loop2 = line.split(' ')[1]
        
        if counter > int(loop)+6 and counter <= int(loop)+6+int(loop2):
            
            line = list2intList(line.replace('\n','').split(' '))
            particle_length.append(line[0])

    print(f'\nInitialize creation of {loop2} particles')
        
    for i in particle_length:
        new += i
        particle_list.append(Particle(x[last:new],y[last:new],z[last:new],f'P{particle_number}'))
        # print(x[last:new])
        last = new
        particle_number += 1
    
    def particle_space():
        """
        This defines the particle space given the initial vtk file as a list 
        of tuples of form [(min x, max x ), (min y, max y), (min z, max z)]
        """
        return [(min(x),max(x)),(min(y),max(y)),(min(z),max(z))]
    
    if ps == True:
        return particle_list, particle_space()
    else:
        return particle_list

# """
# Run the script:
# """

if __name__ == '__main__':

    print('Running Script')
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    try: #to read the VTK/particleTracks.vtk file otherwise generate & read it
        particles,particle_space = get_particle_positions('VTK/particleTracks.vtk',ps = True)
    except:
        os.system('particleTracks')
        particles,particle_space = get_particle_positions('VTK/particleTracks.vtk',ps = True)
    
    with open('particle.data', 'wb') as filehandle:
        # store the data as binary data stream
        pickle.dump([particles,particle_space], filehandle)
        
    
    # to work with this data you will need to do this in other code
    # import ParticleClass
    # with open('particle.data', 'rb') as filehandle:
    #     # read the data from binary data stream
    #     particles,particle_space = pickle.load(filehandle)