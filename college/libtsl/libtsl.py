from math import pi
import xlrd #, xlwt
import csv

###data input

#Reads in data points
def csvdata(filename):
    datareader=csv.reader(open(filename))
    titles=datareader.next()
    datalists=[]
    for row in datareader:
        datalists.append(row)
    print titles
    #some outrageous shit >_<
    return dict(zip(titles,
                    [list(tupl) for tupl in zip(*datalists)]))

###data output

#data LaTeX formatting
#copy-paste or pipe
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


#data excel formatting
#saves to file
#UNTESTED
def exceltable(columns,titles,filename):
    workbook=xlwt.Workbook()
    sheet=workbook.add_sheet("Some Table or Other")
    for i, entry in enumerate(titles):
        sheet.write(i,0, entry, xlwt.easyxf('bold on'))
    for j, column in enumerate(columns):
        for i, entry in enumerate(column):
            sheet.write(i,j,entry)
    workbook.save(filename)

###data manipulations

#subsets data (every nth entry)
def subset(set,n):
    sub=[]
    for i in range(len(set)):
        if i%n==0:
            sub=sub+[set[i]]
    return sub

#sphere geometry
class geometry:
    def __init__(self,geometry,lc):
        self.geom=geometry
        if self.geom=="sphere":
            self.d=lc
            self.r=lc/2.0
            self.xsect=pi*self.r**2.0
            self.sarea=4.0*self.xsect
            self.vol=(4.0/3.0)*pi*self.r**3.0
        elif self.geom=="rod":
            self.d=lc
            self.r=lc/2.0
            self.xsect=pi*self.r**2.0
            self.p=pi*lc

#a shit-ton of heat transfer params
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

    def biot(self):
        return h*l/k_s

    def nusselt(self):
        return h*l/k_f

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

    def hr(self,Tsurf):
        #Don't forget to use absolute temps!
        stefboltz=0.1714e-8/3600.0 #courtesy cengel
        return self.emiss*stefboltz*(Tsurf**4.0-self.Tinf**4.0)/(Tsurf-self.Tinf)

    def hc(self,Tf, geom):
        #Tf is for "Tfilm" and is a hangover from how the first assignment was specified.
        if geom=="sphere":
            #Incropera and Dewitt's empirical equation for hc
            return (2+(0.589*(self.rayleigh(Tf))**0.25)/(1+(0.469/self.prandtl(Tf))**(9.0/16.0))**(4.0/9.0))*(self.k_f/self.l)
        if geom=="rod":
            #Courtesy Cengel
            return (self.k_f/self.l)*((0.387*(self.rayleigh(Tf)**(1.0/6.0)))/(1.0 + (0.559/self.prandtl(Tf))**(9/16))**(8.0/27.0))**2.0

#returns viscosity in centipoise based on params from DV-1 viscometer
def dv2cP(reading,model,number,rpm):
    #pg.3-7 of manual-->excel-->csv-->gnumeric-->csv-->ctrl-c,ctrl-v >_<;;;
    table={'RV': [[200,100,50,40,25,20,10,5,2,1],
    [800,400,200,160,100,80,40,20,8,4],
    [2000,1000,500,400,250,200,100,50,20,10],
    [4000,2000,1000,800,500,400,200,100,40,20],
    [8000,4000,2000,1600,1000,800,400,200,80,40],
    [20000,10000,5000,4000,2500,2000,1000,500,200,100],
    [80000,40000,20000,16000,10000,8000,4000,2000,800,400]],
    'LV': [[200,100,40,20,10,5,2,1],
    [1000,500,200,100,50,25,10,5],
    [4000,2000,800,400,200,100,40,20],
    [20000,10000,4000,2000,1000,500,200,100]]}

    return reading*table[model][number-1][[0.5,1.,2.,2.5,4.,5.,10.,20.,50.,100.].index(rpm)]
