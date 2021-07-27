/*----------------------------------------------------*\
 * Copy from other files
\*--------------------------------*/

#include "fvCFD.H"
#include <math.h>
// here more needs to be added most likely

int main(int argc, char *argv[])
{
	// used variables in code below
	int i; 			// for for loop
	int x0;			// initial cell concentration
	float muemax; 		// muemax
	double exp(double x);	// initializing the exponential function
	Info << "Testing something with cells. " << endl;
	// here some caluclaiton will now happen
	// useing just some testing numbers
	x0 = 500; // choose some values for now
	muemax = 1.05;	// choose some values for now
	Info << "xt was choosen as:  " << x0 << nl << endl;
	Info << "muemax was choosen as: " << muemax << nl << endl;

	for (i = 0; i < 100; i++)
	{
		Info << "Time  = " << i << endl;
		Info << "Cells = " << x0*exp(muemax*i) << nl << endl; // wrong procedure to calculate values check more examples
	}
}
