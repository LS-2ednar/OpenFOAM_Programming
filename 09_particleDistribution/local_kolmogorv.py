"""
Calculating local energy dissipationrate
"""
import os

def get_numbered_directories():
    all_dirs = next(os.walk('.'))[1]
    num_dirs = []
    for di in all_dirs:
        try:
            if '.' not in di:
                num_dirs.append(int(di))
            else:
                num_dirs.append(float(di))
        except:
            continue
    num_dirs.sort()
    return num_dirs

def get_latesttime():
    return get_numbered_directories()[-1]

def read_locations(path):
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

def read_epsilons(path):
    pressures = []
    with open(path,'r') as file:
        
        # readfile
        a = file.read()
        b = a.split('\n')
        
        # loop until
        loop = int(b[20])+22
        
        for i in range(22,loop):
            pressures.append(float(b[i]))
                 
    return pressures

def read_volumes(path):
    """
    Works identical tehn read_pressures. Difference is output list is a list of folats
    """
    return read_epsilons(path)

def calculate_local_kolmogorov(epsilons, kinematicViscosity = 6.922e-4, unit = 'µm'): #assuming 37°C
    """
    Calculates local kolmogorov length scale based on the given kinematic viscosity and energydissipationrate
    """
    kolmogorov = []
    if unit == 'µm':
        print('Kolmogorv length scale in µm')
    else:
        print('Kolmogorv length scale in m')
        
    for i in range(0,len(epsilons)):
        if unit == 'µm':
            kolmogorov.append((kinematicViscosity/(epsilons[i]**3))**(1/4)*1000000)
        else:
            kolmogorov.append((kinematicViscosity/(epsilons[i]**3))**(1/4))
        
    return kolmogorov

def write_kolmogorov(list_of_data):
    head="""/*--------------------------------*- C++ -*----------------------------------*\\
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
    class       volScalarField;
    location    "500";
    object      kolmogorov;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

dimensions      [0 1 0 0 0 0 0];

internalField   nonuniform List<scalar>""" 
    middle = f"""\n{len(list_of_data)}
(
"""
    tail =""")
;

boundaryField
{
    rotor
    {
        type            zeroGradient;
    }
    stator
    {
        type            zeroGradient;
    }
    front
    {
        type            empty;
    }
    back
    {
        type            empty;
    }
}


// ************************************************************************* //"""
    with open('kolmogorov','w') as file:
        file.write(head)
        file.write(middle)
        for element in list_of_data:
            file.write(str(element)+'\n')
        file.write(tail)
        file.close()
    return

def write_zones(list_of_data, cell_diameter=1.5e-5):
    """
    The higher the zone number more critical is the situatlion for the cells
    0 is equal to 110% of the cells diameter and should not affect the cells
    1 is equal to 105% of the cells diameter and might affect them
    2 is equal to less then 105% of the cells diameter effects are certain
    """
    head="""/*--------------------------------*- C++ -*----------------------------------*\\
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
    class       volScalarField;
    location    "500";
    object      DangerZones;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

dimensions      [0 0 0 0 0 0 0];

internalField   nonuniform List<scalar>""" 
    middle = f"""\n{len(list_of_data)}
(
"""
    tail =""")
;

boundaryField
{
    rotor
    {
        type            zeroGradient;
    }
    stator
    {
        type            zeroGradient;
    }
    front
    {
        type            empty;
    }
    back
    {
        type            empty;
    }
}


// ************************************************************************* //"""
    with open('dangerzones','w') as file:
        file.write(head)
        file.write(middle)
        for element in list_of_data:
            if element >= cell_diameter*1.1:                                    #if modifications are needed ajust here 
                file.write(str(1)+'\n')
            elif element > cell_diameter*1.05 and element < cell_diameter*1.1:  #if modifications are needed ajust here
                file.write(str(1)+'\n')
            else:
                file.write(str(2)+'\n')
        file.write(tail)
        file.close()
    return

if __name__ == '__main__':

    print('Running Script')
    #select current working directory
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    #get_data_from latest time_point
    epsilons = read_epsilons(f'{get_latesttime()}\\epsilon')
    #calculate kolmogorow values
    kolmorov = calculate_local_kolmogorov(epsilons,unit = 'm')
    print('\nWriting local_kolmogorov_lengthscale file')
    write_kolmogorov(kolmorov)
    print('\nWriting dangerzones file')
    write_zones(kolmorov)
    
