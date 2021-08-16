// Solve the Cell amount equation 

fvScalarMatrix NEqn
(
    b*fvm::ddt(N) == -fvm::ddt(S)    
);

NEqn.relax();

solve(NEqn);

