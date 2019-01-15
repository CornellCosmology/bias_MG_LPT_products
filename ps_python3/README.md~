# Power spectrum code

This repository contains a python code for the calculation of the real-space 
power spectrum for biased tracers in MG models using Convolution Lagrangian Perturbation Theory (CLPT). 

The code is the MG version of the one originally presented in https://github.com/martinjameswhite/CLEFT_GSM , for 
calculating the various ingredients of the Gaussian Streaming Model (GSM) using EFT corrections to CLPT.
Note, however, that the MG version presented here Only implements CLPT for biased tracers using local-in-density Lagrangian bias.
The Kernels and subroutines that refer to tidal bias terms, EFT corrections and the GSM and exist as part of the original code, have NOT
been adapted for MG. 

The subroutine kernelspool needs to read tabulated values for the various growth factor configurations that
are necessary for the CLPT calculation in MG. These are:
D1(k), D2(p,-k), D2(p, k-p) and D3_sym(k,-p,p), as explained in the paper.
Files with the growth factors for the the various models and cosmological times studied in the
paper are provided in Dgrowthdata/. Furthermore, Mathematica notebooks for the calculation of these growth factors
are provided in the folder Mathematica/. Kernelspool uses these growthfactors to calculate
the various functions Q_n(k) and R_n(k) in MG and then the CLPT power spectrum.
Also, the subset of these k-functions that should be read by the C++ module should be saved by the code.

The current version calculates the various temrs in the CLPT P(k) for the Fr6 MG model at z=0.5, as an example. 
The MG linear power spectrum for this model and z is given at file plin_Fr6z05wmap9.txt.

The code can be run (for this example) using the command:

python3 main.py --pfile plin_Fr6z05wmap9.txt --npool [number of cores] --outfile PCLPT_Fr6z05wmap9.txt --saveq True --saver True --saveqfunc True

The command saves the CLPT P(k) at plin_Fr6z05wmap9.txt and the necessary Q_n(k) and R_n(k) (not all of them) for C++
in the files plin_Fr6z05wmap9_cleftQ.txt and plin_Fr6z05wmap9_cleftR.txt.

The above can be adjusted accordingly, in conjunction with changing the MG growth factors in kernelspool, for any desired MG model and z

The linear power spectra and growth factors for the rest of the MG models in the paper are also provided.



