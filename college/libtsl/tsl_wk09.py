#!/usr/bin/env python

import quantities as units
from mr_darcy import *
from xlrd import open_workbook
from math import pi
from numpy import array, zeros, hstack
from scipy import log

def main():
    # Specific gravity of manometer fluid, from apparatus manual
    s = 0.985

    # Import excel info
    # open_workbook is supposed to support the with/as thing, but, u noe :S
    f = open_workbook('thursday_data.xls', 'rb')
    sheet = f.sheet_by_index(0)
    mdot_w = array(sheet.col_values(2,8,16)) * units.lb/units.minute
    temp_w_i = array(sheet.col_values(3,8,16)) * units.degF
    temp_w_o = array(sheet.col_values(4,8,16)) * units.degF
    temp_a_i = array(sheet.col_values(5,8,16)) * units.degF
    temp_a_o = array(sheet.col_values(6,8,16)) * units.degF
    temp_pipe_i = array(sheet.col_values(7,8,16)) * units.degF
    temp_pipe_o = array(sheet.col_values(8,8,16)) * units.degF
    phead = array(sheet.col_values(9,8,16)) * units.inch/s

    # Air speed and flow rate
    print "air velocity:"
    v_a = [airv(h) for h in phead]
    v_a = clean_quantities(v_a)
    printzor(v_a)
    print "air flow rate:"
    Q_a = [(0.25*pi*(0.75*units.inch)**2*vel).rescale('ft^3/s') for vel in v_a]
    Q_a = clean_quantities(Q_a)
    printzor(Q_a)

    # Water speed and flow rate
    Q_w = (mdot_w / (1000.0*units.kg/(units.m)**3)).rescale('ft^3/s')
    Q_w = clean_quantities(Q_w)
    print "water flow rate:"
    printzor(Q_w)
    # The apparatus manual claims a bore of 1".
    # I wasn't sure what to make of it.
    # I'll measure the apparatus later.
    print "water velocity in hose:"
    v_w = Q_w/(0.25*pi*(1.00*units.inch)**2)
    printzor(v_w)

    # Calculate LMTD -- Note method slightly different for
    # parallel flow and counter-flow!
    print "LMTDs:"
    lmtd_ll = lmtd(temp_a_o[0:4]-temp_w_i[0:4],temp_a_i[0:4]-temp_w_o[0:4])
    lmtd_xf = lmtd(temp_a_o[4:8]-temp_w_i[4:8],temp_a_i[4:8]-temp_w_o[4:8])
    print "parallel,"
    printzor(lmtd_ll)
    print "counter-flow,"
    printzor(lmtd_xf)

    # Calculate H.T. rate (mdot*cp*delT)
    print "Heat transfer rate action:"
    cp_w = 4.184 * units.J/units.gram/units.celsius
    cpv_a = 0.001297 * units.J/(units.cm**3)/units.degC
    Cwater = (cp_w*mdot_w).rescale("W/degC")
    Cair = (cpv_a*Q_a).rescale('W/degC')
    print "by water,"
    htr8s = (Cwater*(temp_w_o-temp_w_i)).rescale("watts")
    printzor(htr8s)
    print "by air,"
    htr8s = (Cair*(temp_a_i-temp_a_o)).rescale("watts")
    printzor(htr8s)

    # Calculate heat transfer coefficients
    # surface areas from heat exchanger lab
    print "Heat transfer coefficients"
    As_i = 169.668 *units.inch**2
    As_o = 185.9561 *units.inch**2
    print hstack((lmtd_ll,lmtd_xf))
    # (hstack drops units :S)
    # I see potential for a decorator here <_<
    htcoeffs_o = htr8s/As_o/hstack((lmtd_ll,lmtd_xf))/units.degF
    htcoeffs_i = htr8s/As_i/hstack((lmtd_ll,lmtd_xf))/units.degF
    print "inside,"
    printzor(htcoeffs_i.rescale("W/m/m/degF"))
    print "outside,"
    printzor(htcoeffs_o.rescale("W/m/m/degF"))

    # Calculate the theoretical maximum--same deal really 
    print "Ideal heat transfer rate action:"
    #print Cwater
    #print Cair
    #calculates the minimum C for each case.
    cmin = clean_quantities(map(lambda a: min(a[0],a[1]),zip(Cwater,Cair)))
    #print cmin
    htr8s_max = (cmin*(temp_a_i-temp_w_i)).rescale("watts")
    printzor(htr8s_max)

    # Calculate effectiveness (easy given HT rate and theoretical max)
    print "effectiveness (%)"
    effectiveness = array(htr8s/htr8s_max)*100. 
    printzor(effectiveness)

def airv(delp):
    # Value for air at about 150 F. Cengel, A-15
    nu = 2.2e-4 * units.ft**2/units.s
    # Clean copper pipe. Crowe, pg.381
    roughness = 6.0e-5 *units.inch
    # Apparatus manual claims 3/4 inch bore
    d = 0.75 * units.inch
    # From memory
    g = 32.2 * units.ft/(units.s**2)
    # Apparatus manual lists this as air manometer separation
    length = 6.302 * units.ft
    vold = 0.0 * units.ft/units.s
    v = 0.025 * units.ft/units.s
    while (vold-v)**2 > 1e-6 * (units.ft/units.s)**2 :
        vold = v
        # Solved the Darcy-Weisbach equation for v assuming constant velocity 
        # and constant height, and assuming delhl=delp_head.
        v = ((2*delp*d*g)/(frictionfactor(vold*d/nu,roughness/d)*length))**0.5
    return v.rescale("ft/s")

def lmtd(delTa,delTb):
    return (delTa-delTb)/log(delTa/delTb)

def clean_quantities(dirty):
    #This pulls quantities out of an array and pops them on the outside
    unittypes=[val.units for val in dirty]
    # Should do sanity check and throw errors, but I don't care atm
    return array(dirty) * unittypes[0]

def printzor(array):
    for i, val in enumerate(array):
        print repr(i)+ ": " + str(val)
    print ""

if __name__ == "__main__":
    main()
