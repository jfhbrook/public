#!/usr/bin/env python

import quantities as units
from mr_darcy import *
from xlrd import open_workbook
from math import pi
from numpy import array, zeros

def main():
    # Specific gravity of manometer fluid, from apparatus manual
    s = 0.985

    # Import excel info
    # open_workbook is supposed to support the with/as thing, but, u noe :S
    f = open_workbook('thursday_data.xls', 'rb')
    sheet = f.sheet_by_index(0)
    mdot_w = array(sheet.col_values(2,8,15)) * units.lb/units.minute
    temp_w_i = array(sheet.col_values(3,8,15))
    temp_w_o = array(sheet.col_values(4,8,15))
    temp_a_i = array(sheet.col_values(5,8,15))
    temp_a_o = array(sheet.col_values(6,8,15))
    temp_pipe_i = array(sheet.col_values(7,8,15))
    temp_pipe_o = array(sheet.col_values(8,8,15))
    phead = array(sheet.col_values(9,8,15)) * units.inch/s

    # Air speed and flow rate
    v = zeros(phead.shape)
    Q = zeros(phead.shape)
    v_a = [airv(h) for h in phead]
    #print v_a
    Q_a = [(0.25*pi*(0.75*units.inch)**2*vel).rescale('ft^3/s') for vel in v_a]
    #print Q_a

    # Water speed and flow rate
    Q_w = (mdot_w / (1000.0*units.kg/(units.m)**3)).rescale('ft^3/s')
    print Q_w
    # The apparatus manual claims a bore of 1".
    # I wasn't sure what to make of it.
    # I'll measure the apparatus later.
    v_w = Q_w/(0.25*pi*(1.00*units.inch)**2)

    # TODO: Calculate LMTD -- Note method slightly different for
    # parallel flow and counter-flow!
    # TODO: Calculate H.T. rate (mdot*cp*delT)
    # TODO: Calculate some kinda theoretical maximum (???)
    # TODO: Calculate effectiveness (easy given HT rate and theoretical max)

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

if __name__ == "__main__":
    main()
