/*----------------------------------------------------*\
 * Copy from other file 00_monod_simple
\*----------------------------------------------------*/
#include "fvCFD.H"
#include <math.h>

int main(int argc, char *argv[])
{
    // Get access to OpenFOAM case
    #include "setRootCase.H"

    // Create the time system and the instance called mesh
    #include "createTime.H"
    #include "createMesh.H"

    //----------------------------------------------------------------
    // LOOK UP THINGS FROM A FILE DICTIONARY AND USING THE STORED DATA 
    //----------------------------------------------------------------	
    
    // Accesssing costum dictionary
    dictionary CellDict;
    const word CellDictName("initialCellProperties");
    
    // Input-Output object which holds the path to the dict and its name 
    IOobject CellDictIO
    (
    CellDictName,		// name of the file
    mesh.time().constant(), 	// path to wehere the file is located
    mesh,			// reference to mesh needed by the constructor
    IOobject::MUST_READ		// reading is required
    );

    // Check for the availability of the dictionary and if it follows the OF format
    if (!CellDictIO.typeHeaderOk<dictionary>(true))
        FatalErrorIn(args.executable()) << "specified dictionary cannot be opend " << CellDictName << exit(FatalError);

    // Dictionary object initialisation
    CellDict = IOdictionary(CellDictIO);

    // Read information form main part of dictionary using standard C++ stringstream syntax
    int CellDensity;
    CellDict.lookup("CellDensity") >> CellDensity;
    
    float MueMax;
    CellDict.lookup("MueMax") >> MueMax;

    // ----------------------------------------------------------------------
    // Accessing controlDict for the variables startTime, endTime and deltaT
    // ----------------------------------------------------------------------
    
    // Accesssing controlDict
    dictionary ContDict;
    const word ContDictName("controlDict");
    
    // Input-Output object which holds the path to the dict and its name 
    IOobject ContDictIO
    (
    ContDictName,		// name of the file
    mesh.time().system(), 	// path to wehere the file is located
    mesh,			// reference to mesh needed by the constructor
    IOobject::MUST_READ		// reading is required
    );

    // Check for the availability of the dictionary and if it follows the OF format
    if (!ContDictIO.typeHeaderOk<dictionary>(true))
        FatalErrorIn(args.executable()) << "specified dictionary cannot be opend " << ContDictName << exit(FatalError);

    // Dictionary object initialisation
    ContDict = IOdictionary(ContDictIO);

    // Read information form main part of dictionary using standard C++ stringstream syntax
    float startTime;
    ContDict.lookup("startTime") >> startTime;
    
    float endTime;
    ContDict.lookup("endTime") >> endTime;

    float deltaT;
    ContDict.lookup("deltaT") >> deltaT;

    // used variables for CellDensity Calculation
    double exp(double x);	// initializing the exponential function

    // -------------------------------------------------------
    // GENERATING AN OUTPUTFILE AND FOLDER TO WORK WITH LATER
    // -------------------------------------------------------
    
    // Creating custom directory and wirte output file
    fileName outputDir = mesh.time().path()/"postProcessing";
    mkDir(outputDir);

    // Outputfile Pointer
    autoPtr<OFstream> outputFilePtr;
    
    // Openfile in new created directory
    outputFilePtr.reset(new OFstream(outputDir/"CellGrowth.csv"));

    //Write header to file
    outputFilePtr() << "Time,Cells" << endl;
    
    // Calculation of Cell values and adding time and CellDensity to outputfile
    for (float i = startTime; i < endTime+deltaT ; i = i+deltaT)
    {
        //Console Outputs
        Info << "Time  = " << i << nl << "Cells = " << round(CellDensity*exp(MueMax*i)) << nl << endl;
        // Appending Values to the new file
        outputFilePtr() << i << "," << round(CellDensity*exp(MueMax*i)) << endl;
    }
    return 0;
}
