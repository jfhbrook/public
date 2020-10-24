#! /usr/bin/env python

"""This script is meant to calculate the gradient(s)  necessary for my project
using sympy.  I'll only need it once, since I only have the one problem."""

import sympy
import numpy

var('r1 r2 r3 r4 t1 t2 sig Ox Oy hx hy x y')
#r1,r2,r3,r4 being member lengths
#t1 and t2 being corresponding angles
#sig being the dyad chooser, +/-1
#Ox and Oy being origin coordinates for r1 and r2
#hx and hy being transforms related to the traced path
#x and y being given data points

A=2*r1*r4*cos(t1)-2*r2*r4*cos(t2)
B=2*r1*r4*sin(t1)-2*r2*r4*sin(t2)
C=r1**2+r2**2+r4**2-r3**2-2*r1*r2*(cos(t1)*cos(t2)*sin(t1)*sin(t2))

t4=2*atan((-B+sig*(B**2-C**2+A**2)**0.5)/(C-A))
Px=r1*cos(t1)+r4*cos(t4)+Ox
Py=r1*sin(t1)+r4*sin(t4)+Oy
Qx=r2*cos(t2)+Ox
Qy=r2*sin(t2)+Oy
Sx=(1-hx)*Qx+hx*Px+hy*(Qy-Py)
Sy=(1-hx)*Qy+hx*Py+hy*(Qx-Px)

gradx=Matrix(9,1,[diff(Sx,r1),diff(Sx,r2),diff(Sx,r3),diff(Sx,r4),diff(Sx,t1),diff(Sx,Ox),diff(Sx,Oy),diff(Sx,hx),diff(Sx,hy)])

grady=Matrix(9,1,[diff(Sy,r1),diff(Sy,r2),diff(Sy,r3),diff(Sy,r4),diff(Sy,t1),diff(Sy,Ox),diff(Sy,Oy),diff(Sy,hx),diff(Sy,hy)])

print "Gradient of Sx wrt v:\n"
for expressions in gradx:
    print simplify(expressions), "\n"

print "\nGradient of Sy wrt v:\n"
for expressions in grady:
    print simplify(expressions), "\n"

print "\ndS_x/dt2:\n"
print simplify(diff(Sx,t2))
print "\ndSy/dt2:\n"
print simplify(diff(Sy,t2))

