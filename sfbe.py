#! /usr/bin/env python
"""This is meant to be an implementation of the Gauss-Newton optimization
method on the position equations for a four-bar linkage. Currently, it works
for 'really nice' situations; also, only for one dyad configuration, since
one working pretty much necessarily means the other one isn't a 
'really nice' situation.

Use linkagefit(points,v,tvector) to get a solution."""

from numpy import *
from scipy import linalg, derivative


#These form the forward motion equation(s) for the four-bar.
#They're used to build up the Jacobian and the residual.
def A(r1,r2,r4,t1,t2): return 2*r1*r4*cos(t1)-2*r2*r4*cos(t2)
def B(r1,r2,r4,t1,t2): return 2*r1*r4*sin(t1)-2*r2*r4*sin(t2)
def C(r1,r2,r3,r4,t1,t2): return r1**2+r2**2+r4**2-r3**2-2*r1*r2*(cos(t1)*cos(t2)+sin(t1)*sin(t2))
def t4(r1,r2,r3,r4,t1,sig,t2): return 2*arctan((-B(r1,r2,r4,t1,t2)+sig*(B(r1,r2,r4,t1,t2)**2-C(r1,r2,r3,r4,t1,t2)**2+A(r1,r2,r4,t1,t2)**2)**0.5)/(C(r1,r2,r3,r4,t1,t2)-A(r1,r2,r4,t1,t2)))
def Px(r1,r2,r3,r4,t1,Ox,sig,t2): return r1*cos(t1)+r4*cos(t4(r1,r2,r3,r4,t1,sig,t2))+Ox
def Py(r1,r2,r3,r4,t1,Oy,sig,t2): return r1*sin(t1)+r4*sin(t4(r1,r2,r3,r4,t1,sig,t2))+Oy
def Qx(r2,Ox,t2): return r2*cos(t2)+Ox
def Qy(r2,Oy,t2): return r2*sin(t2)+Oy
def Sx(r1,r2,r3,r4,t1,hx,hy,Ox,Oy,sig,t2): return (1-hx)*Qx(r2,Ox,t2)+hx*Px(r1,r2,r3,r4,t1,Ox,sig,t2)+hy*(Qy(r2,Oy,t2)-Py(r1,r2,r3,r4,t1,Oy,sig,t2))
def Sy(r1,r2,r3,r4,t1,hx,hy,Ox,Oy,sig,t2): return (1-hx)*Qy(r2,Oy,t2)+hx*Py(r1,r2,r3,r4,t1,Oy,sig,t2)+hy*(Px(r1,r2,r3,r4,t1,Ox,sig,t2)-Qx(r2,Ox,t2))
def discr(r1,r2,r3,r4,t1,t2): return B(r1,r2,r4,t1,t2)**2-C(r1,r2,r3,r4,t1,t2)**2+A(r1,r2,r4,t1,t2)**2

def jacobian(v,sig,tvector):
    #This function defines the Jacobian of my problem.
    
    #Some gradients. These are numerical derivatives; I tried using
    #symbolic ones, but they gave me all sorts of trouble.
    #Note, the standard dx for derivative() is 1.0, which is honestly
    #kinda ridiculous imo.
    def grad_Sx(r1,r2,r3,r4,t1,hx,hy,Ox,Oy,sig,t2):
        return array([
        derivative(lambda a: Sx(a,r2,r3,r4,t1,hx,hy,Ox,Oy,sig,t2),r1,0.01*r1),
        derivative(lambda a: Sx(r1,a,r3,r4,t1,hx,hy,Ox,Oy,sig,t2),r2,0.01*r2),
        derivative(lambda a: Sx(r1,r2,a,r4,t1,hx,hy,Ox,Oy,sig,t2),r3,0.01*r2),
        derivative(lambda a: Sx(r1,r2,r3,a,t1,hx,hy,Ox,Oy,sig,t2),r4,0.01*r4),
        derivative(lambda a: Sx(r1,r2,r3,r4,a,hx,hy,Ox,Oy,sig,t2),t1,0.02),
        derivative(lambda a: Sx(r1,r2,r3,r4,t1,a,hy,Ox,Oy,sig,t2),hx,0.01*hx),
        derivative(lambda a: Sx(r1,r2,r3,r4,t1,hx,a,Ox,Oy,sig,t2),hy,0.01*hy),
        1.0,
        0.0])
    
    def grad_Sy(r1,r2,r3,r4,t1,hx,hy,Ox,Oy,sig,t2):
        return array([
        derivative(lambda a: Sy(a,r2,r3,r4,t1,hx,hy,Ox,Oy,sig,t2),r1,0.01*r1),
        derivative(lambda a: Sy(r1,a,r3,r4,t1,hx,hy,Ox,Oy,sig,t2),r2,0.01*r2),
        derivative(lambda a: Sy(r1,r2,a,r4,t1,hx,hy,Ox,Oy,sig,t2),r3,0.01*r3),
        derivative(lambda a: Sy(r1,r2,r3,a,t1,hx,hy,Ox,Oy,sig,t2),r4,0.01*r4),
        derivative(lambda a: Sy(r1,r2,r3,r4,a,hx,hy,Ox,Oy,sig,t2),t1,0.02),
        derivative(lambda a: Sy(r1,r2,r3,r4,t1,a,hy,Ox,Oy,sig,t2),hx,0.01*hx),
        derivative(lambda a: Sy(r1,r2,r3,r4,t1,hx,a,Ox,Oy,sig,t2),hy,0.01*hy),
        0.0,
        1.0])
    
    def dSxdt2(r1,r2,r3,r4,t1,hx,hy,Ox,Oy,sig,t2):
        return derivative(lambda a: Sx(r1,r2,r3,r4,t1,hx,hy,Ox,Oy,sig,a),t2,0.02)
    
    def dSydt2(r1,r2,r3,r4,t1,hx,hy,Ox,Oy,sig,t2):
        return derivative(lambda a: Sy(r1,r2,r3,r4,t1,hx,hy,Ox,Oy,sig,a),t2,0.02)
    
    #The block matrices for the Jacobian.
    #v contains all the parameters; It's here that I finally break them down.
    #There's probably a more elegant way to do it that I'm not aware of.
    #tvector contains all the \((theta_2)_j\)s,
    def Jx(v,sig,tvector):
        Jx=array([])
        for t2 in tvector:
            if Jx.shape[0]==0:
                Jx=grad_Sx(v[0],v[1],v[2],v[3],v[4],v[5],v[6],v[7],v[8],sig,t2)
            else:
                Jx=vstack((Jx,grad_Sx(v[0],v[1],v[2],v[3],v[4],v[5],v[6],v[7],v[8],sig,t2)))
        return Jx
    
    def Jy(v,sig,tvector):
        Jy=array([])
        for t2 in tvector:
            if Jy.shape[0]==0:
                Jy=grad_Sy(v[0],v[1],v[2],v[3],v[4],v[5],v[6],v[7],v[8],sig,t2)
            else:
                Jy=vstack((Jy,grad_Sy(v[0],v[1],v[2],v[3],v[4],v[5],v[6],v[7],v[8],sig,t2)))
        return Jy
    
    #hopefully these are as slick as I think they are.
    def Dx(v,sig,tvector):
        return diag(dSxdt2(v[0],v[1],v[2],v[3],v[4],v[5],v[6],v[7],v[8],sig,tvector),0)

    def Dy(v,sig,tvector):
        return diag(dSydt2(v[0],v[1],v[2],v[3],v[4],v[5],v[6],v[7],v[8],sig,tvector),0)

    return hstack((vstack((Jx(v,sig,tvector),Jy(v,sig,tvector))),vstack((Dx(v,sig,tvector),Dy(v,sig,tvector)))))

#Mr. Jacobian's good friend.
#Also hopefully as slick as I think it is.
def residuals(x,y,w,sig,tvector):
    return hstack((Sx(w[0],w[1],w[2],w[3],w[4],w[5],w[6],w[7],w[8],sig,tvector)-x,Sy(w[0],w[1],w[2],w[3],w[4],w[5],w[6],w[7],w[8],sig,tvector)-y))

#A single iteration of the method.
def iteration(points,v,sig,tvector):
    x=hstack((v,tvector))
    J=jacobian(v,sig,tvector)
    r=residuals(points[:,0],points[:,1],v,sig,tvector)
    dell=dot(J.T,r)
    #Solving this with a conjugate gradient method,
    #Hopefully the zero entries lead to some savings, but I haven't really checked.
    #there may also be a way to get savings by not multiplying out J'J,
    #but idk how to do that.
    pk=linalg.cg(dot(J.T,J),-dell)[0]
    #Using backtracking to get alpha
    #Using this method because it's what I know.
    #http://en.wikipedia.org/wiki/Wolfe_conditions
    alpha=1.0 #"For Newton and quasi-Newton methods, the step \(\alpha_0 = 1\) should always be used as the initial trial step length."--pg. 59
    rho=0.7 #between 0 and 1
    c=0.1**6 #The "C_1" used in the first wolfe condish. between 0 and 1, typically "quite small"
    xnew=x+alpha*pk
    rnew=residuals(points[:,0],points[:,1],xnew[0:9],sig,xnew[9:x.shape[0]])
    #this is to prevent sticking when the solution is outside the boundary.
    #I don't think it works very well.
    tired=False
    while (dot(rnew,rnew) > dot(r,r)+c*alpha*dot(dell,pk) or not (discr(xnew[0],xnew[1],xnew[2],xnew[3],xnew[4],xnew[9:x.shape[0]])>=0).all()) and not tired:
        alpha=rho*alpha
        xnew=x+alpha*pk
        rnew=residuals(points[:,0],points[:,1],xnew[0:9],sig,xnew[9:x.shape[0]])
        if (rho < 0.1**2) and (discr(xnew[0],xnew[1],xnew[2],xnew[3],xnew[4],xnew[9:x.shape[0]])>=0).all():
            print "warning: Boundary condition issues"
            tired=True
    return xnew[0:9],xnew[9:x.shape[0]]
    
#Everything comes together here.
def linkagefit(points,v,tvector):
    #returns fitted v, dyad configuration and fitted thetas in that order.
    threshhold=0.1**4 #Some measure of how much improvement the algorithm's
                     #producing.
    returns=1 #Make sure this is bigger than the threshhold.
              #Otherwise it doesn't matter.
    vnew=v
    tnew=tvector
    #Choosing the best dyad to pursue.
    #Could be nicer computationally.
    if dot(residuals(points[:,0],points[:,1],vnew,-1,tnew),residuals(points[:,0],points[:,1],vnew,-1,tnew)) < dot(residuals(points[:,0],points[:,1],vnew,1,tnew),residuals(points[:,0],points[:,1],vnew,1,tnew)):
        sig=-1
    else: sig=1
    
    rnew=residuals(points[:,0],points[:,1],vnew,sig,tnew)
    while returns > threshhold:
        vnew,tnew=iteration(points,vnew,sig,tnew)
        rolde=rnew
        rnew=residuals(points[:,0],points[:,1],vnew,sig,tnew)
        returns=dot(rolde,rolde)/dot(rnew,rnew)-1
    return vnew,sig,tnew
