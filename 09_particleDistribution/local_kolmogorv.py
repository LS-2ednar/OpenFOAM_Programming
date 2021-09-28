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
    epsilons = []
    with open(path,'r') as file:
        
        # readfile
        a = file.read()
        b = a.split('\n')
        
        # loop until
        loop = int(b[20])+22
        
        for i in range(22,loop):
            epsilons.append(float(b[i]))
                 
    return epsilons

def read_volumes(path):
    """
    Works identical tehn read_pressures. Difference is output list is a list of folats
    """
    return read_epsilons(path)

def read_tail(File):
    """
    Gets tail of a file
    """
    
    #initialize a counter and tail of a document
    c, tail = 0, ')\n;\n\n'
    
    #try to read the file in windows way
    try:
        with open(f'0\\{File}','r') as f:
            for line in f:
                c += 1
                if c > 21:
                    if 'value' in line:
                        continue
                    elif 'symmetry' in line:
                        tail += '        type symmetry;\n'
                        
                    elif 'type' in line:
                        tail += '        type zeroGradient;\n'
                    else:
                        tail += line
    except:
        with open(f'0/{File}','r') as f:
            for line in f:
                c += 1
                if c > 21:
                    if 'value' in line:
                        continue
                    elif 'symmetry' in line:
                        tail += '        type symmetry;\n'
                        
                    elif 'type' in line:
                        tail += '        type zeroGradient;\n'
                    else:
                        tail += line
    
    return tail

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

def write_kolmogorov(list_of_data,tail):
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
    try:
        with open(f'{get_latesttime()}/kolmogorov','w') as file:
            file.write(head)
            file.write(middle)
            for element in list_of_data:
                file.write(str(element)+'\n')
            file.write(tail)
            file.close()
    except:
        with open(f'{get_latesttime()}\\kolmogorov','w') as file:
            file.write(head)
            file.write(middle)
            for element in list_of_data:
                file.write(str(element)+'\n')
            file.write(tail)
            file.close()       
    return

def write_zones(list_of_data, tail, cell_diameter=1.5e-5):
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
    try:
        with open(f'{get_latesttime()}/dangerzones','w') as file:
            file.write(head)
            file.write(middle)
            for element in list_of_data:
                if element >= cell_diameter*1.1:                                    #if modifications are needed ajust here 
                    file.write(str(1)+'\n')
                elif element > cell_diameter*1.05 and element < cell_diameter*1.1:  #if modifications are needed ajust here
                    file.write(str(2)+'\n')
                else:
                    file.write(str(3)+'\n')
            file.write(tail)
            file.close()
    except:
        with open(f'{get_latesttime()}\\dangerzones','w') as file:
            file.write(head)
            file.write(middle)
            for element in list_of_data:
                if element >= cell_diameter*1.1:                                    #if modifications are needed ajust here 
                    file.write(str(1)+'\n')
                elif element > cell_diameter*1.05 and element < cell_diameter*1.1:  #if modifications are needed ajust here
                    file.write(str(2)+'\n')
                else:
                    file.write(str(3)+'\n')
            file.write(tail)
            file.close()
    return

if __name__ == '__main__':

    print('Running Script')
    #select current working directory
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    #get tail of a document
    tail = read_tail('epsilon')
    #get data from latest time point
    try:
        epsilons = read_epsilons(f'{get_latesttime()}\\epsilon')
    except:
        epsilons = read_epsilons(f'{get_latesttime()}/epsilon')
    #calculate kolmogorow values
    kolmorov = calculate_local_kolmogorov(epsilons, unit = 'm')
    print('\nWriting local_kolmogorov_lengthscale file')
    write_kolmogorov(kolmorov, tail)
    print('\nWriting dangerzones file')
    write_zones(kolmorov, tail)
    
