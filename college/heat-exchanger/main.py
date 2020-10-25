from tabular import 2dtable, Continuoustable, Discretetable
from htxr import Tparams, Htxrparams
from scipy import mean

def main():
    #Tables
    coolant_samples = Discretetable("data/engine_coolant_data.csv")
    schmidt_plates = Discretetable("data/schmidt_data.csv")
    glycol_props = Continuoustable("data/ethylene_glycol_o.5byvol_lut.csv")
    correction_factor = 2dtable("data/lmtd_cross_unmixed_correction_factors.csv")

    #TODO: figure out what this conversion is
    gpm2cftps=1.0

    #TODO: Find better way to deal with coolant samples
    T_h_in=mean(coolant_samples["Outlet (F)"])
    T_h_out=mean(coolant_samples["Inlet (F)"])
    T_c_in=120.
    T_c_out=100.
    voldot_h=avg(coolant_samples["Q (GPM)"])

    #Template for temperature params--need to specify somehow
    #Decide on T_c's, figure out best method for dealing with coolant_samples
    temps=Tparams(T_h_in,T_h_out,T_c_in,T_c_out)

    #Template for htxr--need to iterate through values from schmidt_plates
    #(listcomp?)
    htxr=Htxparams(lx,ly,lz_0,del_lz,As_plate,del_W,density)

    rho_h=glycol_props(temps.T_h_avg,"Density (lb/cft)")
    cp_h=glycol_props(temps.T_h_avg, "Cp (Btu/lb/F)")
    rho_c=glycol_props(temps.T_h_avg,"Density (lb/cft)")
    cp_c=glycol_props(temps.T_c_avg, "Cp (Btu/lb/F)")
    k_h=glycol_props(temps.T_h_avg, "K (Btu*ft/hr/sft/F)")
    k_c=glycol_props(temps.T_c_avg, "K (Btu*ft/hr/sft/F)")
    dvisc_h=glycol_props(temps.T_h_avg, "Dynamic Viscosity (ft/lb/h)")/3600. #per second now
    dvisc_c=glycol_props(temps.T_c_avg, "Dynamic Viscosity (ft/lb/h)")/3600.

    qdot=voldot_h*gpm2cftps*rho_h*cp_h*temps.delT_h
    voldot_c=qdot/(cp_c*temps.delT_c*gpm2cftps*rho_c)


    #TODO!!
    t_plate=????
    t_gap=????
    A_s_plate=????
    l_x
    l_z
    k_solid=????

    #TODO!!
    vel_h=velocity(voldot_h,lx,lz_0+dellz*N)
    vel_c=velocity(voldot_c,lx,lz_0+dellz*N)

    #Gonna need some looping shit here :S
    h_h=h(k_h,t_gap,Re(density_h,vel_h,t_gap,dvisc_h),Pr(dvisc_h,cp_h,k_h))
    h_c=h(k_h,t_gap,Re(density_c,vel_c,t_gap,dvisc_c),Pr(dvisc_c,cp_c,k_c))

    u=((1./h_h)+(1./h_c)+(A_s_plate*t_plate/k_solid))**(-1.) #Hooray!

    #Find zeros of:
    qdot/F(temps.R,temps.P)/temps.LMTD_cf - u

def velocity(voldot
,lx,lz):
    return 2*voldot/lx/lz    

def Qdot(mdot,cp,delt):
    return mdot*cp*delt

def Re(density,vel,l,dvisc):
    return density*vel*l/dvisc

def Pr(dvisc,cp,k):
    return dvisc*cp/k

def h(k,l,re,pr):
    #assumes flat plate
    return 0.037*(re**0.8)*(pr**(1./3.))*k/l

def u(h,thickness,ksteel,asurf):
    rsteel=thickness/ksteek
    return (2*/(h) +asurf*rsteel)**-1.

