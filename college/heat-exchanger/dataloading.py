#import xlrd #, xlwt
import csv

# TODO: Split into own project, think of good names
# TODO: Define some kinda nice table class?

###data input

#Reads in data points
#TODO: docstring,doctest,wrap in with/as construct
#TODO: Some action for "Name (units)"--> "name" and [data]*units
def csvdata(filename):
    with csv.reader(open(filename)) as datareader:
        titles=datareader.next()
        datalists=[]
        for row in datareader:
            datalists.append(row)
        #some outrageous shit >_<
        return dict(zip(titles,
                        [list(tupl) for tupl in zip(*datalists)]))

###data output

#TODO: Add ascii table action--use TextTable? PROBABLY

#data LaTeX formatting
#copy-paste or pipe
#TODO: docstring,doctest,make works with csvdata()-type data arrangement
#TODO: Replace with interface to latex::table using
#http://www.boriel.com/2007/01/21/calling-perl-from-python/
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
#TODO: test,docstring,doctest,make works with csvdata()-type data arrangement
def exceltable(columns,titles,filename):
    workbook=xlwt.Workbook()
    sheet=workbook.add_sheet("Some Table or Other")
    for i, entry in enumerate(titles):
        sheet.write(i,0, entry, xlwt.easyxf('bold on'))
    for j, column in enumerate(columns):
        for i, entry in enumerate(column):
            sheet.write(i,j,entry)
    workbook.save(filename)
