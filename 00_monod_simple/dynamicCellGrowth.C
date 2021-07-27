/*----------------------------------------------------*\
 * Copy from other files
\*--------------------------------*/

#include "fvCFD.H"
// here more needs to be added most likely

int main(int argc, char *argv[])
{
	// used variables in code below
	int i; 		// for for loop
	int x0;		// initial cell concentration
	float muemax; 	// muemax
	Info << "Testing something with cells. " << endl;
	// here some caluclaiton will now happen
	// useing just some testing numbers
	x0 = 500; // choose some values for now
	muemax = 1.05;	// choose some values for now
	Info << "xt was choosen as:  " << x0 << nl << endl;
	Info << "muemax was choosen as: " << muemax << nl << endl;

	for (i = 0; i < 100; i++)
	{
		Info << "Time = " << i << nl << endl;
		Info << "Cells = " << x0*muemax*i << nl << endl; // wrong procedure to calculate values check more examples
	}
}
