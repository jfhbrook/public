#!/usr/bin/python

import quantities as units #awesome
from keas.unit.unit import UnitConverter #...but quantities can't do scale conversions with non-matching zeroes.
from numpy import array #for dropping units

from libtsl import textable #might be the single most useful thing I've ever done

#temperature conversion
def FtoC(T):
    c=UnitConverter()
    return float(c.convert('tempF('+str(T)+')', 'tempC'))

def main():
    # Fig. 1: Awesome system diagram
    #
    #          (2) .----[comp]---. (1)
    # q_out <-- [cond]         [evap] <--q_in
    #          (3) '---[valve]---' (4)
    
    #There are a bunch of quantities we want to define first:
    #Data from our experiment:
    m_water_evap=[50.00, 30.00, 20.00, 20.00, 20.00] *units.g/units.s
    T_evap=[18.00, 12.00, 12.00, 11.00, 13.00] *units.C
    T_water_evap_in=[17.50, 18.00,17.00,17.00,15.00] *units.C
    T_water_evap_out=[18.50, 18.00, 18.00,18.00,18.00] *units.C
    P_evap_R11=[52.00, 58.00, 58.00, 58.00,38.00] *units.N/(units.m**2.)*10.**3.0

    q_comp_wattsup=230.0 *units.W #from a Watts-Up Meter
    
    m_water_cond=[5.00,4.00,4.00,20.00,50.00] *units.g/units.s
    T_cond=[23.00,27.00,28.00,22.00,23.00] *units.C
    T_water_cond_in=[20.00,20.00,21.00,20.00,19.00] *units.C
    T_water_cond_out=[26.00,29.00,29.00,22.00,21.00] *units.C
    P_cond_R11=[52.00,64.00,65.00,44.00,52.00] *units.N/(units.m**2.)*10.**3.0

    #Anything else I'll need
    C_p_water=4.184 *units.J/units.kg/units.C
    T_amb=FtoC(70.0) *units.C #Probably

    #Heat loss information supplied by HEB's manual:
    #Calculates based on earlier-defined values
    q_evap_surr=0.8*(T_amb-T_evap) *units.W/units.C #heat sent to surroundings
    q_comp_surr=20.0 *units.W #heat lost around compressor stage
    q_cond_surr=0.8*(T_amb-T_cond) *units.W/units.C #heat sent to surroundings

    #The heat absorbed by the evaporator
    q_evap=m_water_evap*C_p_water*(T_water_evap_out-T_water_evap_in)+q_evap_surr
    q_evap.units=units.W

    #The heat rejected by the condensor
    q_cond=m_water_cond*C_p_water*(T_water_cond_out-T_water_cond_in)-q_cond_surr
    q_cond.units=units.W
    
    #The work required by the compressor
    q_comp=q_cond+q_comp_surr-q_evap #energy balance
    #compare to q_comp_wattsup
    q_comp.units=units.W
    #The COP of the refrigeration system
    COP_fridge=q_evap/q_comp
    COP_heater=q_cond/q_comp

    #pretty printing
    #kinda

    print r'\documentclass[12pt]{article}'
    print r'\begin{document}'
    print r'Evaporator:\\'
    textable([['1','2','3','4','5'],
              array(m_water_evap),
              array(T_evap),
              array(T_water_evap_in),
              array(T_water_evap_out),
              0.001*array(P_evap_R11)],

             [r'Test \#', 
              r'Mass Flow Rate (g/s)', 
              r'\(T_{\textrm{R11}}\) (C)',
              r'\(T_\textrm{in}\) (C)',
              r'\(T_\textrm{out}\) (C)',
              r'\(P_{\textrm{R11}}\) (kPa)'])
    print ''
    print r'Condensor:\\'
    textable([['1','2','3','4','5'],
              array(m_water_cond),
              array(T_cond),
              array(T_water_cond_in),
              array(T_water_cond_out),
              0.001*array(P_cond_R11)],

             [r'Test \#', 
              r'Mass Flow Rate (g/s)', 
              r'\(T_{\textrm{R11}}\) (C)',
              r'\(T_\textrm{in}\) (C)',
              r'\(T_\textrm{out}\) (C)',
              r'\(P_{\textrm{R11}}\) (kPa)'])

    print ''
    print r'Calculated Values:\\'
    textable([['1','2','3','4','5'],
              array(q_evap),
              array(q_cond),
              array(q_comp),
              array(COP_fridge),
              array(COP_heater)],
              [r'Test \#',
               r'\(q_{\textrm{evap.}}\) (W)',
               r'\(q_{\textrm{cond.}}\) (W)',
               r'\(q_{\textrm{comp.}}\) (W)',
               'cooling COP',
               'heating COP'])
    print r'\end{document}'

if __name__ == '__main__':
    main()
