from math import pi

#data LaTeX formatting
def textable(columns,titles):
    print r'\begin{tabular}{*{'+str(len(columns))+r'}{l}}'
    print ' & '.join(titles), r'\\'
    print r'\hline'
    for row in zip(*columns):
        strrow=[]
        for element in row:
            strrow.append(str(element))
        print ' & '.join(strrow), r'\\'
    print r'\end{tabular}','\n'

#data manipulations
def subset(set,n):
    sub=[]
    for i in range(len(set)):
        if i%n==0:
            sub=sub+[set[i]]
    return sub

#sphere geometry
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
        self.rho_f=args.get('rho_f',False)
        self.rho_s=args.get('rho_s',False)
        self.dvisc=args.get('dvisc',False)
        if(not self.kvisc and self.rho_f and self.dvisc):
            self.kvisc=self.dvisc/self.rho_f
        if(not self.dvisc and self.rho_f and self.kvisc):
            self.dvisc=self.kvisc*self.rho_f
        self.k_f=args.get('k_f',False)
        self.k_s=args.get('k_s',False)
        self.cp_f=args.get('cp_f',False)
        self.cp_s=args.get('cp_s',False)
        self.alpha=args.get('alpha',False)
        if (not self.alpha and self.rho_f and self.cp_f and self.k_f):
            self.alpha=self.k_f/(self.rho_f*self.cp_f)
        self.h=args.get('h',False)
        self.emiss=args.get('emiss',1.0)
        self.thermexp=args.get('thermexp',1.0/self.Tinf)

#    def biot(self)
#        return h*l/k

    def rayleigh(self,Tf):
        return self.grashof(Tf)*self.prandtl(Tf)

    def grashof(self,T):
        return (self.g*self.thermexp*(T-self.Tinf)*((self.l)**3.0))/((self.kvisc)**2.0)

    def prandtl(self,T):
        return self.kvisc/self.alpha

    def reynolds(self):
        return self.v*self.l/self.kvisc

    def Tfilm(self,Tzero,Tfinal):
        return 0.25*(Tzero+Tfinal)+0.5*self.Tinf

    #specific to metal sphere
    def hc(self,Tzero,Tfinal):
        #Incropera and Dewitt's empirical equation for hc
        Tf=self.Tfilm(Tzero,Tfinal)
        return (2+(0.589*(self.rayleigh(Tf))**0.25)/(1+(0.469/self.prandtl(Tf))**(9.0/16.0))**(4.0/9.0))*(self.k_f/self.l)

    def hr(self,Tsurf):
        #Don't forget to use absolute temps!
        stefboltz=0.1714e-8/3600.0 #courtesy cengel
        return self.emiss*stefboltz*(Tsurf**4.0-self.Tinf**4.0)/(Tsurf-self.Tinf)