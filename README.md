### General Information
---  
This repo is used to show the process to develop functions for OpenFOAM and how these functions need to be structured to archive working applications to enchance your CFD simulations.

### Basics
To generate new applications and functions in OpenFOAM the structure of the sepcific files has to be stored as shown in the image below.\n <img src="https://cdn.cfd.direct/docs/user-guide-v7/img/user253x.png" >
### First example 
The first example (**00_monod_simple**) is used to show how the basic monod calculation with a fixed value for muemax and an inital cell density can be applied and how the amount of cells would be calculated using C syntax.

### Second example
The second example (**01_monod_save_data**) shows how data is accessed from dictionary files and how the data can be stored in other files by creating a "postProcessing" directory where the calculated cell values per time step are stored in a file called "CellGrowth.csv"


