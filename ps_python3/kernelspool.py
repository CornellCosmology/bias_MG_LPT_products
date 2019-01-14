import numpy
import numpy as np
from scipy.interpolate import InterpolatedUnivariateSpline as interpolate
from scipy.integrate import trapz, simps
from itertools import product
import multiprocessing as mp
import qfuncpool as qfn
import math
from scipy.interpolate import RegularGridInterpolator
from scipy.interpolate import interp1d
from scipy.interpolate import Rbf
## Define functions

#define ngrav to differentiate between GR and MG models. 0 for GR, 1 for f(R) MG and 2 for nDGP
ngrav=0

#import growth factor data doe f(R)
#D1growthdata=np.loadtxt("/home/astrosun2/gvalogiannis/bias_MG_LPT/CLEFT_GSM-master/D1growthFr4z05p2000.txt")
#D1growthdata=np.loadtxt("/home/astrosun2/gvalogiannis/bias_MG_LPT/CLEFT_GSM-master/D1growthFr4z05p2000.txt")
#D1growthdata=np.loadtxt("/home/astrosun2/gvalogiannis/bias_MG_LPT/CLEFT_GSM-master/D1growthFr6z05p2000.txt")
D1growthdata=np.loadtxt("/home/astrosun2/gvalogiannis/bias_MG_LPT/CLEFT_GSM-master/D1growthFr5z1planckp2000.txt")
kd1=np.logspace(-6,5,3e3)
d1growth=D1growthdata[:]
#1st order growth factor interpolation
d1_int=interp1d(kd1,d1growth,kind='cubic')
#import growth factor data for nDGP
D1growthdatanDGP=np.loadtxt("/home/astrosun2/gvalogiannis/bias_MG_LPT/CLEFT_GSM-master/D1growthN1wmap9.txt")
#D1growthdatanDGP=np.loadtxt("/home/astrosun2/gvalogiannis/bias_MG_LPT/CLEFT_GSM-master/D1growthN5wmap9.txt")
ad1=D1growthdatanDGP[:,0]
d1growthnDGP=D1growthdatanDGP[:,1]
#1st order growth factor interpolation
d1_nDGP=interp1d(ad1,d1growthnDGP,kind='cubic')
#D2growthdata=np.loadtxt("/home/astrosun2/gvalogiannis/CLEFT_GSM-master/D2growthFr4z0p12010.txt")
#D2growthdata=np.loadtxt("/home/astrosun2/gvalogiannis/bias_MG_LPT/CLEFT_GSM-master/D2growthFr4z05p80809.txt")
#D2growthdata=np.loadtxt("/home/astrosun2/gvalogiannis/bias_MG_LPT/CLEFT_GSM-master/D2growthFr4z05p80809.txt")
D2growthdata=np.loadtxt("/home/astrosun2/gvalogiannis/bias_MG_LPT/CLEFT_GSM-master/D2growthFr5z1planckp80809.txt")
#D2growthdata=np.loadtxt("/home/astrosun2/gvalogiannis/bias_MG_LPT/CLEFT_GSM-master/D2growthFr6z05p80809.txt")
#D2growthdata=np.loadtxt("/home/astrosun2/gvalogiannis/bias_MG_LPT/CLEFT_GSM-master/D2growthN1z05p80809.txt")
#D2growthdata=np.loadtxt("/home/astrosun2/gvalogiannis/bias_MG_LPT/CLEFT_GSM-master/D2growthN5z05p80809.txt")
#D2pkdata=np.loadtxt("/home/astrosun2/gvalogiannis/bias_MG_LPT/CLEFT_GSM-master/D2pkFr4z05p80809.txt")
#D2pkdata=np.loadtxt("/home/astrosun2/gvalogiannis/bias_MG_LPT/CLEFT_GSM-master/D2pkFr6z05p80809.txt")
#D2pkdata=np.loadtxt("/home/astrosun2/gvalogiannis/bias_MG_LPT/CLEFT_GSM-master/D2pkFr6z05noscrp80809.txt")
D2pkdata=np.loadtxt("/home/astrosun2/gvalogiannis/bias_MG_LPT/CLEFT_GSM-master/D2pkFr5z1planckp80809.txt")
#D2pkdata=np.loadtxt("/home/astrosun2/gvalogiannis/bias_MG_LPT/CLEFT_GSM-master/D2pkFr4z05p80809.txt")
#D2pkdata=np.loadtxt("/home/astrosun2/gvalogiannis/bias_MG_LPT/CLEFT_GSM-master/D2pkN1z05p80809.txt")
#D2pkdata=np.loadtxt("/home/astrosun2/gvalogiannis/bias_MG_LPT/CLEFT_GSM-master/D2pkN5z05p80809.txt")
#D3symgrowthdata=np.loadtxt("/home/astrosun2/gvalogiannis/CLEFT_GSM-master/D3symgrowthscreen.txt")
#D3symgrowthdata=np.loadtxt("/home/astrosun2/gvalogiannis/bias_MG_LPT/CLEFT_GSM-master/D3symgrowthFr4z05p80809.txt")
#D3symgrowthdata=np.loadtxt("/home/astrosun2/gvalogiannis/bias_MG_LPT/CLEFT_GSM-master/D3symgrowthN1z00p80809new.txt")
#D3symgrowthdata=np.loadtxt("/home/astrosun2/gvalogiannis/bias_MG_LPT/CLEFT_GSM-master/D3symgrowthFr6z05p80809.txt")
D3symgrowthdata=np.loadtxt("/home/astrosun2/gvalogiannis/bias_MG_LPT/CLEFT_GSM-master/D3symgrowthFr5z1planckp80809.txt")
#D3symgrowthdata=np.loadtxt("/home/astrosun2/gvalogiannis/bias_MG_LPT/CLEFT_GSM-master/D3symgrowthFr4z05p80809.txt")
#D3symgrowthdata=np.loadtxt("/home/astrosun2/gvalogiannis/bias_MG_LPT/CLEFT_GSM-master/D3symgrowthN1z05p80809.txt")
#D3symgrowthdata=np.loadtxt("/home/astrosun2/gvalogiannis/bias_MG_LPT/CLEFT_GSM-master/D3symgrowthN5z05p80809.txt")
D2growth=D2growthdata[:]
D2pk=D2pkdata[:]
D3symgrowth=D3symgrowthdata[:]
#
#trilinear interpolation grid set up
Np=80
Npx=9
k=np.logspace(-3,2,Np)
r=np.logspace(-3,2,Np)
x=np.linspace(-1,1,Npx)
points=(k,r,x)
D2valgrowth=np.zeros((k.shape[0],r.shape[0],x.shape[0]))
D2valpk=np.zeros((k.shape[0],r.shape[0],x.shape[0]))
D3valgrowth=np.zeros((k.shape[0],r.shape[0],x.shape[0]))
for i in range(k.shape[0]):
  for j in range(r.shape[0]):
    for kin in range(x.shape[0]):
       D2valgrowth[i,j,kin]=D2growth[(Np*i+j)*Npx+kin]
       D2valpk[i,j,kin]=D2pk[(Np*i+j)*Npx+kin]
       D3valgrowth[i,j,kin]=D3symgrowth[(Np*i+j)*Npx+kin]
#constructing interpolators for D2&D3 factors
D2growth_interp=RegularGridInterpolator(points, D2valgrowth, method='linear')
D2pk_interp=RegularGridInterpolator(points, D2valpk, method='linear')
D3growth_interp=RegularGridInterpolator(points, D3valgrowth, method='linear')
#Interpolator for 120x120x10 grip points
#Npp=120
#Npxx=10
#kk=np.logspace(-3,2,Npp)
#rr=np.logspace(-3,2,Npp)
#xx=np.linspace(-1,1,Npxx)
#pointsnew=(kk,rr,xx)
#D2valgrowth=np.zeros((kk.shape[0],rr.shape[0],xx.shape[0]))
#for i in range(kk.shape[0]):
#  for j in range(rr.shape[0]):
#    for kin in range(xx.shape[0]):
#       D2valgrowth[i,j,kin]=D2growth[(Npp*i+j)*Npxx+kin]
#constructing interpolators for D2&D3 factors
#D2growth_interp=RegularGridInterpolator(pointsnew, D2valgrowth, method='linear')
#end of George's part

#constants

#Define Q:
def Q1approx(k, r, x):
    return 0.25*(1 + x)**2

def Q1(k, r, x): #Because of MG, promote Q(r,x) to Q(k,r,x), added by George
    y =  1 + r**2 - 2*r*x
    if ngrav==1:
      D2att=np.empty((r.shape[0],x.shape[1]))
      points = np.meshgrid(np.array([k]),r[:,0],x[0,:])
      flat=np.array([m.flatten() for m in points])
      out_array =  D2growth_interp(flat.T)
      D2att = out_array.reshape(*points[0].shape)
      D2att=D2att[:,0,:]
      return (r**2)*((7/3)*D2att/(d1_int(k*r)*d1_int(k*numpy.sqrt(y))))**2
    elif ngrav==2:
      D2att=np.empty((r.shape[0],x.shape[1]))
      points = np.meshgrid(np.array([k]),r[:,0],x[0,:])
      flat=np.array([m.flatten() for m in points])
      out_array =  D2growth_interp(flat.T)
      D2att = out_array.reshape(*points[0].shape)
      D2att=D2att[:,0,:]
      return (r**2)*((7/3)*D2att/(d1_nDGP(0.6667)*d1_nDGP(0.6667)))**2
    else:
      return (r**2 *(1 - x**2)**2)/y**2

def Q2approx(k, r, x):
    return 0.25*x*(1 + x)

def Q2(k, r, x):
    y =  1 + r**2 - 2*r*x
    if ngrav==1:
      D2att=np.empty((r.shape[0],x.shape[1]))
      points = np.meshgrid(np.array([k]),r[:,0],x[0,:])
      flat=np.array([m.flatten() for m in points])
      out_array =  D2growth_interp(flat.T)
      D2att = out_array.reshape(*points[0].shape)
      D2att=D2att[:,0,:]  
      return (r*x*(1 - r*x)/y)*((7/3)*D2att/d1_int(k*r)/d1_int(k*numpy.sqrt(y)))
    elif ngrav==2:
     D2att=np.empty((r.shape[0],x.shape[1]))
     points = np.meshgrid(np.array([k]),r[:,0],x[0,:])
     flat=np.array([m.flatten() for m in points])
     out_array =  D2growth_interp(flat.T)
     D2att = out_array.reshape(*points[0].shape)
     D2att=D2att[:,0,:]
     #print (d1_nDGP(0.999))
     return (r*x*(1 - r*x)/y)*((7/3)*D2att/d1_nDGP(0.6667)/d1_nDGP(0.6667))
    else:
      return ((1- x**2)*r*x*(1 - r*x))/y**2

def Q3approx(k, r, x):
    return 0.25*x**2

def Q3(k, r, x):
    y =  1 + r**2 - 2*r*x
    return (x**2 *(1 - r*x)**2)/y**2

def Q5approx(k, r, x):
    y =  1 + r**2 - 2*r*x
    return x*(1 + x)/2.

def Q5(k, r, x):
    y =  1 + r**2 - 2*r*x
    if ngrav==1:
      D2att=np.empty((r.shape[0],x.shape[1]))
      points = np.meshgrid(np.array([k]),r[:,0],x[0,:])
      flat=np.array([m.flatten() for m in points])
      out_array =  D2growth_interp(flat.T)
      D2att = out_array.reshape(*points[0].shape)
      D2att=D2att[:,0,:]  
      return (r*x)*((7/3)*D2att/d1_int(k*r)/d1_int(k*numpy.sqrt(1 + r**2 - 2*r*x)))
    elif ngrav==2:
     D2att=np.empty((r.shape[0],x.shape[1]))
     points = np.meshgrid(np.array([k]),r[:,0],x[0,:])
     flat=np.array([m.flatten() for m in points])
     out_array =  D2growth_interp(flat.T)
     D2att = out_array.reshape(*points[0].shape)
     D2att=D2att[:,0,:]
     return (r*x)*((7/3)*D2att/d1_nDGP(0.6667)/d1_nDGP(0.6667))
    else:
      return r*x*(1 - x**2.)/y

def Q8approx(k, r, x):
    y =  1 + r**2 - 2*r*x
    return (1 + x)/2.

def Q8(k, r, x):
    y =  1 + r**2 - 2*r*x
    if ngrav==1:
      D2att=np.empty((r.shape[0],x.shape[1]))
      points = np.meshgrid(np.array([k]),r[:,0],x[0,:])
      flat=np.array([m.flatten() for m in points])
      out_array =  D2growth_interp(flat.T)
      D2att = out_array.reshape(*points[0].shape)
      D2att=D2att[:,0,:]  
      return (r**2)*((7/3)*D2att/d1_int(k*r)/d1_int(k*numpy.sqrt(1 + r**2 - 2*r*x)))
    elif ngrav==2:
     D2att=np.empty((r.shape[0],x.shape[1]))
     points = np.meshgrid(np.array([k]),r[:,0],x[0,:])
     flat=np.array([m.flatten() for m in points])
     out_array =  D2growth_interp(flat.T)
     D2att = out_array.reshape(*points[0].shape)
     D2att=D2att[:,0,:]
     return (r**2)*((7/3)*D2att/d1_nDGP(0.6667)/d1_nDGP(0.6667))
    else:
      return r**2.*(1 - x**2.)/y

def Qs2approx(k, r, x):
    y =  1 + r**2 - 2*r*x
    return (1 + x)*(1- 3*x)/4.

def Qs2(k, r, x):
    y =  1 + r**2 - 2*r*x
    return r**2.*(x**2 - 1.)*(1 - 2*r**2 + 4*r*x - 3*x**2)/y**2
#Extra SPT functions added by George

def QI(k, r, x):
    y =  1 + r**2 - 2*r*x
    if ngrav==1:
      D2att=np.empty((r.shape[0],x.shape[1]))
      points = np.meshgrid(np.array([k]),r[:,0],x[0,:])
      flat=np.array([m.flatten() for m in points])
      out_array =  D2growth_interp(flat.T)
      D2att = out_array.reshape(*points[0].shape)
      D2att=D2att[:,0,:]  
      return (r**2)*(1-x*x)*((7/3)*D2att/d1_int(k*r)/d1_int(k*numpy.sqrt(1 + r**2 - 2*r*x)))
    elif ngrav==2:
      D2att=np.empty((r.shape[0],x.shape[1]))
      points = np.meshgrid(np.array([k]),r[:,0],x[0,:])
      flat=np.array([m.flatten() for m in points])
      out_array =  D2growth_interp(flat.T)
      D2att = out_array.reshape(*points[0].shape)
      D2att=D2att[:,0,:]
      return (r**2)*(1-x*x)*((7/3)*D2att/d1_nDGP(0.6667)/d1_nDGP(0.6667))
    else:
      return (r**2 *(1 - x**2)**2)/y**2   

def Q7approx(k, r, x):
    y =  1 + r**2 - 2*r*x
    return (x**2 *(1 - r*x))/y

def Q7(k, r, x):
    y =  1 + r**2 - 2*r*x
    return (x**2 *(1 - r*x))/y

def Q9approx(k, r, x):
    y =  1 + r**2 - 2*r*x
    return (r*x*(1 - r*x))/y

def Q9(k, r, x):
    y =  1 + r**2 - 2*r*x
    return (r*x*(1 - r*x))/y

def Q11approx(k, r, x):
    y =  1 + r**2 - 2*r*x
    return x*x

def Q11(k, r, x):
    y =  1 + r**2 - 2*r*x
    return x*x

def Q12approx(k, r, x):
    y =  1 + r**2 - 2*r*x
    return r*x

def Q12(k, r, x):
    y =  1 + r**2 - 2*r*x
    return r*x

def Q13approx(k, r, x):
    y =  1 + r**2 - 2*r*x
    return r*r

def Q13(k, r, x):
    y =  1 + r**2 - 2*r*x
    return r*r

dictQapprox = {1:Q1approx, 2:Q2approx, 3:Q3approx, 5:Q5approx, 8:Q8approx, -1:Qs2approx, 7:Q7approx, 9:Q9approx, 11:Q11approx, 12:Q12approx, 13:Q13approx}
dictQ = {1:Q1, 2:Q2, 3:Q3, 5:Q5, 8: Q8, -1:Qs2, 20:QI, 7:Q7, 9:Q9, 11:Q11, 12:Q12, 13:Q13}
#dictQapprox = {1:Q1approx, 2:Q2approx, 3:Q3approx, 5:Q5approx, 8:Q8approx, -1:Qs2approx}
#dictQ = {1:Q1, 2:Q2, 3:Q3, 5:Q5, 8: Q8, -1:Qs2}


#####Define double integral here
def Q_internal(k, n, r, approx = False):
    if approx:
        func = lambda r, x: ilpk(k*numpy.sqrt(1 + r**2 - 2*r*x))*dictQapprox[n](k, r, x)
    else:
        func = lambda r, x: ilpk(k*numpy.sqrt(1 + r**2 - 2*r*x))*dictQ[n](k, r, x)
    return (glwval*func(r, glxval)).sum(axis = -1)



def Q_external(n, k):
    fac = k**3 /(2*numpy.pi)**2
    #r = (kint/k)
    #print (k)
    r=numpy.logspace(-3, 2, 1e3)
    kint=k*r
    pkint = ilpk(kint)
    #tempmax= (numpy.min(r))
    #if tempmax < 1e-6:
    #  print (tempmax)
    absr1 = abs(r-1)
    mask = absr1 < tol
    y = numpy.zeros_like(r)
    #print ((r[~mask].reshape(-1, 1)).shape)
    y[~mask]  = Q_internal(k, n, r[~mask].reshape(-1, 1))
    if mask.sum():
        y[mask] = Q_internal(k, n,  r[mask].reshape(-1, 1), approx = True)
    y *= pkint
    return fac*trapz(y, r)


def Q(kv, pk, npool = 4, ns = None, kintv = None):

    global ilpk, tol, kint, pkint, glxval, glwval

    ilpk = pk
    #print (kv)
    if kintv is None:
        kint = numpy.logspace(-3, 2, 1e3)
        #kint = numpy.logspace(-6, 3, 1e3)
        #r=numpy.logspace(numpy.log10(1e-3),numpy.log10(1e2),1e3)
        #kint = r*kv
    else:
        kint = kintv
    pkint = ilpk(kint)

    tol = 10**-5. 
    glxval, glwval = numpy.loadtxt("gl_128.txt", unpack = True)
    #print (glxval)
    glxval = glxval.reshape(1, -1)
    glwval = glwval.reshape(1, -1)
    #print (glxval.shape)
    if ns is None:
        ns = [1, 2, 3, 5, 8, -1, 20, 7, 9, 11, 12, 13]
        #ns = [1, 2, 3, 5, 8, -1]

    pool = mp.Pool(npool)
    prod = product(ns, kv)
    #print (list(prod))
    Qv = pool.starmap(Q_external, list(prod))
    pool.close()
    pool.join()
    Qv = numpy.array(Qv).reshape(len(ns), -1)
    toret = numpy.zeros([Qv.shape[0] + 1, Qv.shape[1]])
    toret[0] = kv
    toret[1:, :] = Qv

    del ilpk, tol, kint, pkint, glxval, glwval

    return toret

###############################################################


def R1approx(k, r, x):
    return 0.5*(1- x)*(1 + x)**2

def R1(k, r, x):
    y =  1 + r**2 - 2*r*x
    if ngrav==1:
      D3att=np.empty((r.shape[0],x.shape[1]))
      points = np.meshgrid(np.array([k]),r[:,0],x[0,:])
      flat=np.array([m.flatten() for m in points])
      out_array =  D3growth_interp(flat.T)
      D3att = out_array.reshape(*points[0].shape)
      D3att=D3att[:,0,:]
      #print ((r**2).shape)  
      #return ((d1_int(k*r)*d1_int(k))/0.76/0.76)**(-2)*(21/10)*(r**2)*(D3att/d1_int(k)/(d1_int(k*r)**2))
      #return ((d1_int(k*r)*d1_int(k*numpy.sqrt(k))/0.76/0.76)**-1)*(21/10)*(r**2)*(D3att/d1_int(k)/(d1_int(k*r)**2))
      return (21/10)*(r**2)*(D3att/(d1_int(k)*(d1_int(k*r)**2)))
      #return (r**2 *(1 - x**2)**2)/y
    elif ngrav==2:
     D3att=np.empty((r.shape[0],x.shape[1]))
     points = np.meshgrid(np.array([k]),r[:,0],x[0,:])
     flat=np.array([m.flatten() for m in points])
     out_array =  D3growth_interp(flat.T)
     D3att = out_array.reshape(*points[0].shape)
     D3att=D3att[:,0,:]
     #print((r**2 *(1 - x**2)**2)/y/((21/10)*(r**2)*(D3att/(d1_nDGP(0.9999)*(d1_nDGP(0.9999)**2)))))
     return (21/10)*(r**2)*(D3att/(d1_nDGP(0.6667)*(d1_nDGP(0.6667)**2)))
    else:
     return (r**2 *(1 - x**2)**2)/y


def R2approx(k, r, x):
    return 0.5*x*(1 + x)*(1-x)

def R2(k, r, x):
    y =  1 + r**2 - 2*r*x
    if ngrav==1:
      D2att=np.empty((r.shape[0],x.shape[1]))
      points = np.meshgrid(np.array([k]),r[:,0],x[0,:])
      flat=np.array([m.flatten() for m in points])
      out_array =  D2pk_interp(flat.T)
      D2att = out_array.reshape(*points[0].shape)
      D2att=D2att[:,0,:]
      #print (D2att.shape)  
      return (r*x*(1 - r*x)/y)*(7/3)*(D2att/d1_int(k)/(d1_int(k*r)))
    elif ngrav==2:
      D2att=np.empty((r.shape[0],x.shape[1]))
      points = np.meshgrid(np.array([k]),r[:,0],x[0,:])
      flat=np.array([m.flatten() for m in points])
      out_array =  D2pk_interp(flat.T)
      D2att = out_array.reshape(*points[0].shape)
      D2att=D2att[:,0,:]
      return (r*x*(1 - r*x)/y)*(7/3)*(D2att/d1_nDGP(0.6667)/(d1_nDGP(0.6667)))
    else:
     return ((1- x**2)*r*x*(1 - r*x))/y

def R3(k, r, x):
    y =  1 + r**2 - 2*r*x
    if ngrav==1:
      D2att=np.empty((r.shape[0],x.shape[1]))
      points = np.meshgrid(np.array([k]),r[:,0],x[0,:])
      flat=np.array([m.flatten() for m in points])
      out_array =  D2pk_interp(flat.T)
      D2att = out_array.reshape(*points[0].shape)
      D2att=D2att[:,0,:]
      #print (D2att.shape)  
      return (r*r*(1 - r*x)/y)*(7/3)*(D2att/d1_int(k)/(d1_int(k*r)))
    elif ngrav==2:
      D2att=np.empty((r.shape[0],x.shape[1]))
      points = np.meshgrid(np.array([k]),r[:,0],x[0,:])
      flat=np.array([m.flatten() for m in points])
      out_array =  D2pk_interp(flat.T)
      D2att = out_array.reshape(*points[0].shape)
      D2att=D2att[:,0,:]
      return (r*r*(1 - r*x)/y)*(7/3)*(D2att/d1_nDGP(0.6667)/(d1_nDGP(0.6667)))
    else:
      return (r*r*(1 - r*x)*(1-x*x)/y)



def R4(k, r, x):
    y =  1 + r**2 - 2*r*x
    if ngrav==1:
      D2att=np.empty((r.shape[0],x.shape[1]))
      points = np.meshgrid(np.array([k]),r[:,0],x[0,:])
      flat=np.array([m.flatten() for m in points])
      out_array =  D2pk_interp(flat.T)
      D2att = out_array.reshape(*points[0].shape)
      D2att=D2att[:,0,:]
      #print (D2att.shape)  
      return (r*r*(1 - x*x)/y)*(7/3)*(D2att/d1_int(k)/(d1_int(k*r)))
    elif ngrav==2:
      D2att=np.empty((r.shape[0],x.shape[1]))
      points = np.meshgrid(np.array([k]),r[:,0],x[0,:])
      flat=np.array([m.flatten() for m in points])
      out_array =  D2pk_interp(flat.T)
      D2att = out_array.reshape(*points[0].shape)
      D2att=D2att[:,0,:]
      return (r*r*(1 - x*x)/y)*(7/3)*(D2att/d1_nDGP(0.6667)/(d1_nDGP(0.6667)))
    else:
      return (r**2 *(1 - x**2)**2)/y


listRapprox = [R1approx, R2approx]
listR = [R1, R2, R3, R4]


#Double integral here

def R_internal(k, n, r, approx = False):
    if ngrav==1:
     func = lambda r, x: listR[n-1](k, r, x)
     return (glwval*func(r, glxval)).sum(axis = -1)        
    else:
     func = lambda r, x: listR[n-1](k, r, x)
     return (glwval*func(r, glxval)).sum(axis = -1)       

def R_external(n, k):

    fac = k**3 /(2*numpy.pi)**2 *ilpk(k)
    #r = (kint/k)
    r=numpy.logspace(-3, 2, 1e3)
    kint=k*r
    pkint = ilpk(kint)
    absr1 = abs(r-1)
    mask = absr1 < tol
    y = numpy.zeros_like(r)
    if ngrav==1:
     y[~mask]  = R_internal(k, n, r[~mask].reshape(-1, 1))
     if mask.sum():
         y[mask] = R_internal(k, n, r[mask].reshape(-1, 1), approx = True)#initially True
    else:
     y[~mask]  = R_internal(k, n, r[~mask].reshape(-1, 1))
     if mask.sum():
         y[mask] = R_internal(k, n, r[mask].reshape(-1, 1), approx = True)
    y *= pkint
    return fac*trapz(y, r)



def R(kv, pk, npool = 4, ns = None, kintv = None):

    global ilpk, tol, kint, pkint, glxval, glwval

    ilpk = pk
    if kintv is None:
        kint = numpy.logspace(-3, 2, 1e3)
        #kint = numpy.logspace(-3, 2, 1e3)
        #r=numpy.logspace(numpy.log10(1e-3),numpy.log10(1e2),1e3)
        #kint = r*kv
    else:
        kint = kintv
    pkint = ilpk(kint)

    tol = 10**-5. 
    glxval, glwval = numpy.loadtxt("gl_128.txt", unpack = True)
    glxval = glxval.reshape(1, -1)
    glwval = glwval.reshape(1, -1)

    if ns is None:
        ns = [1, 2, 3, 4]

    pool = mp.Pool(npool)
    prod = product(ns, kv)
    Rv = pool.starmap(R_external, list(prod))
    pool.close()
    pool.join()
    Rv = numpy.array(Rv).reshape(len(ns), -1)
    toret = numpy.zeros([Rv.shape[0] + 1, Rv.shape[1]])
    toret[0] = kv
    toret[1:, :] = Rv

    del ilpk, tol, kint, pkint, glxval, glwval

    return toret
