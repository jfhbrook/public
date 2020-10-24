#! /usr/bin/env python
"""The problem is still acting odd, so I'm testing the Jacobian
using the "close" test problem parameters and an abbreviated points set."""


import sfbe
from numpy import *

points=array([[-9.72, 8.81],
[-11.08, 3.85],
[-8.91, -2.76],
[-3.43, 8.96],
[-1.13, 15.91],
[-9.67, 8.35]]
)

startingpt=array([16.0,8.0,17.0,19.0,pi*(15.0/180.0),0.75,0.3,-3.0,-5.0])

thetas=(pi/180.0)*array([-179.82,-140.05,-60.08,19.70,100.27,179.64])

"The initial Jacobian for the \"close\" test problem with an abbreviated points set:"
print sfbe.jacobian(startingpt,-1,thetas)
