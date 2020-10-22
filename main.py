import pandas as pd
import math
import os
import bokeh
from bokeh.plotting import figure, output_file, show,curdoc
from bokeh.models import ColumnDataSource
from bokeh.models import Button
from bokeh.layouts import column
pd.options.mode.chained_assignment = None
from methods import *

######## call backs #########################################
def callback1(attr,old,new):
    zip1=int(new) #selected zipcode1
    df1=getSource(zip1)
    source1.data=df1
def callback2(attr,old,new):
    zip2=int(new) #selected zipcode1
    df2=getSource(zip2)
    source2.data=df2

# load data ##################################################
trimpath=('~/598A4/nyc_dash/nyctrim.csv')
cleanpath=('~/598A4/nyc_dash/dataclean.csv')
if not os.path.exists(trimpath):
    processData(trimpath,cleanpath)

df=pd.read_csv(cleanpath)

##ziplist = list containing all zipcodes
ziplist=getZip(df)
#################################################################

##allzip = list containing avg for zip0
allzip=[0]*12
for m in range(12):
    a=df[(df['Month']==m+1)]['Diff'].mean()
    allzip[m]=a


##default data source
M=list(range(1,13))
zip0=pd.DataFrame(list(zip(M,allzip)),columns=['Month','Avg'])
zip1=zip0
zip2=zip0
source0=ColumnDataSource(data=zip0)
source1=ColumnDataSource(data=zip1)
source2=ColumnDataSource(data=zip2)


##Add dropdown
[dropdown1,dropdown2]=addDropdown(ziplist)
##Handle callbacks
dropdown1.on_change('value',callback1)
dropdown2.on_change('value',callback2)

##plot line
p=figure(plot_width=600, plot_height=500,title="Average Response Time by Zipcode",x_range=(1,12),x_axis_label='Month',y_axis_label='Average Response Time')
p.line(x='Month',y='Avg',line_width=3,color="lightsteelblue",source=source1,legend_label='Average Response Time for Zipcode1')
p.line(x='Month',y='Avg',line_width=3,color="burlywood",source=source2,legend_label='Average Response Time for Zipcode2')
p.line(x='Month',y='Avg',line_width=3,color="olive",source=source0,legend_label='2020 Average Response Time')


#### add to page
curdoc().add_root(column(p,dropdown1,dropdown2))


