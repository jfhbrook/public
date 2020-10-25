from dataloading import csvdata
from numpy import mean, std
from text_table import TextTable

#This little function is actually really useful!
coolant=csvdata('engine_coolant_data.csv')

#csv data's labels actually are kinda crummy for dict keys
#csv data's also not in float form :S
for keys in zip(coolant.keys(), ['input','output','flow']):
    coolant[keys[1]]=[float(r) for r in coolant[keys[0]] ]
    del coolant[keys[0]]

#enjoying TextTable ^__^
datatable = TextTable((5,'input'), (6,'output'), (5,'flow'))
for row in zip(coolant['input'],coolant['output'],coolant['flow']):
    datatable.row(str(row[0]), str(row[1]), str(row[2]))
print datatable.draw()

#Now gonna make another table with avg and std and stuff.
statstable = TextTable((7, 'field'),
                       (7, 'avg.'), 
                       (7, 'stddev'),
                       (7, 'min'),
                       (7, 'max'))
for row in coolant.keys():
    statstable.row(row, 
                  '%.3f' % mean(coolant[row]), 
                  '%.3f' % std(coolant[row]),
                  '%.1f' % max(coolant[row]),
                  '%.1f' % min(coolant[row]))
print statstable.draw()

#Now, what else do we know?
#We know that temp_c_out-temp_c_in >= 20.0, measured near baseboard
#We know the minimum return temperature should be 140.0 degrees F (60.0 C)
#We know that both fluids are 50% glycol by volume.
#From the supplied table, we may find all properties as a function of 
#temperature.

#property tables
madprops=csvdata('ethylene_glycol_0.5byvol_lut.csv')
for keys in zip(madprops.keys(), ['temperature','density','cp','k','dvisc']):
    madprops[keys[1]]=[float(r) for r in madprops[keys[0]] ]
    del madprops[keys[0]]

propstable = TextTable((7,'t'),(5,'rho'),(5,'cp'),(5,'k'),(5,'dvisc'))
for row in zip(madprops['temperature'],madprops['density'],madprops['cp'], madprops['k'], madprops['dvisc']):
    propstable.row(str(row[0]),str(row[1]),str(row[2]),str(row[3]),str(row[4]))
print propstable.draw()



