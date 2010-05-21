#!/usr/bin/env python

#experimenting with Shapely
from shapely import geometry, wkb
#also need gdal stuff--YUCK :C
from osgeo import osr, ogr
#since these things take time, I decided to have fun with progress bars.
from progressbar import ProgressBar, Percentage, Bar

"""
Prints intersections between lines and Alaskan rivers, using a bunch of
shapefile data. The lines are defined to be between a handfull of Alaskan bush villages and a subset of Trans-Alaska pipeline pumping stations.

I use it by running ./count_crossings.py > results.csv . Works great! :v
"""

#Converts shapefile information to lists of lists of shapely objects
def shp2shapely(shape_ogr):
    shape_shapely=[]
    layers=shape_ogr.GetLayerCount()
    for i in xrange(layers):
        layer=shape_ogr.GetLayer(i)
        layer_shapely=[]
        features=layer.GetFeatureCount()
        widgets=['Reading features for Layer '+str(i+1)+' of '+str(layers)+': ', Percentage(), Bar(left='[', marker=':', right=']')]
        pbar=ProgressBar(widgets=widgets, maxval=features).start()
        for j in xrange(features):
            feat=layer.GetFeature(j)
            feat_shapely=wkb.loads(feat.GetGeometryRef().ExportToWkb())
            layer_shapely.append(feat_shapely)
            pbar.update(j+1)
        pbar.finish
        shape_shapely.append(layer_shapely)
    return shape_shapely


#This wraps point data of in the form of the original towns data I had.
#The name for this class is probably too specific, but whatevs rite??
class towncoords:
    def __init__(self,filename):
        #print "Opening", filename + ':'
        shp=ogr.Open(filename)
        layer=shp.GetLayer(0) #assumes there's only one layer <_<
        layers=layer.GetFeatureCount()
        self.lookup=dict()
        widgets=['Scouting the Area: ', Percentage(), Bar(left='[', marker=':', right=']')]
        pbar=ProgressBar(widgets=widgets, maxval=layers).start()
        for i in xrange(layers):
            town=layer.GetFeature(i)
            self.lookup[town.GetField('NAME')]=wkb.loads(town.GetGeometryRef().ExportToWkb())
            pbar.update(i+1)
        pbar.finish
    def __getitem__(self,name):
        return self.lookup[name]
    def path(self, towna, townb):
        #returns a linestring using the coordinates of towns a and b
        return geometry.LineString((
               (self.lookup[towna].x, self.lookup[towna].y),
               (self.lookup[townb].x, self.lookup[townb].y)))

if __name__=="__main__":
    #File locations here.
    files={'rivers': 'shape_data/rivers_gnomonic/rivers_gnomonic',
    'towns': 'shape_data/towns_stations_gnomonic/towns_gnomonic',
    'boundary': 'shape_data/ADNR_Alaska_State_Boundary_1_250_000/alaska_250000_py'}

    townsdir=towncoords(files['towns']+'.shp')
    rivers=shp2shapely(ogr.Open(files['rivers']+'.shp'))[0]

    # Finding intersections between various pumping stations and cities
    widgets=['Finding intersections: ', Percentage(), Bar(left='[', marker=':', right=']')]
    #maxval hardcoded, fyi
    pbar=ProgressBar(widgets=widgets, maxval=50).start()
    progdex=0

    print "point a, point b, number of intersections"
    #Only uses stations 1-10 (excludes 11, 12 and the terminus), and avoids
    #towns that are too far South, since these other cases put us in danger
    #of involving oceans, which will take more thought.
    #in Barrow's case, the data for station 1 is likely garbage because, again,
    #of oceans.
    for ptb in ["Barrow", "Bethel", "Kotzebue", "Nome", "Tanana"]:
        for pta in ["station_"+str(st) for st in xrange(1,11)]:
            path=townsdir.path(pta,ptb)
            count=0
            for line in rivers:
                if line.intersects(path): 
                    count+=1
            print pta+", "+ptb+", "+str(count)
            progdex+=1
            pbar.update(progdex)
    pbar.finish
