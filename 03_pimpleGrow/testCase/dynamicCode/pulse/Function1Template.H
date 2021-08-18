/*---------------------------------------------------------------------------*  =========                 |
  \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
   \\    /   O peration     | Website:  https://openfoam.org
    \\  /    A nd           | Copyright (C) YEAR OpenFOAM Foundation
     \\/     M anipulation  |
-------------------------------------------------------------------------------
License
    This file is part of OpenFOAM.

    OpenFOAM is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    OpenFOAM is distributed in the hope that it will be useful, but WITHOUT
    ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
    FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
    for more details.

    You should have received a copy of the GNU General Public License
    along with OpenFOAM.  If not, see <http://www.gnu.org/licenses/>.

Description
    Template for use with dynamic code generation of a Function1.

    - without state

SourceFiles
    Function1Template.C

\*---------------------------------------------------------------------------*/

#ifndef Function1Template_H
#define Function1Template_H

#include "Function1.H"

//{{{ begin codeInclude
#line 32 "/home/lukas/000_MA/checkCase/pitzDailyPulse/0/U/boundaryField/inlet"
#include "mathematicalConstants.H"
//}}} end codeInclude

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

namespace Foam
{
namespace Function1s
{

/*---------------------------------------------------------------------------*                           A templated Function1
\*---------------------------------------------------------------------------*/

class pulseFunction1vector
:
    public FieldFunction1<vector, pulseFunction1vector>
{

public:

    // Runtime type information
    TypeName("pulse");


    // Constructors

        //- Construct from entry name and dictionary
        pulseFunction1vector
        (
            const word& entryName,
            const dictionary& dict
        );

        //- Copy constructor
        pulseFunction1vector
        (
            const pulseFunction1vector& f1
        );

        //- Construct and return a clone
        virtual tmp<Function1<vector>> clone() const
        {
            return tmp<Function1<vector>>
            (
                new pulseFunction1vector(*this)
            );
        }


    //- Destructor
    virtual ~pulseFunction1vector();


    // Member Functions

        //- Return constant value
        inline virtual vector value(const scalar x) const
        {
//{{{ begin code
    #line 37 "/home/lukas/000_MA/checkCase/pitzDailyPulse/0/U/boundaryField/inlet"
return vector
            (
                0.5*(1 - cos(constant::mathematical::twoPi*min(x/0.3, 1))),
                0,
                0
            );
//}}} end code
        }

        //- Integrate between two values
        virtual vector integrate
        (
            const scalar x1,
            const scalar x2
        ) const;

        //- Write in dictionary format
        virtual void writeData(Ostream& os) const;


    // Member Operators

        //- Disallow default bitwise assignment
        void operator=(const pulseFunction1vector&) = delete;
};


// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

} // End namespace Function1s
} // End namespace Foam

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

#endif

// ************************************************************************* //

