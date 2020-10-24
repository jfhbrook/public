#! /usr/bin/env python
"""This is a script that runs sfbe through some benchmarks."""

import sfbe
from numpy import *

"""The "close" problem, where I choose a starting point that I know is
already near the solution.

It seems to work."""

points=array([[-9.72, 8.81],
[-10.69, 6.03],
[-11.08, 3.85],
[-10.94, 1.01],
[-10.41, -0.28],
[-9.83, -1.61],
[-8.91, -2.76],
[-8.06, -2.45],
[-6.46, 0.08],
[-6.02, 3.82],
[-3.43, 8.96],
[0.35, 13.59],
[1.27, 15.61],
[0.41, 16.54],
[-1.13, 15.91],
[-3.31, 14.99],
[-5.84, 13.63],
[-8.12, 11.05],
[-9.67, 8.35]]
)

startingpt=array([16.0,8.0,17.0,19.0,pi*(15.0/180.0),0.75,0.3,-3.0,-5.0])

thetas=(pi/180.0)*array([-179.82,-160.16,-140.05,-119.44,-99.54,-80.05,-60.08,-40.12,-20.62,0.10,19.70,39.79,59.93,79.60,100.27,119.48,140.49,159.74,179.64])

(vnew,sigma,tnew)=sfbe.linkagefit(points,startingpt,thetas)
print "The output of sfbe.linkagefit for the \"close\" problem is:\n"
print "r_1: ", vnew[0]
print "r_2: ", vnew[1]
print "r_3: ", vnew[2]
print "r_4: ", vnew[3]
print "t_1: ", vnew[4]
print "h_x: ", vnew[5]
print "h_y: ", vnew[6]
print "O_x: ", vnew[7]
print "O_y: ", vnew[8]

oldr=sfbe.residuals(points[:,0],points[:,1],startingpt,-1,thetas)
newr=sfbe.residuals(points[:,0],points[:,1],vnew,-1,tnew)

print "\nThe sum of the squares of the original residuals was: ", dot(oldr,oldr)
print "\nThe sum of the squares of the new residuals is: ", dot(newr,newr)



"""A modification of the base problem, where I changed a the parameters around a little.
It converged nicely enough."""
    
startingpt=array([18.0,7.0,17.0,18.0,15.0*(pi/180),0.5,0.5,0.0,0.0])

(vnew,sigma,tnew)=sfbe.linkagefit(points,startingpt,thetas)
print "\nThe output of sfbe.linkagefit for a mid-range starting point is:\n"
print "r_1: ", vnew[0]
print "r_2: ", vnew[1]
print "r_3: ", vnew[2]
print "r_4: ", vnew[3]
print "t_1: ", vnew[4]
print "h_x: ", vnew[5]
print "h_y: ", vnew[6]
print "O_x: ", vnew[7]
print "O_y: ", vnew[8]

oldr=sfbe.residuals(points[:,0],points[:,1],startingpt,-1,thetas)
newr=sfbe.residuals(points[:,0],points[:,1],vnew,-1,tnew)

print "\nThe sum of the squares of the original residuals was: ", dot(oldr,oldr)
print "\nThe sum of the squares of the new residuals is: ", dot(newr,newr)




"""An attempted example at application of this technique.
It converges beautifully."""


startingpt=array([16.0,8.0,17.0,15.0,-10.0*(pi/180),0.5,0.3,0.0,-3.0])

points=array([[0.0,0.0],[2.0,2.0],[4.0,4.0],[6.0,6.0],[8.0,8.0],[10.0,10.0]])

thetas=(pi/180.0)*array([-60.0,-45.0,-30.0,-15.0,0.0,15.0])

(vnew,sigma,tnew)=sfbe.linkagefit(points,startingpt,thetas)
print "\nThe output of sfbe.linkagefit for the plausible application problem is:\n"
print "r_1: ", vnew[0]
print "r_2: ", vnew[1]
print "r_3: ", vnew[2]
print "r_4: ", vnew[3]
print "t_1: ", vnew[4]
print "h_x: ", vnew[5]
print "h_y: ", vnew[6]
print "O_x: ", vnew[7]
print "O_y: ", vnew[8]

oldr=sfbe.residuals(points[:,0],points[:,1],startingpt,-1,thetas)
newr=sfbe.residuals(points[:,0],points[:,1],vnew,-1,tnew)

print "\nThe sum of the squares of the original residuals was: ", dot(oldr,oldr)
print "\nThe sum of the squares of the new residuals is: ", dot(newr,newr)





"""A modification of the base problem, where I changed a the parameters around a lot.
It didn't converge."""

startingpt=array([16.0,11.0,16.0,12.0,-5.0*(pi/180),1.2,-0.2,0.0,2.0])

points=array([[-9.72, 8.81],
[-10.69, 6.03],
[-11.08, 3.85],
[-10.94, 1.01],
[-10.41, -0.28],
[-9.83, -1.61],
[-8.91, -2.76],
[-8.06, -2.45],
[-6.46, 0.08],
[-6.02, 3.82],
[-3.43, 8.96],
[0.35, 13.59],
[1.27, 15.61],
[0.41, 16.54],
[-1.13, 15.91],
[-3.31, 14.99],
[-5.84, 13.63],
[-8.12, 11.05],
[-9.67, 8.35]]
)

thetas=(pi/180.0)*array([-179.82,-160.16,-140.05,-119.44,-99.54,-80.05,-60.08,-40.12,-20.62,0.10,19.70,39.79,59.93,79.60,100.27,119.48,140.49,159.74,179.64])

(vnew,sigma,tnew)=sfbe.linkagefit(points,startingpt,thetas)
print "\nThe output of sfbe.linkagefit for a more difficult starting point is:\n"
print "r_1: ", vnew[0]
print "r_2: ", vnew[1]
print "r_3: ", vnew[2]
print "r_4: ", vnew[3]
print "t_1: ", vnew[4]
print "h_x: ", vnew[5]
print "h_y: ", vnew[6]
print "O_x: ", vnew[7]
print "O_y: ", vnew[8]

oldr=sfbe.residuals(points[:,0],points[:,1],startingpt,-1,thetas)
newr=sfbe.residuals(points[:,0],points[:,1],vnew,-1,tnew)

print "\nThe sum of the squares of the original residuals was: ", dot(oldr,oldr)
print "\nThe sum of the squares of the new residuals is: ", dot(newr,newr)