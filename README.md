# Note this REPO is in the making and will take some time until it is finished.
***
***
### General Information
***  
This repo is used to show the process to develop functions for OpenFOAM and how these functions need to be structured to archive working applications to enchance your CFD simulations. First very briefly the appliaction directory structure and important files which have to be defined are explained. Then it is explained how the applcations are compiled and how certain dependencies can be removed again. Finally an example is shown, that explains the developement of a new application for OpenFOAM in different complexity levels increasing with the example number. 

### Basics
***
To generate new applications and functions in OpenFOAM the structure of the sepcific files has to be stored as shown in the image below: <br> <p align="center"><img src="https://cdn.cfd.direct/docs/user-guide-v7/img/user253x.png" alt = "From OpenFOAM Programmer's Guide" > </p> <br> As indicated there are several files which are important for the final working application. New application show a *Placeholder*.C source file, which it the file that is to be compiled. This file has the code which later is run after compilation. The *Placeholder*.H files are used to check for errors, since these files represent headers of classes which later are used in the code. The subdirectory Make has two files the *files* file and the *options* file. The *files* file is a list of the files which are generated in the end aswell as the name of the source file and the the name of the later executable command. The *options* file contains the full directory paths to locate header files. To compile an application one can run the *wmake* command to compile everything. This step is especially usefull ince hit might show potential errors which are found during compilation. In case that the application should be removed, one can run the *wclean* command.

In general the approach to create a new application for OpenFOAM should be that an allready exisiting application is modified by introducing new .H files and including them in existing solver code (.C files). 

### Code Examples
***
The preseneted codes try to show some different level of monod kinetics. The examples (00 to **XY**) work with the imaginary concept of constant growth, no limitations and no negative effects of anymetabolites. Therefore one can say that the amount of Cells (<a href="https://www.codecogs.com/eqnedit.php?latex=N_t" target="_blank"><img src="https://latex.codecogs.com/gif.latex?N_t" title="N_t" /></a>) after a time *t* is only dependent on the maximal growth rate initial number of Cells (<a href="https://www.codecogs.com/eqnedit.php?latex=N_0" target="_blank"><img src="https://latex.codecogs.com/gif.latex?N_0" title="N_0" /></a>), the maximal specific growth rate (<a href="https://www.codecogs.com/eqnedit.php?latex=\mu_{max}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\mu_{max}" title="\mu_{max}" /></a>) and, time (*t*). Which can be described as follows:
<p align="center"> <a href="https://www.codecogs.com/eqnedit.php?latex=N_t&space;=&space;N_0\cdot&space;e^{\mu_{max}\cdot&space;t}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?N_t&space;=&space;N_0\cdot&space;e^{\mu_{max}\cdot&space;t}" title="N_t = N_0\cdot e^{\mu_{max}\cdot t}" /></a> </p>

The next set of examples (02 & 03) have an specific growthrate based on the amount of availabe substrate. Which leads to the equations:
<p align="center"> <a href="https://www.codecogs.com/eqnedit.php?latex=N_t&space;=&space;N_0\cdot&space;e^{\mu_{t}\cdot&space;t}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?N_t&space;=&space;N_0\cdot&space;e^{\mu_{t}\cdot&space;t}" title="N_t = N_0\cdot e^{\mu_{t}\cdot t}" /></a> </p> Where (<a href="https://www.codecogs.com/eqnedit.php?latex=\mu_{t}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\mu_{t}" title="\mu_{t}" /></a>) is determined via the substrate and the substrate affinity coefficient as shown below:

<p align="center"> <a href="https://www.codecogs.com/eqnedit.php?latex=\mu_t&space;=&space;\mu_{max}&space;\cdot&space;\frac{S}{K_s&space;&plus;&space;S}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\mu_t&space;=&space;\mu_{max}&space;\cdot&space;\frac{S}{K_s&space;&plus;&space;S}" title="\mu_t = \mu_{max} \cdot \frac{S}{K_s + S}" /></a> </p>


### First example 
The first example (**00_monod_simple**) is used to show how the basic monod calculation with a fixed value for muemax and an inital cell density can be applied and how the amount of cells would be calculated using C syntax.

### Second example
The second example (**01_monod_save_data**) shows how data is accessed from dictionary files and how to work with runTime. Further, it is show how data can be stored in other files by creating a "postProcessing" directory where the calculated cell values per time step are stored in a file called "CellGrowth.csv" 

### Third example
The Cell Growth is determined prior to an the calculation of of the flowfield (using simpleFoam) followed by the custom function also the concept of a substrate is introduced and an changing value for the specific growthrate is implemented. 

### Forth example 
Here the pimple algorithm is modified to work with specific values which are added to an "cellProperties" dictionary and calculate the value of cells and substrate after every iteration. To archive this the pimpleFoam solver application is copyied then the .C file is renamed and adjusted in the Make/files file. Then an additional TestEqn.H is introduced where the calculation of cells and substrate is done. Note that at this stage the calculated values are not reflecting the acctual values. This is due to the way the function is updated every timestep. Further, the outputfile no just shows the last calculated value which needs some more modifications.

### Fifth example
Here the "particleFoam" solver is used to first simulate the different particles in a given test case. Then an additional step is taken and the postprocessing technique "particleTracks" which needs an additional constant/particleTrackProperties file are used to generate a VTK file.

### Sixth example
Here the DPMFoam solver was used and then the particleTracks method was applied. Then a python script was introduced which allows the reorganization of the vtk file in a way, that the individual particle tracks are saved at the same spot.
<p align="center"> <img src="https://github.com/LS-2ednar/OpenFOAM_Programming/blob/main/05_DPMFoam_ParticleTrack/ExamplePlot.png" width=300 align=center> </p>

### Seventh example (Not jet workign)
This case will combine the MPPIC solver with the "particleTracks" utility to save the ParticleTracks in runtime and therefore have more tracking points. After inspecting the source code it is clear, that the MPPICFoam is based on the code of the the DPMFoam however in the MPPICFoam code another cloud headerfile is used "basicKinematicMPPICCloud.H" which means that the DPMFoam is the code that needs to be modified. To trick "wmake" the "DPMFoam.C" is directly modified and used for hte new solver Code to include other dependent files later in the code which are linked with a OpenFOAM specific function. Therfore only in the Make/files file the resulting appications name is changed but the sourceFile is still DPMFoam.C.




***
***
## Sources
This Repo is based on the ideas shown here [UnnamedMoose BasicOpenFOAMProgrammingTutorials](https://github.com/UnnamedMoose/BasicOpenFOAMProgrammingTutorials)

---
### TO DO
Try to fuse some of the particletracking methods (particleFoam, MPPICFoam) with the particleTracks method to get a vtk file and link the function with the pythonscript provided in case 04

It seems that the Tracking of particles is harder in OpenFOAM v8 but as of july 2021 OpenFOAM v9 seems the show improvement in several quite important locations. [Link](https://openfoam.org/version/9/)
