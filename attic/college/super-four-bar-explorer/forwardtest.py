#! /usr/bin/env python

#This is used to make sure that the forward equations are correct.
#I compared the results with those from sfbe_plotter.gnumeric and
#sfbe_plotter.xls and worked until they were the same.
#I found that all three had bugs, and I believe I found all of them.

import sfbe
from numpy import *


print "A:", sfbe.A(16.0,8.0,19.0,15.0*(pi/180.0),pi/2.0)
print "B:", sfbe.B(16.0,8.0,19.0,15.0*(pi/180.0),pi/2.0)
print "C:", sfbe.C(16.0,8.0,17.0,19.0,15.0*(pi/180.0),pi/2.0)
print "t4:", sfbe.t4(16.0,8.0,17.0,19.0,15.0*(pi/180.0),-1,pi/2.0)
print "Px:", sfbe.Px(16.0,8.0,17.0,19.0,15.0*(pi/180.0),-3.0,-1,pi/2.0)
print "Py:", sfbe.Py(16.0,8.0,17.0,19.0,15.0*(pi/180.0),-5.0,-1,pi/2.0)
print "Qx:", sfbe.Qx(8.0,-3.0,pi/2.0)
print "Qy:", sfbe.Qy(8.0,-5.0,pi/2.0)

print "Sx:", sfbe.Sx(16.0,8.0,17.0,19.0,pi*(15.0/180.0),0.75,0.3,-3.0,-5.0,-1,pi/2.0)
print "Sy:", sfbe.Sy(16.0,8.0,17.0,19.0,pi*(15.0/180.0),0.75,0.3,-3.0,-5.0,-1,pi/2.0)

