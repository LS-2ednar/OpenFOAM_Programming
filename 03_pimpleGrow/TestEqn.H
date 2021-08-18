// This is a test function just to print a message while the code is runing

double exp(double x);

// creating accessable dictionary for cell number determination
dictionary CellDict;
const word CellDictName("cellProperties");

IOobject CellDictIO
(
CellDictName,
mesh.time().constant(),
mesh,
IOobject::MUST_READ
);

CellDict = IOdictionary(CellDictIO);

float N0;
CellDict.lookup("N0") >> N0;

float S0;
CellDict.lookup("S0") >> S0;

float mue_max;
CellDict.lookup("mue_max") >> mue_max;

float Ks;
CellDict.lookup("Ks") >> Ks;

float Yxs;
CellDict.lookup("Yxs") >> Yxs;

float N;
N = N0;


//Calculating new values for Substrate and Cells
float S = S0-(N*Yxs);

N = N0*exp((S/(S+Ks))*runTime.value());



Info << "Cells and Substrate at time: " << runTime.timeName() << endl;
Info << "Cells: " << N << nl << "Substrate: " << S << endl;

autoPtr<OFstream> outputFilePtr;
outputFilePtr.open(OFstream("postProcessing/growth.csv"), std::ios_base::app);
outputFilePtr() << runTime.value() << "," << N << "," << S << "," << mue_max << endl;


