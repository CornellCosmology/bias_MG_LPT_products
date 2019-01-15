# Bias_MG_LPT_products

This repository contains codes for the calculation of the real-space correlation function 
and power spectrum for biased tracers in MG models using Convolution Lagrangian Perturbation Theory (CLPT). 

The codes are the MG versions of the ones originally presented in https://github.com/martinjameswhite/CLEFT_GSM , for 
calculating the various ingredients of the Gaussian Streaming Model (GSM) using EFT corrections to CLPT.
Note, however, that the MG version presented here Only implements CLPT for biased tracers using local-in-density Lagrangian bias.
The Kernels and subroutines that refer to tidal bias terms, EFT corrections and the GSM and exist as part of the original code, have NOT
been adapted for MG. 

The configuration space CLPT 2-point correlation function \xi(r) is calculated by the C++ module.
For each calculation, the user needs to provide 3 files: the MG linear power spectrum for the particular cosmology, as well as
the necessary k-dependent Q_n(k) and R_n(k) functions in MG, that the code reads in the subroutine setupQR of lsm.cpp. 
The functions Q_n(k) and R_n(k) are calculated as part of the python module in ps_python3 (see the separate Readme in that directory for how to run the python version).

The current version calculates \xi for the Fr6 MG model at z=0.5, as an example. 
The Q_n(k) and R_n(k) functions are provided in files plin_Fr6z05wmap9_cleftQ.txt
and plin_Fr6z05wmap9_cleftR.txt, that are read by the subroutine setupQR of lsm.cpp.
The MG linear power spectrum for this model and z is given at file plin_Fr6z05wmap9.txt.

After compiling with 'make', the code can be run from the terminal with the command

./lesm plin_Fr6z05wmap9.txt

Subroutine printXiStuff in lsm.cpp prints the contributions to \xi(r) that are relevant to our discussion.

The linear power spectra for the rest of the MG models in the paper are also provided.

