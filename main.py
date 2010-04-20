from tabular import 2dtable, Propstable
from htxr import Tparams

def main():
    #Tables
    coolant_samples = Discretetable("data/engine_coolant_data.csv")
    schmidt_plates = Discretetable("data/schmidt_data.csv")
    glycol_props = Continuoustable("data/ethylene_glycol_o.5byvol_lut.csv")
    correction_factor = 2dtable("data/lmtd_cross_unmixed_correction_factors.csv")

    #Template for temperature params--need to specify somehow
    #Decide on T_c's, figure out best method for dealing with coolant_samples
    temps=Tparams(T_h_in,T_h_out,T_c_in,T_c_out)

    #Template for htxr--need to iterate through values from schmidt_plates
    #(listcomp?)
    htxr=Htxparams(lx,ly,lz_0,del_lz,As_plate,del_W,density)



def h(k,l,re,pr):
    #assumes flat plate
    re = density*vel*l/dvisc
    pr = dvisc*cp/k
    return 0.037*(re**0.8)*(pr**(1./3.))*k/l

def u(h,thickness,ksteel,asurf):
    rsteel=thickness/ksteek
    return (2*/(h) +asurf*rsteel)**-1.
