/*--------------------------------*- C++ -*----------------------------------*\
| =========                 |                                                 |
| \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |
|  \\    /   O peration     | Version:  dev                                   |
|   \\  /    A nd           | Web:      www.OpenFOAM.com                      |
|    \\/     M anipulation  |                                                 |
\*---------------------------------------------------------------------------*/
// Accessing given and custom files to calculate cell densities and writing the
// output to a csv file.
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

#include "fvCFD.H"
#include <math.h>

int main(int argc, char *argv[])
{
    // Get access to OpenFOAM case
    #include "setRootCase.H"

    // Create the time system and the instance called mesh
    #include "createTime.H"
    #include "createMesh.H"
    
    // including createFileds.H since we work with fields for this case
    
    #include "createFields.H"

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
    float CellDensity;
    CellDict.lookup("CellDensity") >> CellDensity;
    
    float MueMax;
    CellDict.lookup("MueMax") >> MueMax;
    
    float Substrate;
    CellDict.lookup("Substrate") >> Substrate;
    
    float Ks;
    CellDict.lookup("Ks") >> Ks;

    float Yxs;
    CellDict.lookup("Yxs") >> Yxs;
    
    // used variables for CellDensity Calculation
    double exp(double x);	// initializing the exponential function
    
    float mue;
    mue = MueMax*(Substrate/(Substrate+Ks));

    /*Output of the previous values read from the costum dictionary*/
    
    Info << nl <<"Reading Celldata info" << endl;
    Info << nl << "CellDensity:" << CellDensity << nl << "MueMax" << MueMax << endl;
    Info << "Calculated Mue0:" << mue << nl << "Substrate:" << Substrate << endl; 
    Info << "Ks:"<< Ks << nl << "Yxs" << Yxs << endl;

    /*This part is new since here the realation factors from the fvSolution files are read*/
    scalar alpha;
    fvSolution.lookup("alpha") >> alpha;
    scalar pRefCell;
    fvSolution.lookup("pRefCell") >> pRefCell;
    scalar pRefValue;
    fvSolution.lookup("pRefValue") >> pRefValue;
    
    /*Output of the previous values read from the fvSolutin*/
    Info << nl << "Reading field corrections" << endl; 
    Info << nl << "alpha:" << alpha << nl << "pRefCell" << pRefCell << endl;
    Info << "pRefValue" << pRefValue  << endl; 
     
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

    // Write header to file
    outputFilePtr() << "Time,Cells,Substrate" << endl;
    
    // Calculation of Cell values and adding time and CellDensity to outputfile
    while(runTime.loop())
    {
        Info << "Runtime: " << runTime.timeName() << endl;
        
        //definiton of momentum equation
        fvVectorMatrix UEqn
        (
            fvm::div(phi,U) - fvm::laplacian(nu,U) == -fvc::grad(p)
        );
        
        //Solving the defined momentum equation UEqn
        UEqn.solve();

        //Geting A and H matricies as fields
        volScalarField A = UEqn.A();
        volVectorField H = UEqn.H();
        
        //
        volScalarField A_inv = 1.0/A;
        
        surfaceScalarField A_inv_flux = fvc::interpolate(A_inv); 
        
        volVectorField HbyA = A_inv * H;
        

        fvScalarMatrix pEqn
        (
            fvm::laplacian(A_inv_flux,p) == fvc::div(HbyA)
        );

        // Reference Preasure to Equation
        pEqn.setReference(pRefCell,pRefValue);
        
        pEqn.solve();
        p = alpha*p+(1.0-alpha)*p_old;

        U = A_inv*H - A_inv*fvc::grad(p);

        phi = fvc::interpolate(U) & mesh.Sf();
        
        U.correctBoundaryConditions();
        p.correctBoundaryConditions();
        
        p_old = p;

        // BiologicalCell Calucations
        CellDensity = CellDensity*exp(MueMax*runTime.value()); 
        
        Substrate = Substrate-(CellDensity*exp(mue*runTime.value())*Yxs);
       
	//Console Output
        Info << nl <<"Time = " << runTime.timeName() << nl << "Cells = " << CellDensity <<" g/L" << nl <<"Substrate = " << Substrate << nl << endl;

        // Appending Values to csv file
        outputFilePtr() << runTime.timeName() << "," <<  CellDensity << "," << Substrate
<< endl;

    }
    runTime.write();
    Info << nl << "Finished in:" << nl << runTime.elapsedCpuTime() << " s" << endl;
}


/*Things to modify*/
/*Line 125 to end need update so its solves something worth testing :-)*/
