"""
Calculating local energy dissipationrate
"""
import os
import pandas as pd
import numpy as np
import sys

def get_numbered_directories():
    """
    generates a list of numbered directories
    """
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
    """
    Returns latesttime of a subfolder
    """
    return get_numbered_directories()[-1]

def read_locations(path):
    """
    Given a path to an locations file the epsilons are put in a list
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

def read_epsilons(path):
    """
    Given a path to an epsilon file the epsilons are put in a list
    """
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

def read_gradU(path):
    """
    Works identical tehn read_locations. Difference is output list is a list of floats
    """
    grad = []
    with open(path,'r') as file:
        
        # readfile
        a = file.read()
        b = a.split('\n')
        
        # loop until
        loop = int(b[20])+22
        
        for i in range(22,loop):
            c = b[i].replace('(','').replace(')','').split(' ')
            gra = [float(c[0]), float(c[1]), float(c[2]), float(c[3]),float(c[4]),float(c[5]),float(c[6]),float(c[7]),float(c[8])]
            grad.append(gra)
                 
    return grad

def read_U(path):
    """
    Works identical to read_locations. Difference is output list is a list of floats
    """
    return read_locations(path)

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

def calculate_stresses():
    
    #access latest time
    latest_time = get_latesttime()
    
    #generate needed data
    try:
        os.system('postProcess -func time')
        os.system('postProcess -func writeCellVolumes')
        os.system('simpleFoam -postProcess -func "grad(U)" -field U')
        print()
    except:
        print('Something went worng')
        
    #open needed files for further calculation
    U = read_U(str(latest_time)+'/U')
    gradU = read_gradU(str(latest_time)+'/grad(U)')
    
    #generate dataframe
    grad = pd.DataFrame(gradU)
    grad['normal'] = np.nan
    grad['shear'] = np.nan
    
    #for progressbar
    c, pb = 0,0
    print('\nCalculating Normal- and Shearforces:')
    for i in range(len(U)):
        
        #determine normal stress
        Umag = (U[i][0]**2 + U[i][1]**2 + U[i][2]**2)**(1/2) + 10**(-15)
        Unull = ((U[i][1]-U[i][2])**2 + (U[i][2]-U[i][0])**2 + (U[i][0]-U[i][1])**2)**(1/2) + 10**(-15)
        N1 = (U[i][0]/Umag*gradU[i][0] + U[i][1]/Umag*gradU[i][3] + U[i][2]/Umag*gradU[i][6]) * U[i][0]/Umag 
        N2 = (U[i][0]/Umag*gradU[i][1] + U[i][1]/Umag*gradU[i][4] + U[i][2]/Umag*gradU[i][7]) * U[i][1]/Umag 
        N3 = (U[i][0]/Umag*gradU[i][2] + U[i][1]/Umag*gradU[i][5] + U[i][2]/Umag*gradU[i][8]) * U[i][2]/Umag 
        #(Ux/Umag*xx + Uy/Umag*yx + Uz/Umag*zx) * Ux/Umag
        #(Ux/Umag*xy + Uy/Umag*yy + Uz/Umag*zy) * Uy/Umag
        #(Ux/Umag*xz + Uy/Umag*yz + Uz/Umag*zz) * Uz/Umag
        N4 = (N1 + N2 + N3)**2
        grad['normal'][i] = (2*N4)**(1/2)
        
        #determine shear stress
        dusdys1 = (U[i][0]/Umag*gradU[i][0] + U[i][1]/Umag*gradU[i][3] + U[i][2]/Umag*gradU[i][6]) * (U[i][1]-U[i][2])/Unull             
        dusdys2 = (U[i][0]/Umag*gradU[i][1] + U[i][1]/Umag*gradU[i][4] + U[i][2]/Umag*gradU[i][7]) * (U[i][2]-U[i][0])/Unull             
        dusdys3 = (U[i][0]/Umag*gradU[i][2] + U[i][1]/Umag*gradU[i][5] + U[i][2]/Umag*gradU[i][8]) * (U[i][0]-U[i][1])/Unull             
        #dusdys1 = (Ux/Umag*xx + Uy/Umag*yx + Uz/Umag*zx) *(Uy - Uz)/Unull
        #dusdys2 = (Ux/Umag*xy + Uy/Umag*yy + Uz/Umag*zy) *(Uz - Ux)/Unull
        #dusdys3 = (Ux/Umag*xz + Uy/Umag*yz + Uz/Umag*zz) *(Ux - Uy)/Unull
        
        dvsdxs1 = ((U[i][1] - U[i][2])/Unull*gradU[i][0] + (U[i][2] - U[i][0])/Unull*gradU[i][3] + (U[i][0] - U[i][1])/Unull*gradU[i][6])*U[i][0]/Umag 
        dvsdxs2 = ((U[i][1] - U[i][2])/Unull*gradU[i][1] + (U[i][2] - U[i][0])/Unull*gradU[i][4] + (U[i][0] - U[i][1])/Unull*gradU[i][7])*U[i][1]/Umag 
        dvsdxs3 = ((U[i][1] - U[i][2])/Unull*gradU[i][2] + (U[i][2] - U[i][0])/Unull*gradU[i][5] + (U[i][0] - U[i][1])/Unull*gradU[i][8])*U[i][2]/Umag 
        #dvsdxs1 = ((Uy - Uz)/Unull*xx + (Uz - Ux)/Unull*yx + (Ux - Uy)/Unull*zx)*Ux/Umag
        #dvsdxs2 = ((Uy - Uz)/Unull*xy + (Uz - Ux)/Unull*yy + (Ux - Uy)/Unull*zy)*Uy/Umag
        #dvsdxs3 = ((Uy - Uz)/Unull*xz + (Uz - Ux)/Unull*yz + (Ux - Uy)/Unull*zz)*Uz/Umag
        
        dusdzs1 = (U[i][0]/Umag*gradU[i][0] + U[i][1]/Umag*gradU[i][3] + U[i][2]/Umag*gradU[i][6]) * (U[i][1]*(U[i][0] - U[i][1])/Umag/Unull - U[i][2]*(U[i][2]-U[i][0])/Umag/Unull) 
        dusdzs2 = (U[i][0]/Umag*gradU[i][1] + U[i][1]/Umag*gradU[i][4] + U[i][2]/Umag*gradU[i][7]) * (U[i][2]*(U[i][1] - U[i][2])/Umag/Unull - U[i][0]*(U[i][0]-U[i][1])/Umag/Unull) 
        dusdzs3 = (U[i][0]/Umag*gradU[i][2] + U[i][1]/Umag*gradU[i][5] + U[i][2]/Umag*gradU[i][8]) * (U[i][0]*(U[i][2] - U[i][0])/Umag/Unull - U[i][1]*(U[i][1]-U[i][2])/Umag/Unull) 
        #dusdzs1 = (Ux/Umag*xx + Uy/Umag*yx + Uz/Umag*zx) * (Uy*(Ux - Uy)/Umag/Unull - Uz*(Uz-Ux)/Umag/Unull)
        #dusdzs2 = (Ux/Umag*xy + Uy/Umag*yy + Uz/Umag*zy) * (Uz*(Uy - Uz)/Umag/Unull - Ux*(Ux-Uy)/Umag/Unull)
        #dusdzs3 = (Ux/Umag*xz + Uy/Umag*yz + Uz/Umag*zz) * (Ux*(Uz - Ux)/Umag/Unull - Uy*(Uy-Uz)/Umag/Unull)
        
        dwsdxs11 = ((U[i][0] - U[i][1])*U[i][1]/Umag/Unull - (U[i][2] - U[i][0])*U[i][2]/Umag/Unull)*gradU[i][0]
        dwsdxs12 = ((U[i][1] - U[i][2])*U[i][2]/Umag/Unull - (U[i][0] - U[i][1])*U[i][0]/Umag/Unull)*gradU[i][3]
        dwsdxs13 = ((U[i][2] - U[i][0])*U[i][0]/Umag/Unull - (U[i][1] - U[i][2])*U[i][1]/Umag/Unull)*gradU[i][6]
        # dwsdxs11 = ((Ux - Uy)*Uy/Umag/Unull - (Uz - Ux)*Uz/Umag/Unull)*xx
        # dwsdxs12 = ((Uy - Uz)*Uz/Umag/Unull - (Ux - Uy)*Ux/Umag/Unull)*yx            
        # dwsdxs13 = ((Uz - Ux)*Ux/Umag/Unull - (Uy - Uz)*Uy/Umag/Unull)*zx
        dwsdxs1g = (dwsdxs11 + dwsdxs12 + dwsdxs13)*U[i][0]/Umag;
        
        dwsdxs21 = ((U[i][0] - U[i][1])*U[i][1]/Umag/Unull - (U[i][2] - U[i][0])*U[i][2]/Umag/Unull)*gradU[i][1]
        dwsdxs22 = ((U[i][1] - U[i][2])*U[i][2]/Umag/Unull - (U[i][0] - U[i][1])*U[i][0]/Umag/Unull)*gradU[i][4]
        dwsdxs23 = ((U[i][2] - U[i][0])*U[i][0]/Umag/Unull - (U[i][1] - U[i][2])*U[i][1]/Umag/Unull)*gradU[i][7]
        # dwsdxs21 = ((Ux - Uy)*Uy/Umag/Unull - (Uz - Ux)*Uz/Umag/Unull)*xy
        # dwsdxs22 = ((Uy - Uz)*Uz/Umag/Unull - (Ux - Uy)*Ux/Umag/Unull)*yy
        # dwsdxs23 = ((Uz - Ux)*Ux/Umag/Unull - (Uy - Uz)*Uy/Umag/Unull)*zy
        dwsdxs2g = (dwsdxs21 + dwsdxs22 + dwsdxs23)*U[i][1]/Umag;
        
        dwsdxs31 = ((U[i][0] - U[i][1])*U[i][1]/Umag/Unull - (U[i][2] - U[i][0])*U[i][2]/Umag/Unull)*gradU[i][2]
        dwsdxs32 = ((U[i][1] - U[i][2])*U[i][2]/Umag/Unull - (U[i][0] - U[i][1])*U[i][0]/Umag/Unull)*gradU[i][5]
        dwsdxs33 = ((U[i][2] - U[i][0])*U[i][0]/Umag/Unull - (U[i][1] - U[i][2])*U[i][1]/Umag/Unull)*gradU[i][8]
        # dwsdxs31 = ((Ux - Uy)*Uy/Umag/Unull - (Uz - Ux)*Uz/Umag/Unull)*xz
        # dwsdxs32 = ((Uy - Uz)*Uz/Umag/Unull - (Ux - Uy)*Ux/Umag/Unull)*yz
        # dwsdxs33 = ((Uz - Ux)*Ux/Umag/Unull - (Uy - Uz)*Uy/Umag/Unull)*zz
        dwsdxs3g = (dwsdxs31 + dwsdxs32 + dwsdxs33)*U[i][2]/Umag;
        TermS1 = (dusdys1 + dusdys2 + dusdys3 + dvsdxs1 + dvsdxs2 + dvsdxs3)**2
        TermS2 = (dusdzs1 + dusdzs2 + dusdzs3 + dwsdxs1g + dwsdxs2g + dwsdxs3g)**2
        grad['shear'][i]=(TermS1 + TermS2)**(1/2)
        
        c+= 1
        
        if c == len(U)//100:
                pb += 1
                sys.stdout.write('\r')
                sys.stdout.write("[%-100s] %d%%" % ('='*pb, pb))
                sys.stdout.flush()
                c = 0
                
    # print(grad.head(5))
    # print(U)
    # print(gradU)
    # print(latest_time)
    return grad['normal'].values.tolist(), grad['shear'].values.tolist()

def write_kolmogorov(list_of_data,tail):
    head=f"""/*--------------------------------*- C++ -*----------------------------------*\\
  =========                 |
  \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
   \\    /   O peration     | Website:  https://openfoam.org
    \\  /    A nd           | Version:  8
     \\/     M anipulation  |
\*---------------------------------------------------------------------------*/
FoamFile
{{
    version     2.0;
    format      ascii;
    class       volScalarField;
    location    {get_latesttime()};
    object      kolmogorov;
}}
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


def write_normalstress(list_of_data,tail):
    head=f"""/*--------------------------------*- C++ -*----------------------------------*\\
  =========                 |
  \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
   \\    /   O peration     | Website:  https://openfoam.org
    \\  /    A nd           | Version:  8
     \\/     M anipulation  |
\*---------------------------------------------------------------------------*/
FoamFile
{{
    version     2.0;
    format      ascii;
    class       volScalarField;
    location    {get_latesttime()};
    object      normalstress;
}}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

dimensions      [1 -1 -2 0 0 0 0];

internalField   nonuniform List<scalar>""" 
    middle = f"""\n{len(list_of_data)}
(
"""
    try:
        with open(f'{get_latesttime()}/normalstress','w') as file:
            file.write(head)
            file.write(middle)
            for element in list_of_data:
                file.write(str(element)+'\n')
            file.write(tail)
            file.close()
    except:
        with open(f'{get_latesttime()}\\normalstress','w') as file:
            file.write(head)
            file.write(middle)
            for element in list_of_data:
                file.write(str(element)+'\n')
            file.write(tail)
            file.close()       
    return

def write_shearstress(list_of_data,tail):
    head=f"""/*--------------------------------*- C++ -*----------------------------------*\\
  =========                 |
  \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
   \\    /   O peration     | Website:  https://openfoam.org
    \\  /    A nd           | Version:  8
     \\/     M anipulation  |
\*---------------------------------------------------------------------------*/
FoamFile
{{
    version     2.0;
    format      ascii;
    class       volScalarField;
    location    {get_latesttime()};
    object      shearstress;
}}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

dimensions      [1 -1 -2 0 0 0 0];

internalField   nonuniform List<scalar>""" 
    middle = f"""\n{len(list_of_data)}
(
"""
    try:
        with open(f'{get_latesttime()}/shearstress','w') as file:
            file.write(head)
            file.write(middle)
            for element in list_of_data:
                file.write(str(element)+'\n')
            file.write(tail)
            file.close()
    except:
        with open(f'{get_latesttime()}\\shearstress','w') as file:
            file.write(head)
            file.write(middle)
            for element in list_of_data:
                file.write(str(element)+'\n')
            file.write(tail)
            file.close()       
    return

def write_all_zones(kolmogorov, normalstresses, shearstresses, tail):
    """
    All DangerZones are based on the values given by the individual parameters,
    they are treaded as sorted lists where least dangerous values greated with 
    number 1 and more risky values are grated numbers up to 3 which imply high 
    risk. 
    For the individual analized parameters the following is true:
        kolmogorov length scale --> the smaller the value the higher the risk
        normalstress            --> the higher the value the higher the risk
        shearstress             --> the higher the value the higher the risk
    """
    head0=f"""/*--------------------------------*- C++ -*----------------------------------*\\
  =========                 |
  \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
   \\    /   O peration     | Website:  https://openfoam.org
    \\  /    A nd           | Version:  8
     \\/     M anipulation  |
\*---------------------------------------------------------------------------*/
FoamFile
{{
    version     2.0;
    format      ascii;
    class       volScalarField;
    location    {get_latesttime()};
    object      DangerZonesCombined;
}}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

dimensions      [0 0 0 0 0 0 0];

internalField   nonuniform List<scalar>""" 

    head1=f"""/*--------------------------------*- C++ -*----------------------------------*\\
  =========                 |
  \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
   \\    /   O peration     | Website:  https://openfoam.org
    \\  /    A nd           | Version:  8
     \\/     M anipulation  |
\*---------------------------------------------------------------------------*/
FoamFile
{{
    version     2.0;
    format      ascii;
    class       volScalarField;
    location    {get_latesttime()};
    object      DangerZonesKolmogorov;
}}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

dimensions      [0 0 0 0 0 0 0];

internalField   nonuniform List<scalar>""" 

    head2=f"""/*--------------------------------*- C++ -*----------------------------------*\\
  =========                 |
  \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
   \\    /   O peration     | Website:  https://openfoam.org
    \\  /    A nd           | Version:  8
     \\/     M anipulation  |
\*---------------------------------------------------------------------------*/
FoamFile
{{
    version     2.0;
    format      ascii;
    class       volScalarField;
    location    {get_latesttime()};
    object      DangerZonesNormalstress;
}}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

dimensions      [0 0 0 0 0 0 0];

internalField   nonuniform List<scalar>""" 

    head3=f"""/*--------------------------------*- C++ -*----------------------------------*\\
  =========                 |
  \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
   \\    /   O peration     | Website:  https://openfoam.org
    \\  /    A nd           | Version:  8
     \\/     M anipulation  |
\*---------------------------------------------------------------------------*/
FoamFile
{{
    version     2.0;
    format      ascii;
    class       volScalarField;
    location    {get_latesttime()};
    object      DangerZonesShearstress;
}}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

dimensions      [0 0 0 0 0 0 0];

internalField   nonuniform List<scalar>""" 

    middle = f"""\n{len(kolmogorov)}
(
"""

    #get length of data
    len_data = len(kolmogorov)
    #determine stepsze for zones
    step = len_data//3 
    
    #kolmogorov zones
    kolZones = []
    
    zone1 = sorted(kolmogorov,reverse=True)[step] 
    zone2 = sorted(kolmogorov,reverse=True)[2*step]
    
    for i in kolmogorov:
        if i <= zone1:
            kolZones.append(1)
        elif i <= zone2:
            kolZones.append(2)
        else:
            kolZones.append(3)
    
    #normalstress zones
    normZones = []
    
    zone1 = sorted(normalstresses)[step] 
    zone2 = sorted(normalstresses)[2*step]
    
    for i in normalstresses:
        if i <= zone1:
            normZones.append(1)
        elif i <= zone2:
            normZones.append(2)
        else:
            normZones.append(3)
    
    #shearstress zones
    shearZones = []
    
    zone1 = sorted(shearstresses)[step] 
    zone2 = sorted(shearstresses)[2*step]
    
    for i in normalstresses:
        if i <= zone1:
            shearZones.append(1)
        elif i <= zone2:
            shearZones.append(2)
        else:
            shearZones.append(3)
    
    #combined zones
    combinedZones = []
    #summantion of all zones divided by 3
    for i in range(len_data):
        combinedZones.append((kolZones[i]+normZones[i]+shearZones[i])/3)
        
    #Writing the files
    
    #combinedZones
    try:
        with open(f'{get_latesttime()}/DangerZonesCombined','w') as file:
            file.write(head0)
            file.write(middle)
            for element in combinedZones:
                    file.write(str(element)+'\n')
            file.write(tail)
            file.close()
    except:
        with open(f'{get_latesttime()}\\DangerZonesCombined','w') as file:
            file.write(head0)
            file.write(middle)
            for element in combinedZones:
                    file.write(str(element)+'\n')
            file.write(tail)
            file.close()
            
    #kolmogorovZones
    try:
        with open(f'{get_latesttime()}/DangerZonesKolmogorov','w') as file:
            file.write(head1)
            file.write(middle)
            for element in kolZones:
                    file.write(str(element)+'\n')
            file.write(tail)
            file.close()
    except:
        with open(f'{get_latesttime()}\\DangerZonesKolmogorov','w') as file:
            file.write(head1)
            file.write(middle)
            for element in kolZones:
                    file.write(str(element)+'\n')
            file.write(tail)
            file.close()    
    
    #normalstressZones
    try:
        with open(f'{get_latesttime()}/DangerZonesNormalstress','w') as file:
            file.write(head2)
            file.write(middle)
            for element in normZones:
                    file.write(str(element)+'\n')
            file.write(tail)
            file.close()
    except:
        with open(f'{get_latesttime()}\\DangerZonesNormalstress','w') as file:
            file.write(head2)
            file.write(middle)
            for element in normZones:
                    file.write(str(element)+'\n')
            file.write(tail)
            file.close()
            
    #shearstressZones
    try:
        with open(f'{get_latesttime()}/DangerZonesShearstress','w') as file:
            file.write(head3)
            file.write(middle)
            for element in shearZones:
                    file.write(str(element)+'\n')
            file.write(tail)
            file.close()
    except:
        with open(f'{get_latesttime()}\\DangerZonesShearstress','w') as file:
            file.write(head3)
            file.write(middle)
            for element in shearZones:
                    file.write(str(element)+'\n')
            file.write(tail)
            file.close()  
    
    return


# def write_zones(list_of_data, tail, cell_diameter=1.5e-5):
#     """
#     The higher the zone number more critical is the situatlion for the cells
#     0 is equal to 110% of the cells diameter and should not affect the cells
#     1 is equal to 105% of the cells diameter and might affect them
#     2 is equal to less then 105% of the cells diameter effects are certain
#     """
#     head=f"""/*--------------------------------*- C++ -*----------------------------------*\\
#   =========                 |
#   \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
#    \\    /   O peration     | Website:  https://openfoam.org
#     \\  /    A nd           | Version:  8
#      \\/     M anipulation  |
# \*---------------------------------------------------------------------------*/
# FoamFile
# {{
#     version     2.0;
#     format      ascii;
#     class       volScalarField;
#     location    {get_latesttime()};
#     object      DangerZones;
# }}
# // * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

# dimensions      [0 0 0 0 0 0 0];

# internalField   nonuniform List<scalar>""" 
#     middle = f"""\n{len(list_of_data)}
# (
# """
#     try:
#         with open(f'{get_latesttime()}/dangerzones','w') as file:
#             file.write(head)
#             file.write(middle)
#             for element in list_of_data:
#                 if element >= cell_diameter*1.1:                                    #if modifications are needed ajust here 
#                     file.write(str(1)+'\n')
#                 elif element > cell_diameter*1.05 and element < cell_diameter*1.1:  #if modifications are needed ajust here
#                     file.write(str(2)+'\n')
#                 else:
#                     file.write(str(3)+'\n')
#             file.write(tail)
#             file.close()
#     except:
#         with open(f'{get_latesttime()}\\dangerzones','w') as file:
#             file.write(head)
#             file.write(middle)
#             for element in list_of_data:
#                 if element >= cell_diameter*1.1:                                    #if modifications are needed ajust here 
#                     file.write(str(1)+'\n')
#                 elif element > cell_diameter*1.05 and element < cell_diameter*1.1:  #if modifications are needed ajust here
#                     file.write(str(2)+'\n')
#                 else:
#                     file.write(str(3)+'\n')
#             file.write(tail)
#             file.close()
#     return


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
    kolmogorov = calculate_local_kolmogorov(epsilons, unit = 'm')
    print('\nWriting local_kolmogorov_lengthscale file')
    write_kolmogorov(kolmogorov, tail)
    
    #calculating normal- and shearstress
    normal, shear = calculate_stresses()
    print('\n\nWriting local normalstress')
    write_normalstress(normal,tail)
    print('\nWriting local shearstress')
    write_shearstress(shear,tail)
    
    
    print('\nWriting dangerzones files')
    write_all_zones(kolmogorov,normal,shear,tail)
    # write_zones(kolmorov, tail)
    
