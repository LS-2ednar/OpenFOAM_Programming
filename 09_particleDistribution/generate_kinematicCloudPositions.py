"""
Generating Randomly placed particles in a OpenFOAM 
"""
import numpy as np

def generate_file(x, y, z, numPoints=100):
    print('Genearing KinematicCloudPosition file')
    def random_position():
        x_min, x_max, y_min, y_max, z_min,z_max = min(x), max(x), min(y), max(y), min(z), max(z)
        
        ret_arg = ''
        for i in range(numPoints):
            Px, Py, Pz = round(np.random.uniform(x_min,x_max),4), round(np.random.uniform(y_min,y_max),4), round(np.random.uniform(z_min,z_max),4)
            ret_arg += f'({Px} {Py} {Pz})\n'
        
        return ret_arg
    
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
    print(head+random_position()+')\n\n// ************************************************************************* //')
    # output = head+random_position()+')\n'+'\n// ************************************************************************* //'

    with open('kinematicCloudPositions','w') as file:
        file.write(head)
        file.write(random_position())
        file.write(bottom)
        file.close()
    print('Done!')
    return 

def get_solutuin_space(filename):
    
    x,y,z = 0,0,0
    
    return x,y,z


if __name__ == '__main__':
    print(1)
    
