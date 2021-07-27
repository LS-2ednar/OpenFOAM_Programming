# Note this REPO is in the making and will take some time until it is finished.
### General Information
***  
This repo is used to show the process to develop functions for OpenFOAM and how these functions need to be structured to archive working applications to enchance your CFD simulations. First very briefly the appliaction directory structure and important files which have to be defined are explained. Then it is explained how the applcations are compiled and how certain dependencies can be removed again. Finally an example is shown, that explains the developement of a new application for OpenFOAM in different complexity levels increasing with the example number. 

### Basics
***
To generate new applications and functions in OpenFOAM the structure of the sepcific files has to be stored as shown in the image below: <br> <p align="center"><img src="https://cdn.cfd.direct/docs/user-guide-v7/img/user253x.png" alt = "From OpenFOAM Programmer's Guide" > </p> <br> As indicated there are several files which are important for the final working Application. New application show a *Placeholder*.C source file, which it the file that is to be compiled. This file has the code which later is run after compilation. The *Placeholder*.H files are used to check for errors, since these files represent headers of classes which later are used in the code. The subdirectory Make has two files the *files* file and the *options* file. The *files* file is a list of the files which are generated in the end aswell as the name of the source file and the the name of the later executable command. The *options* file contains the full directory paths to locate header files. To compile an application one can run the *wmake* command to compile everything. This step is especially usefull ince hit might show potential errors which are found during compilation. In case that the application should be removed, one can run the *wclean* command.

### Code Examples
***
The preseneted codes try to show some different level of monod kinetics. The examples (00 to **XY**) work with the imaginary concept of constant growth, no limitations and no negative effects of anymetabolites. Therefore one can say that the amount of Cells (<a href="https://www.codecogs.com/eqnedit.php?latex=N_t" target="_blank"><img src="https://latex.codecogs.com/gif.latex?N_t" title="N_t" /></a>) after a time *t* is only dependent on the maximal growth rate initial number of Cells (<a href="https://www.codecogs.com/eqnedit.php?latex=N_0" target="_blank"><img src="https://latex.codecogs.com/gif.latex?N_0" title="N_0" /></a>), the maximal specific growth rate (<a href="https://www.codecogs.com/eqnedit.php?latex=\mu_{max}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\mu_{max}" title="\mu_{max}" /></a>) and, time (*t*). Which can be described as follows:
<p align="center"> <a href="https://www.codecogs.com/eqnedit.php?latex=N_t&space;=&space;N_0\cdot&space;e^{\mu_{max}\cdot&space;t}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?N_t&space;=&space;N_0\cdot&space;e^{\mu_{max}\cdot&space;t}" title="N_t = N_0\cdot e^{\mu_{max}\cdot t}" /></a> </p>

### First example 
The first example (**00_monod_simple**) is used to show how the basic monod calculation with a fixed value for muemax and an inital cell density can be applied and how the amount of cells would be calculated using C syntax.

### Second example
The second example (**01_monod_save_data**) shows how data is accessed from dictionary files and how the data can be stored in other files by creating a "postProcessing" directory where the calculated cell values per time step are stored in a file called "CellGrowth.csv"


