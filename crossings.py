#!/usr/bin/env python

#experimenting with Shapely
from shapely import geometry, wkb
#also need gdal stuff--YUCK :C
from osgeo import osr, ogr
#since these things take time...
from progressbar import ProgressBar, Percentage, Bar


#Converts shapefile information to lists of lists of shapely objects
def shp2shapely(filename):
    print "Opening", filename + ':'
    shape_ogr=ogr.Open(filename)
    shape_shapely=[]
    layers=shape_ogr.GetLayerCount()
    for i in xrange(layers):
        print "Layer ", i+1, ' of ', layers, ': '
        layer=shape_ogr.GetLayer(i)
        layer_shapely=[]
        features=layer.GetFeatureCount()
        widgets=['Reading features:', Percentage(), Bar(left='[', marker=':', right=']')]
        pbar=ProgressBar(widgets=widgets, maxval=features).start()
        for j in xrange(features):
            feat=layer.GetFeature(j)
            feat_shapely=wkb.loads(feat.GetGeometryRef().ExportToWkb())
            layer_shapely.append(feat_shapely)
            pbar.update(j+1)
        pbar.finish
        shape_shapely.append(layer_shapely)
    print "Done. \n"
    return shape_shapely

#Grab coords for various towns
class towncoords:
    def __init__(self,filename):
        print "Opening", filename + ':'
        shp=ogr.Open(filename)
        layer=shp.GetLayer(0) #assumes there's only one layer <_<
        layers=layer.GetFeatureCount()
        self.lookup=dict()
        widgets=['Scouting the Area:', Percentage(), Bar(left='[', marker=':', right=']')]
        pbar=ProgressBar(widgets=widgets, maxval=layers).start()
        for i in xrange(layers):
            town=layer.GetFeature(i)
            self.lookup[town.GetField('NAME')]=wkb.loads(town.GetGeometryRef().ExportToWkb())
            pbar.update(i+1)
        pbar.finish
        print "Done. \n"
    def __getitem__(self,name):
        return self.lookup[name]
    def path(self, towna, townb):
        #actually kind of a crummy way to have to do it, imho :(
        return geometry.LineString(((self.lookup[towna].x, self.lookup[towna].y),
                              (self.lookup[townb].x, self.lookup[townb].y)))    
        
#Shapely's wasn't working. Whatever.
#input a list of polygons to unionize.
def cascaded_union(polygons):
    tot_area=polygons
    widgets=['Unionizing:', Percentage(), Bar(left='[', marker=':', right=']')]
    pbar=ProgressBar(widgets=widgets, maxval=len(polygons)).start()
    for i in xrange(len(polygons)-1):
        tot_area=tot_area.union(polygons[i+1])
        pbar.update(i+1)
    pbar.finish
    return tot_area


#where files are :6
files={'rivers': 'shape_data/ADNR_Rivers_1_1_000_000_Line/akrivers_ln_83',
'towns': 'shape_data/ADNR_Towns_and_Villages-1/town',
'boundary': 'shape_data/ADNR_Alaska_State_Boundary_1_250_000/alaska_250000_py'}

#seems to have worked out fine
rivers=shp2shapely(files['rivers']+'.shp')[0]
#boundary=shp2shapely(files['boundary']+'.shp')[0]
townsdir=towncoords(files['towns']+'.shp')

#might work for these too?
#rivers=cascaded_union(rivers)

print "Producing a path between Fairbanks and Nome"
path=townsdir.path("Fairbanks","Nome")

widgets=['Finding intersections:', Percentage(), Bar(left='[', marker=':', right=']')]
crossings=[]
numcrossings=0
pbar=ProgressBar(widgets=widgets, maxval=len(rivers)).start()
for i, linestring in enumerate(rivers):
    if linestring.intersects(path): numcrossings+=1
    crossings.append(linestring.intersection(path))
    pbar.update(i+1)
pbar.finish

print "This path has", numcrossings, "stream crossings."
