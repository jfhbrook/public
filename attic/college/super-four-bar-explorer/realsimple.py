#! /usr/bin/env python
"""
This is meant to generate the residual vector and the Jacobian
for an extremely simple case, so that I may prove to myself
that it is working properly.

They seem to be, and this is tragic.
"""


from numpy import *
from scipy import derivative
import sfbe
    
#These vectors are the size that I want them, dammit.
x=array([3.0])
y=array([3.0])
v=array([1.0,2.0,1.0,2.0,0.0,1.0,1.0,1.0,1.0])
sig=-1
thetas=array([pi/2])

print "Basic length tests:"
print "Are x, y and thetas the same size? Here are their lengths:"
print x.shape[0]
print y.shape[0]
print thetas.shape[0]
print "Is v nine long?:"
print (v.shape[0]==9)

r1=v[0]
r2=v[1]
r3=v[2]
r4=v[3]
t1=v[4]
hx=v[5]
hy=v[6]
Ox=v[7]
Oy=v[8]
t2=thetas[0]

print "\nLet's make sure the forward equations are working..."
print "Sx:", sfbe.Sx(r1,r2,r3,r4,t1,hx,hy,Ox,Oy,sig,t2)
print "Sy:", sfbe.Sy(r1,r2,r3,r4,t1,hx,hy,Ox,Oy,sig,t2)

print "\nSome numerical derivatives we're surely gonna need..."
print "Fuck doing them by hand! I *know* the forward equations are right!\n"

print "the gradient bits for Sx:"
print "1:",derivative(lambda a: sfbe.Sx(a,r2,r3,r4,t1,hx,hy,Ox,Oy,sig,t2),r1,0.01*abs(r1))
print "2:",derivative(lambda a: sfbe.Sx(r1,a,r3,r4,t1,hx,hy,Ox,Oy,sig,t2),r2,0.01*abs(r2))
print "3:",derivative(lambda a: sfbe.Sx(r1,r2,a,r4,t1,hx,hy,Ox,Oy,sig,t2),r3,0.01*abs(r3))
print "4:",derivative(lambda a: sfbe.Sx(r1,r2,r3,a,t1,hx,hy,Ox,Oy,sig,t2),r4,0.01*abs(r4))
print "5:",derivative(lambda a: sfbe.Sx(r1,r2,r3,r4,a,hx,hy,Ox,Oy,sig,t2),t1,0.02)
print "6:",derivative(lambda a: sfbe.Sx(r1,r2,r3,r4,t1,a,hy,Ox,Oy,sig,t2),hx,0.01*abs(hx))
print "7:",derivative(lambda a: sfbe.Sx(r1,r2,r3,r4,t1,hx,a,Ox,Oy,sig,t2),hy,0.01*abs(hy))
print "8:",1.0
print "9:",0.0

print "\nthe gradient bits for Sy:"
print "1:", derivative(lambda a: sfbe.Sy(a,r2,r3,r4,t1,hx,hy,Ox,Oy,sig,t2),r1,0.01*abs(r1))
print "2:", derivative(lambda a: sfbe.Sy(r1,a,r3,r4,t1,hx,hy,Ox,Oy,sig,t2),r2,0.01*abs(r2))
print "3:", derivative(lambda a: sfbe.Sy(r1,r2,a,r4,t1,hx,hy,Ox,Oy,sig,t2),r3,0.01*abs(r3))
print "4:", derivative(lambda a: sfbe.Sy(r1,r2,r3,a,t1,hx,hy,Ox,Oy,sig,t2),r4,0.01*abs(r4))
print "5:", derivative(lambda a: sfbe.Sy(r1,r2,r3,r4,a,hx,hy,Ox,Oy,sig,t2),t1,0.02)
print "6:", derivative(lambda a: sfbe.Sy(r1,r2,r3,r4,t1,a,hy,Ox,Oy,sig,t2),hx,0.01*abs(hx))
print "7:", derivative(lambda a: sfbe.Sy(r1,r2,r3,r4,t1,hx,a,Ox,Oy,sig,t2),hy,0.01*abs(hy))
print "8:", 0.0
print "9:", 1.0

print "\nthe derivatives wrt t2:"
print "Sx:", derivative(lambda a: sfbe.Sx(r1,r2,r3,r4,t1,hx,hy,Ox,Oy,sig,a),t2,0.02)
print "Sy:", derivative(lambda a: sfbe.Sy(r1,r2,r3,r4,t1,hx,hy,Ox,Oy,sig,a),t2,0.02)

print "\nAnd now for cool shit:"
print "r=",sfbe.residuals(x,y,v,sig,thetas)
print "J=",sfbe.jacobian(v,sig,thetas)

print "\nThey're the right sizes, right?"
print "residual:", sfbe.residuals(x,y,v,sig,thetas).shape[0]==2*x.shape[0]
print "Jacobian:", sfbe.jacobian(v,sig,thetas).shape==(2*x.shape[0],9+x.shape[0])