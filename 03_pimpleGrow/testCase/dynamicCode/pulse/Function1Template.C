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

\*---------------------------------------------------------------------------*/

#include "Function1Template.H"

// * * * * * * * * * * * * * * Static Data Members * * * * * * * * * * * * * //

namespace Foam
{
namespace Function1s
{
    defineTypeNameAndDebug(pulseFunction1vector, 0);
}
    Function1<vector>::adddictionaryConstructorToTable<Function1s::
        pulseFunction1vector>
        pulseFunction1vectorConstructorToTable_;
}


// * * * * * * * * * * * * * * * Global Functions  * * * * * * * * * * * * * //

extern "C"
{
    // dynamicCode:
    // SHA1 = 836c01257f56160729021142ea45930e4c6506e1
    //
    // Unique function name that can be checked if the correct library version
    // has been loaded
    void pulse_836c01257f56160729021142ea45930e4c6506e1(bool load)
    {
        if (load)
        {
            // code that can be explicitly executed after loading
        }
        else
        {
            // code that can be explicitly executed before unloading
        }
    }
}


// * * * * * * * * * * * * * * * * Constructors  * * * * * * * * * * * * * * //

Foam::Function1s::pulseFunction1vector::
pulseFunction1vector
(
    const word& entryName,
    const dictionary& dict
)
:
    FieldFunction1<vector, pulseFunction1vector>
    (
        entryName
    )
{
    if (false)
    {
        Info<< "Construct pulse sha1: 836c01257f56160729021142ea45930e4c6506e1 from dictionary\n";
    }
}


Foam::Function1s::pulseFunction1vector::
pulseFunction1vector
(
    const pulseFunction1vector& f1
)
:
    FieldFunction1<vector, pulseFunction1vector>
    (
        f1
    )
{
    if (false)
    {
        Info<< "Construct pulse sha1: 836c01257f56160729021142ea45930e4c6506e1 as copy\n";
    }
}


// * * * * * * * * * * * * * * * * Destructor  * * * * * * * * * * * * * * * //

Foam::Function1s::pulseFunction1vector::
~pulseFunction1vector()
{
    if (false)
    {
        Info<< "Destroy pulse sha1: 836c01257f56160729021142ea45930e4c6506e1\n";
    }
}


// * * * * * * * * * * * * * * * Member Functions  * * * * * * * * * * * * * //

Foam::vector
Foam::Function1s::pulseFunction1vector::integrate
(
    const scalar x1,
    const scalar x2
) const
{
    NotImplemented;
    return pTraits<vector>::zero;
}


void Foam::Function1s::pulseFunction1vector::writeData
(
    Ostream& os
) const
{
    NotImplemented;
}


// ************************************************************************* i/

