"""
Generate a kinematicCloud File to work with openFoam this
"""
import os

def get_internalmesh():
    
    #try to read the C file in 0
    if os.path.isfile('0\C'):
        with open('0\C','r') as cFile:
            intMesh = cFile.read().split('\n')
            elements = 22+int(intMesh[20])
            cFile.close()
    
    else:
        print('No C file found trying to create it')
        try:
            os.system('postProcess -func writeCellCentres -latestTime')
            with open('0\C','r') as cFile:
                intMesh = cFile.read().split('\n')
                elements = 22+int(intMesh[20])
                cFile.close()
        except:
            return 'something went wrong'
        
    
    return intMesh[22:elements]


def set_particles(number_of_particles,internalMesh):
    
    
    
    #calculations for startposition seleciton
    pos_postions = len(internalMesh)
    step_difference = pos_postions // number_of_particles
    
    #setup for the file to be written
    head = """/*--------------------------------*- C++ -*----------------------------------*\\
 =========                 |
  \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
   \\    /   O peration     | Website:  https://openfoam.org
    \\  /    A nd           | Version:  8
     \\/     M anipulation  |
\*---------------------------------------------------------------------------*/
FoamFile
{
    version     2.0;
    format      ascii;
    class       vectorField;
    object      kinematicCloudPositions;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

(
"""
    bottom = ')\n\n// ************************************************************************* //'
    
    #writing the file 
    with open('kinematicCloudPositions','w') as file:
        file.write(head)
        index = 0
        for i in range(number_of_particles):
            file.write(internalMesh[index]+'\n')
            index += step_difference
        file.write(bottom)
    return 

if __name__ == '__main__':
    #set current working directory to file location
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    
    #set a number of particles in the internal mesh at the cell centers given.
    set_particles(200,get_internalmesh())
    