from scipy import log10

def frictionfactor(roughness,Re):
    try:
        

def _flowregime(Re):
    if Re < 2300.:
        return "laminar"
    if Re > 4000.:
        return "turbulent"
    else:
        # transition behavior
        raise ValueError

def _laminar(Re): return 64.0/Re

def _turbulent(roughness,Re):
    # Uses Serghides's Solution to approximate solutions for the Darcy friction
    # factor in the Colebrook-White equation. In other words, this is
    # equivalent to looking up the Darcy friction factor on the Moody Diagram,
    # and (in fact) if you plotted log10(f) vs. log10(Re) for level curves of 
    # relative roughness, you would find yourself with a very nice looking
    # Moody diagram (for turbulent flow ranges).
    a=-2*log10(roughness/3.7 + 12.0/Re)
    b=-2*log10(roughness/3.7 + 2.51*a/Re)
    c=-2*log10(roughness/3.7 + 2.51*b/Re)
    return (a-(b-a)**2/(c-2*b+a))**-2.0 #returns f
