import csv
from libtsl import subset,htparams,sphere
from numpy import array, exp
from matplotlib.pyplot import *
from keas.unit.unit import UnitConverter

#Reads in data points
datareader=csv.reader(open('friday_aluminum_sphere.csv'))
time=[]
temp=[]
datareader.next()
for row in datareader:
    temp=temp+[float(row[2])]
    time=time+[15*len(temp)-1]

#pulls off front crap
istart=temp.index(max(temp))
tempsub=temp[istart:-1]
timesub=time[istart:-1]

#Subsets data points
n=10
timesub=array(subset(timesub,n))
tempsub=array(subset(tempsub,n))

#finds theoretical equation action
#units in 'murican

#unit converter object
c=UnitConverter()

#sphere dimensions
sphdims=sphere(1.95)

sphere=htparams(g=386.22, #thx wiki
                l=sphdims.d,
                xsect=sphdims.xsect,
                sarea=sphdims.sarea,
                vol=sphdims.vol,
                Tinf=float(c.convert('tempF('+str(temp[0])+')','tempR')),
                kvisc=(1.54e-8)*1550.0031, #thx Crowe, et al
                rho=0.0975436884, #lb/in^3
                k=0.0016584693, #thx engineeringtoolbox.com
                cp=0.229, #thx cengel/boles
                emmis=0.26)

Tzero=float(c.convert('tempF('+str(tempsub[0])+')', 'tempR'))
Tfinal=float(c.convert('tempF('+str(tempsub[-1])+')','tempR'))
print 'T0=', Tzero
print 'Tf=', Tfinal
print 'Tinf=', sphere.Tinf

print 'Axs=', sphere.xsect
print 'Sa=', sphere.sarea
print 'V=', sphere.vol

Tfilm=sphere.Tfilm(Tzero,Tfinal)
print 'film temperature=', Tfilm

sphere.thermexp=1.0/Tfilm #approximation for ideal gasses, thx wiki

print 'thermal expansion=', sphere.thermexp

h=sphere.hc(Tzero,Tfinal) + sphere.hr(Tzero)
print 'h=', h

beta=(h*sphere.sarea)/(sphere.rho*sphere.vol*sphere.cp)

print '1/Tau=', beta

theory=(tempsub[0]-temp[0])*exp(-beta*(timesub-timesub[0])) + temp[0]
print theory

#plot some shizz
#plot(timesub,tempsub, 'ko')
plot(timesub,theory, 'k-')
#axis([0, time[-1],80, 400] )
#show()
