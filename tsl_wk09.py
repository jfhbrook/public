#!/usr/bin/env python

import quantities as units
from mr_darcy import *

def main():
    # Specific gravity of manometer fluid, from apparatus manual
    s = 0.985

    # TODO: Import excel bs

    # TODO: Loop through relevant values from excel sheet
    delphead = 10.0 * units.inch / s
    print v(delphead)
    # TODO: use this v to get flow rate

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
    print "running"
    main()
else:
    print "loljoshtarded"
