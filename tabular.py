from math import log
from scipy.interpolate import interp2d
from scipy.interpolate import UnivariateSpline as interp1d

#should work for correction factor table.
class 2dtable(filename):
    def __init__(filename):
        with open(filename) as datafile:
            reader = csv.reader(datafile)
            #get the "x" coordinates"
            toprow=reader.next()
            axes=[map(float,toprow[1:-1]),[]]
            self.labels=toprow[0]
            data=[]
            #grab "y" coordinates and "z" values
            for row in reader:
                data.append(map(float,row[1:-1]))
                axes[1].append(float(row[0]))

        #2d splines from scipy.interpolate
        #There are lots of other toys in there, but the docs suck imo
        #interp2d might be older, but I can figure out how to use it
        #at least. XD
        self.function=interp2d(axes[0],axes[1],data,kind='cubic')
        
    def __call__(x,y):
        #This is where you'd enter in x,y and get z
        return self.function(x,y)

#should work for the fluid data (kinda), htx selection data and fluid props table.
class Propstable(filename):
    def __init__(filename):
        with open(filename) as datafile:
            reader = csv.reader(datafile)
            #get the labels
            axis=map(float,reader.next())
            data=[]
            #grab values
            for row in reader:
                for value in row:
                    try:
                        value = float(value)
                    except (ValueError):
                        pass
                data.append(row)
    #At the moment, you'll only be able to go from the left-most foward.
    self.functions=[]
    cols=zip(*data)
    for col in cols:
        self.functions.append(scipy.interpolate.interp1d(cols[0],col)
    #TODO: Make up a good way to find any xi with any xj
    def __call__(x,outval):
        i=self.axis.index(outval)
        return self.unctions[i](x)
