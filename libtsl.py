from math import pi

#data manipulations
def subset(set,n):
    sub=[]
    for i in range(len(set)):
        if i%n==0:
            sub=sub+[set[i]]
    return sub

class sphere:
    def __init__(self,d):
        self.d=d
        self.r=d/2.0
        self.xsect=pi*self.r**2.0
        self.sarea=4.0*self.xsect
        self.vol=(4.0/3.0)*pi*self.r**3.0

#heat transfer params
class htparams:
    def __init__(self,**args):
        self.g=args.get('g',9.81)
        self.l=args.get('l',1.0)
        self.xsect=args.get('xsect',1.0)
        self.sarea=args.get('sarea',1.0)
        self.vol=args.get('vol',1.0)
        self.Tinf=args.get('Tinf',273.15)

        self.kvisc=args.get('kvisc',False)
        self.rho=args.get('rho',False)
        self.dvisc=args.get('dvisc',False)
        if(not self.kvisc and self.rho and self.dvisc):
            self.kvisc=self.dvisc/self.rho
        if(not self.dvisc and self.rho and self.kvisc):
            self.dvisc=self.kvisc*self.rho
        self.k=args.get('k',False)
        self.cp=args.get('cp',False)
        self.alpha=args.get('alpha',False)
        if (not self.alpha and self.rho and self.cp and self.k):
            self.alpha=self.k/(self.rho*self.cp)
        self.h=args.get('h',False)
        self.emiss=args.get('emiss',1.0)
        self.thermexp=args.get('thermexp',1.0)

#    def biot(self)
#        return h*l/k

    def rayleigh(self,Tf):
        print 'Ra=', self.grashof(Tf)*self.prandtl(Tf)
        return self.grashof(Tf)*self.prandtl(Tf)

    def grashof(self,T):
        print 'Gr=', self.g * self.thermexp * (T-self.Tinf)*(self.l**3.0)/(self.kvisc**2)
        return (self.g*self.thermexp*(T-self.Tinf)*self.l**3.0)/(self.kvisc**2)

    def prandtl(self,T):
        print 'Pr=', self.kvisc/self.alpha
        return self.kvisc/self.alpha

    def reynolds(self):
        return self.v*self.l/self.kvisc

    def Tfilm(self,Tzero,Tfinal):
        return 0.25*(Tzero+Tfinal)+0.5*self.Tinf

    #specific to metal sphere
    def hc(self,Tzero,Tfinal):
        #Incropera and Dewitt's empirical equation for hc
        #May depend on Englilish units.
        Tf=self.Tfilm(Tzero,Tfinal)
        return (self.k/self.l)*((0.589*self.rayleigh(Tf)**0.25)/(1+(0.469/self.prandtl(Tf))**(9.0/16.0))**(4.0/9.0)+2)

    def hr(self,Tsurf):
        #Don't forget to use absolute temps!
        stefboltz=5.6704e-5/1055.0559/1550.0031/1.8 #thx units as well
        #thx http://en.wikipedia.org/wiki/Stefan%E2%80%93Boltzmann_constant
        return self.emiss*stefboltz*(Tsurf**4.0-self.Tinf**4.0)/(Tsurf-self.Tinf)
