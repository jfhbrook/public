#!/usr/bin/env python

from math import log
from scipy.interpolate import interp2d

class 2dtable(filename):
    def __init__(filename):
        with open(filename) as datafile:
            reader = csv.reader(datafile)
            #get the "x" coordinates"
            axes=[map(float,reader.next()[1:-1]),[]]
            data=[]
            #grab "y" coordinates and "z" values
            for row in reader:
                data.append(map(float,row[1:-1]))
                axes[1].append(float(row[0]))

        #2d splines from scipy.interpolate
        #There are lots of other toys in there, but the docs suck imo
        #interp2d might be older, but I can figure out how to use it
        #at least. XD
        self.function=interp2d(axes[0],axes[1],data,kind='cubic')
        
    def __call__(x,y):
        #This is where you'd enter in x,y and get z
        return self.function(x,y)


class Propstable(filename):
    def __init__(filename):
        with open(filename) as datafile:
            reader = csv.reader(datafile)
            #get the "x" coordinates"
            axis=map(float,reader.next())
            data=[]
            #grab "y" coordinates and "z" values
            for row in reader:
                data.append(map(float,row))

    #TODO: Make up a good way to find any xi with any xj
        
    def __call__(x,y):



def h(cp,density,dvisc,k,l,vel):
    #assumes flat plate
    re = density*vel*l/dvisc
    pr = dvisc*cp/k
    return 0.037*(re**0.8)*(pr**0.33333)*k/l

def u(h,rsteel,asurf):
    #rsteel is thickness/ksteek
    return (2*/(h) +asurf*rsteel)**-1.

#This stuff probably shouldn't be a class.
def main():
        #self.T_h_in = T_h_in
        #self.T_h_out = T_h_out
        #self.T_c_in = T_c_in
        #self.T_c_out = T_c_out

    def LMTD(self):
        delT_a = self.T_h_in-self.T_c_out
        delT_b = self.T_c_out-self.T_h_in
        #TODO: Need to incorporate a correction factor look-up
        f=0.8
        return f*(delT_a-delT_b)/log(delT_a/delT_b)

    def R(self):
        return (self.T_h_in-self.T_h_out)/(T_c_out-T_c_in)
    def P(self):
        return (self.T_c_out-self.T_c_in)/(self.T_h_in-T_c_in)

    def qdot(self,T_in,T_out):
        return self.mdot*self.cp*(T_in-T_out)



