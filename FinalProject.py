#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 16:55:47 2020

@author: hendrasetiawan
"""




import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import kde
import matplotlib.pyplot as plt


#step one (time selection)
#read the data and slice the data to point of time we want to analyze
def readandpick(x,y,z):
    global dataunclean
    global datasettargetyear
    dataunclean=pd.read_csv('sumberdata.csv',index_col=0)
    datasettargetyear='datasettargetyear'
    globals()[datasettargetyear+x]=dataunclean[[x,'Indicator Name']]
    globals()[datasettargetyear+y]=dataunclean[[y,'Indicator Name']]
    globals()[datasettargetyear+z]=dataunclean[[z,'Indicator Name']]
    return()


readandpick('1997','1998','1999')
readandpick('2007','2008','2009')


def countryselectiondashboard(x,y,z,u,v,w):
    #global selectedcountries
    selectedcountries='selectedcountries'
    with open("listofcountry.txt") as f:
            inventories = f.readlines()
            countryname=[item.strip() for item in inventories]   
    globals()[selectedcountries+x]=datasettargetyear1997.loc[datasettargetyear1997.index.isin(countryname)] 
    globals()[selectedcountries+y]=datasettargetyear1998.loc[datasettargetyear1998.index.isin(countryname)]
    globals()[selectedcountries+z]=datasettargetyear1999.loc[datasettargetyear1999.index.isin(countryname)]
    globals()[selectedcountries+u]=datasettargetyear2007.loc[datasettargetyear2007.index.isin(countryname)]
    globals()[selectedcountries+v]=datasettargetyear2008.loc[datasettargetyear2008.index.isin(countryname)]
    globals()[selectedcountries+w]=datasettargetyear2009.loc[datasettargetyear2009.index.isin(countryname)] 

countryselectiondashboard('1997','1998','1999','2007','2008','2009')

selectedcountries1997['Year'] = '1997'
selectedcountries1998['Year'] = '1998'
selectedcountries1999['Year'] = '1999'
selectedcountries2007['Year'] = '2007'
selectedcountries2008['Year'] = '2008'
selectedcountries2009['Year'] = '2009'


selectedcountries1997=selectedcountries1997.rename(columns={"1997":"Value"})
selectedcountries1998=selectedcountries1998.rename(columns={"1998":"Value"})
selectedcountries1999=selectedcountries1999.rename(columns={"1999":"Value"})
selectedcountries2007=selectedcountries2007.rename(columns={"2007":"Value"})
selectedcountries2008=selectedcountries2008.rename(columns={"2008":"Value"})
selectedcountries2009=selectedcountries2009.rename(columns={"2009":"Value"})


selectedvariableofinterest='selectedvariableofinterest'
indis='indis'
with open('FinancialSystemPackage.txt') as f:
    vinterests = f.readlines()
    vinterestname=[vinterest.strip() for vinterest in vinterests]   
    selectedcountries1997=selectedcountries1997.loc[selectedcountries1997['Indicator Name'].isin(vinterestname)]
    selectedcountries1998=selectedcountries1998.loc[selectedcountries1998['Indicator Name'].isin(vinterestname)]
    selectedcountries1999=selectedcountries1999.loc[selectedcountries1999['Indicator Name'].isin(vinterestname)]
    selectedcountries2007=selectedcountries2007.loc[selectedcountries2007['Indicator Name'].isin(vinterestname)]
    selectedcountries2008=selectedcountries2008.loc[selectedcountries2008['Indicator Name'].isin(vinterestname)]
    selectedcountries2009=selectedcountries2009.loc[selectedcountries2009['Indicator Name'].isin(vinterestname)]



dashboardready = pd.concat([selectedcountries1997, selectedcountries1998,selectedcountries1999,selectedcountries2007,selectedcountries2008,selectedcountries2009], sort=False)
dashboardready .to_csv("dashboardready1.csv")

#investigate the price of banking stock when crisis happens using API

# quandl for financial data
import quandl
# pandas for data manipulation
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.dates import MonthLocator, DateFormatter
quandl.ApiConfig.api_key = 'zNSVkNFKh_WNvSTkbvb9'
# Retrieve Morgan Stanly data from Quandl
morgan= quandl.get('WIKI/MS')
# Retrieve the Citigroup data from Quandl
gm = quandl.get('WIKI/C')
gm.head(5)
fig, ax = plt.subplots()
ax.plot(morgan.index, morgan['Open'])

yy=dataunclean.drop(dataunclean.columns[10:30], axis=1, inplace=True)
