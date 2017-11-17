import numpy as np
import argparse
import matplotlib.pyplot as plt
from math import log10
import subprocess

fnam="grmonty.spec"

# CGS constants
LSUN = 3.827e33

# Take input arguments
parser = argparse.ArgumentParser(description='Runs grmonty on a grid of the input variables and outputs a set of points and values.')

## Define input variables
parser.add_argument('nph',type=int,help='Number of photons to use.')
parser.add_argument('dumpnam',type=str,help='Dump file location.')
# Accretion rates
parser.add_argument('mdoti',type=float,help='Lower accretion limit (in Medd).')
parser.add_argument('mdotf',type=float,help='Upper accretion limit (in Medd).')
parser.add_argument('nmdot',type=int,help='Amount of points to use (including initial and final).')
# BH masses
parser.add_argument('mi',type=float,help='Lower mass limit (in Msun).')
parser.add_argument('mf',type=float,help='Upper mass limit (in Msun)n.')
parser.add_argument('nm',type=int,help='Amount of points to use (including initial and final).')

# Take input variables
args = parser.parse_args()
nph=args.nph
dumpnam=args.dumpnam
mdoti=args.mdoti
mdotf=args.mdotf
nmdot=args.nmdot
mi=args.mi
mf=args.mf
nm=args.nm

## Hardcoded in grmonty, will change in the near future.
# Observer angles
thetai=0.3
thetaf=100
ntheta=6

# Frequencies
nui=1.2355897e8
nuf=4.98969853e29
nnu=200

#Create vectors for all variables,
mdot=np.logspace(log10(mdoti),log10(mdotf),nmdot)
m=np.logspace(log10(mi),log10(mf),nm)
theta=np.linspace(thetai,thetaf,num=ntheta)
nu=np.logspace(log10(nui),log10(nuf),nnu)

# Logarithm of the vectors for interpolation
logm=map(log10,m)
logmdot=map(log10,mdot)
lognu=map(log10,nu)

# Declare arrays
values=np.empty((nm,nmdot,ntheta,nnu),dtype=float)
points=[logm,logmdot,theta,lognu]

#Call grmonty iteratively and store results.
for i in range(0,nm):
    for j in range(0,nmdot):
        subprocess.call(["./grmonty", repr(nph), dumpnam, repr(mdot[j]), repr(m[i]), repr(1)])
        data=np.loadtxt(fnam)
        DNULNU = (len(data[0])-1)/ntheta
        for k in range(0,ntheta):
            values[i][j][k][:]=data[:,1 + k*DNULNU]*LSUN
            for l in range(0,nnu):
                if values[i][j][k][l]>0:
                    values[i][j][k][l]=log10(values[i][j][k][l])

# Export results
np.save("points",points)
np.save("values",values)