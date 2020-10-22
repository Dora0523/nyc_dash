import pandas as pd
import math
import os
import bokeh
from bokeh.plotting import figure, output_file, show,curdoc
from bokeh.models import ColumnDataSource
from bokeh.models import Select
from bokeh.layouts import widgetbox
from bokeh.layouts import column
pd.options.mode.chained_assignment = None

def processData(trimpath,cleanpath):
    df0=pd.read_csv(trimpath, usecols=[1,2,8,19],names=['Created Date','Closed Date','Incident Zip','Status'])
    df0=df0[df0['Status']=="Closed"]

    #drop NA
    df0.dropna(inplace=True)
    

    #add column of response hours,
    df0['Month']=df0['Closed Date'].str.slice(0,2)

    df0['Created Date']=pd.to_datetime(df0['Created Date'],format='%m/%d/%Y %I:%M:%S %p')
    df0['Closed Date']=pd.to_datetime(df0['Closed Date'],format='%m/%d/%Y %I:%M:%S %p')
    df0['Diff']=(df0['Closed Date']-df0['Created Date'])/pd.Timedelta(hours=1)
    df0.drop(['Created Date','Closed Date','Status'],axis=1,inplace=True)

    #remove negative duration
    df0=df0[df0['Diff']>=0]

    #save processed data in 'dataclean.csv'
    df0.to_csv(cleanpath, index=False)
##collect all zipcodes
def getZip(df):
    zipcodeLst=[]
    for zip in df['Incident Zip']:
        if not (zip in zipcodeLst):
            zipcodeLst.append(int(zip))
    return zipcodeLst
        
##Create a Average table
def getSource(z):
    cleanpath=('~/598A4/nyc_dash/dataclean.csv')
    dfzip=pd.read_csv(cleanpath)

    dfzip=dfzip[dfzip['Incident Zip']==z]
    M=range(1,13)
    Avg=dfzip.groupby("Month")["Diff"].mean() #mean zip by month
    zipdf=pd.DataFrame(list(zip(M,Avg)),columns=['Month','Avg'])
    return zipdf

def addDropdown(allzip):
    zipcode = [str(z) for z in allzip]
    dropdown1 = Select(title="Zipcode 1", value = "1", options = [""] + zipcode)
    dropdown2 = Select(title="Zipcode 2", value = "", options = [""] + zipcode)

    return [dropdown1,dropdown2]








