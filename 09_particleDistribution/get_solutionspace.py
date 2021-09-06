"""
Get Solution Space form file
"""

def get_solutiuonspace(filename):
    """
    Generate Solutionspace from a Eulerian/Lagrangian File and 
    corresponding local data this solutionspace is a cube not jet
    looking like the actual mesh      
    """
    #opencorisponding file
    rawdata = open(filename,'r')
    
    #setup for variables   
    varS = []
    
    #get all variables 
    for line in rawdata:
        l = line.replace('\n','').split('\t')
        for i in range(0,len(l)):
            varS.append(l[i])
        break
    
    for var in varS:
        variables = {key:[] for key in varS}
        
    for line in rawdata:
        line = line.replace('\n','').split('\t')
        i = 0
        for key in variables:            
            variables[key].append(line[i])
            i += 1
            
    rawdata.close()
    #returning solutionspace and coresponding variables
    return [(min(variables['x']), 
             max(variables['x'])), 
            (min(variables['y']), 
             max(variables['y'])), 
            (min(variables['z']), 
             max(variables['z']))], variables