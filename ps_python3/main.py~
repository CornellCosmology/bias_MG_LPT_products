import numpy as np
import cleftpool as cpool
import argparse

import math
from scipy.interpolate import RegularGridInterpolator
from scipy.interpolate import interp1d
from scipy.interpolate import Rbf
import matplotlib.pyplot as plt

def parse_arguments():
   parser = argparse.ArgumentParser()
   parser.add_argument('--pfile', required=True, help='Input power spectrum in order - k, p')
   parser.add_argument('--qfile', default = None, help='File with table of Q functions in order - k, Q1, Q2, Q3, Q5, Q8, Qs2')
   parser.add_argument('--rfile', default = None, help='File with table of R functions in order - k, R1, R2')
   parser.add_argument('--npool', default = 32, type = int, help ="Number of processors")
   parser.add_argument('--nk', default = 150, type = int, help ="Number of k-values to estimate power spectrum at")
   parser.add_argument('--z', default = 0., type = float, help ="Redshift")
   parser.add_argument('--kmin', default = 1e-3, type = float, help ="minimum k")
   parser.add_argument('--kmax', default = 0.40, type = float, help ="maximum k")
   parser.add_argument('--M', default = 0.281, type = float, help ="Matter density")
   parser.add_argument('--outfile', default = 'pk', help ="output file")
   parser.add_argument('--saveq', default = False, type = bool, help ="Save Q kernels; saved in the directory of input spectrum")
   parser.add_argument('--saver', default = False, type = bool, help ="Save R kernels; saved in the directory of input spectrum")
   parser.add_argument('--saveqfunc', default = False, type = bool, help ="Save intermediate q-functions created; saved in the directory of input spectrum")
   args = parser.parse_args()

   return args


############
if __name__=="__main__":
    
   args = parse_arguments()

   if args.pfile == None:
      print('Need an input power spectrum')

   else:

      #In no output file name is given, create from input file
      if args.outfile == 'pk':
         s = args.pfile
         fmtpos = s.rfind('.')
         outfile = s[:fmtpos] + '_cleftpk' + s[fmtpos:]
         print('Spectrum will be saved at \n%s'%outfile)
         if args.saveq:
            #qfile = s[:fmtpos] + '_cleftQnew_z%03d'%(args.z*100) + s[fmtpos:]
            qfile = s[:fmtpos] + '_cleftQ'+ s[fmtpos:]
         if args.saver:
            #rfile = s[:fmtpos] + '_cleftRnew_z%03d'%(args.z*100) + s[fmtpos:]
            rfile = s[:fmtpos] + '_cleftR'+ s[fmtpos:]
         if args.saveqfunc:
            #qfuncfile = s[:fmtpos] + '_cleftqfuncnew_z%03d'%(args.z*100) + s[fmtpos:]
            qfuncfile = s[:fmtpos] + '_cleftqfunc'+ s[fmtpos:]
         else:
            qfuncfile = None
      else:
         s = args.pfile
         fmtpos = s.rfind('.')
         print('Spectrum will be saved at \n%s'%args.outfile)
         if args.saveq:
            #qfile = s[:fmtpos] + '_cleftQnew_z%03d'%(args.z*100) + s[fmtpos:]
            qfile = s[:fmtpos] + '_cleftQ'+ s[fmtpos:]
         if args.saver:
            #rfile = s[:fmtpos] + '_cleftRnew_z%03d'%(args.z*100) + s[fmtpos:]
            rfile = s[:fmtpos] + '_cleftR'+ s[fmtpos:]
         if args.saveqfunc:
            #qfuncfile = s[:fmtpos] + '_cleftqfuncnew_z%03d'%(args.z*100) + s[fmtpos:]
            qfuncfile = s[:fmtpos] + '_cleftqfunc'+ s[fmtpos:]
         else:
            qfuncfile = None  
      #Create kernels
      cl = cpool.CLEFT(pfile = args.pfile, npool = args.npool, qfile = args.qfile, rfile = args.rfile, saveqfile=qfuncfile);
      ##Save them

      if args.saveq:
         #np.savetxt(qfile, np.array([cl.qf.kq, cl.qf.Q1, cl.qf.Q2, cl.qf.Q3, cl.qf.Q5, cl.qf.Q8, cl.qf.Qs2, cl.qf.QI, cl.qf.Q7, cl.qf.Q9, cl.qf.Q11, cl.qf.Q12, cl.qf.Q13]).T, fmt='%0.4e')

         #header = 'k[h/Mpc]   Q1   Q2    Q3    Q5    Q8     Qs2    QI\n'
         np.savetxt(qfile, np.array([cl.qf.kq, cl.qf.Q1, cl.qf.Q2, cl.qf.Q3, cl.qf.Q5, cl.qf.Q8, cl.qf.Qs2, cl.qf.QI]).T, fmt='%0.4e')
      if args.saver:
         np.savetxt(rfile, np.array([cl.qf.kr, cl.qf.R1, cl.qf.R2, cl.qf.R3, cl.qf.R4]).T, fmt='%0.4e')
         #np.savetxt(rfile, np.array([cl.qf.kr, cl.qf.R1, cl.qf.R2]).T, fmt='%0.4e')
         #header = 'k[h/Mpc]   R1   R2 \n'
         #np.savetxt(rfile, np.array([cl.qf.kr, cl.qf.R1, cl.qf.R2]).T, fmt='%0.4e', header=header)

      #Calculate spectrum
      pk = cpool.make_table(cl, nk = args.nk, kmin = args.kmin, kmax = args.kmax, npool = args.npool, z = args.z, M = args.M)

      ##Save it
      if args.outfile == 'pk':
        header = "k[h/Mpc]   P_Zel   P_A    P_W    P_d    P_dd     P_d^2    P_d^2d^2  P_dd^2\n"
        #header = "k[h/Mpc]   P_Zel   P_A    P_W    P_d    P_dd     P_d^2    P_d^2d^2  P_dd^2    P_s^2    P_ds^2    P_d^2s^2   P_s^2s^2   P_D2d     P_dD2d\n"
        np.savetxt(outfile, pk, fmt='%0.4e', header=header)
      else:
        header = "k[h/Mpc]   P_Zel   P_A    P_W    P_d    P_dd     P_d^2    P_d^2d^2  P_dd^2\n"
        #header = "k[h/Mpc]   P_Zel   P_A    P_W    P_d    P_dd     P_d^2    P_d^2d^2  P_dd^2    P_s^2    P_ds^2    P_d^2s^2   P_s^2s^2   P_D2d     P_dD2d\n"
        np.savetxt(args.outfile, pk, fmt='%0.4e', header=header)        


      
