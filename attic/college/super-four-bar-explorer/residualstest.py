#! /usr/bin/env python
"""
residuals() wasn't working so I worked on this part separately.
At this point in time, it at least create output that makes sense
at a glance, but I haven't checked it to make sure it's actually
doing what I expect it to.
"""


from numpy import *
import sfbe
    
#These vectors are the size that I want them, dammit.
x=array([1.0,2.0,3.0,4.0,5.0,4.0,3.0,2.0,1.0,0.0])
y=array([1.0,2.0,3.0,4.0,5.0,4.0,3.0,2.0,1.0,0.0])
v=array([16.0,8.0,17.0,19.0,pi*(15.0/180.0),0.75,0.3,-3.0,-5.0])
sig=1
thetas=(pi/180.0)*array([1,2,3,4,5,6,7,8,9,10])

print "Are x, y and thetas the same size? Here are their lengths:"
print x.shape[0]
print y.shape[0]
print thetas.shape[0]
print "Is v nine long?:"
print (v.shape[0]==9)
print "So what's the residual vector?"
arrgh=sfbe.residuals(x,y,v,sig,thetas)
print arrgh
print "How big is arrgh? It should be twice as long as x or y:"
print arrgh.shape[0]