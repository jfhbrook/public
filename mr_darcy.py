from math import log10

def frictionfactor(Re,relrough):
    """
    Returns the Darcy friction factor based on reynolds # and relative roughness.
    """
    try:
        regime = _flowregime(Re,relrough)
    else:
        if regime=='laminar':
            return _laminar(Re)
        elif regime=='turbulent':
            return _turbulent(Re,relrough)

def _flowregime(Re,relrough):
    if Re < 2300.:
        return "laminar"
    if Re > 4000.:
        return "turbulent"
    else:
        raise RegimeError(Re,relrough)

def _laminar(Re): return 64.0/Re

def _turbulent(Re,relrough):
    # Uses Serghides's Solution to approximate solutions for the Darcy friction
    # factor in the Colebrook-White equation. In other words, this is
    # equivalent to looking up the Darcy friction factor on the Moody Diagram,
    # and (in fact) if you plotted log10(f) vs. log10(Re) for level curves of 
    # relative roughness, you would find yourself with a very nice looking
    # Moody diagram (for turbulent flow ranges).
    a=-2*log10(relrough/3.7 + 12.0/Re)
    b=-2*log10(relrough/3.7 + 2.51*a/Re)
    c=-2*log10(relrough/3.7 + 2.51*b/Re)
    return (a-(b-a)**2/(c-2*b+a))**-2.0 #returns f

class RegimeError(ValueError):
    def __init__(self):
        self.explain = "Flow regime transitory!"
        self.values = {"laminar": _laminar(Re), 
                       "turbulent": _turbulent(Re,roughness)}
    def __str__(self):
        return repr(explain)
