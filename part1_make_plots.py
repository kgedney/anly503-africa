#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 22:07:06 2018

@author: kgedney
"""
# set working directory
import os
project_root = '/Users/kgedney/Documents/georgetown/anly503/project/'
os.chdir(project_root)

# prep
import wbdata
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas.api.types import CategoricalDtype

import seaborn as sns
sns.set_style("whitegrid")


# load data
gdp           = pd.read_csv('data/gdp.csv')
pop           = pd.read_csv('data/pop.csv')
log_gdp       = pd.read_csv('data/log_gdp.csv')
log_pop       = pd.read_csv('data/log_pop.csv')
df_electric   = pd.read_csv('data/electric.csv')
df_internet   = pd.read_csv('data/internet.csv')
df_cellphones = pd.read_csv('data/cellphones.csv')
#df_hospitals  = pd.read_csv('data/hospitals.csv')
#df_doctors    = pd.read_csv('data/doctors.csv')
gdp_growth    = pd.read_csv('data/gdp_growth.csv')

# add category info back to files
cat_type = CategoricalDtype(categories=['High income', 'Upper middle income', 'Lower middle income', 'Low income'], 
                            ordered=True)
for df in [gdp, pop, df_electric, df_internet, df_cellphones, log_pop, log_gdp, gdp_growth]:
    df['income_level'] = df['income_level'].astype(cat_type)



### HEATMAPS ###

# Plot 1 (Heat Map - Internet): 
df_heat = df_internet.set_index('country')
df_heat = df_heat.drop(columns=[str(x) for x in list(range(1960,2000))])
df_heat = df_heat.drop(columns=['2017', 'country_code', 'income_level', 'delta_2000'])

plt.figure(figsize=(12,12))
sns.heatmap(df_heat, linewidths=.5, cmap='Reds')
plt.title('Population Using Internet (%)')
plt.ylabel('Country')
plt.xlabel('Year')
plt.show()


# Plot 2 (Heat Map - Cellphones):
df_heat = df_cellphones.set_index('country')
df_heat = df_heat.drop(columns=[str(x) for x in list(range(1960,2000))])
df_heat = df_heat.drop(columns=['2017', 'country_code', 'income_level', 'delta_2000'])

plt.figure(figsize=(12,12))
sns.heatmap(df_heat, linewidths=.5, cmap="Blues")
plt.title('Cellphone Subscriptions (per 100)')
plt.ylabel('Country')
plt.xlabel('Year')
plt.show()  
    
df_heat['2016']

# Plot 3 (Heatmap - Electricity)
df_heat = df_electric.set_index('country')
df_heat = df_heat.drop(columns=[str(x) for x in list(range(1990,2000))])
df_heat = df_heat.drop(columns=['country_code', 'income_level','delta_2000'])

plt.figure(figsize=(12,12))
sns.heatmap(df_heat, linewidths=.5, cmap='Greens')
plt.title('Population with Electricty Access (%)')
plt.ylabel('Country')
plt.xlabel('Year')
plt.show()




### SCATTERPLOTS ###

# create new feature: delta_5yr
df_electric['delta_20yr'] = ((df_electric['2016'] - df_electric['1996']) / df_electric['2011']) *100
df_internet['delta_5yr'] = ((df_internet['2016'] - df_internet['2011']) / df_internet['2011']) *100
df_cellphones['delta_5yr'] = ((df_cellphones['2016'] - df_cellphones['2011']) / df_cellphones['2011']) *100


# Plot 4 (Growth in Internet vs. Growth in GDP):
df_scatter = pd.concat([df_internet['country_code'], 
                        df_internet['income_level'], 
                        df_internet['delta_5yr'], 
                        gdp_growth['2016']], axis=1)
df_scatter = df_scatter.rename(columns={'income_level': 'Income Level of Country'})
print(df_scatter['delta_5yr'].corr(df_scatter['2016']))
  
plt.figure(figsize=(12,8))
sns.scatterplot(x='delta_5yr', 
                y='2016', 
                data=df_scatter, 
                hue='Income Level of Country', 
                palette=['b','g','C1','r'])
plt.title('Infrastructure and GDP Growth')
plt.xlabel('Internet Growth Rate (2011 to 2016)')
plt.ylabel('GDP Growth Rate (2016)')
plt.legend(loc='lower right')
for i, label in enumerate(list(range(0,46))):
    plt.annotate(s=df_scatter['country_code'][i], 
                 xy=(df_scatter['delta_5yr'][i], df_scatter['2016'][i]),
                 size=9,
                 alpha=0.75)
plt.show()



# Plot 5 (Growth in Cellphones vs. Growth in GDP):
df_scatter = pd.concat([df_cellphones['country_code'], 
                        df_cellphones['income_level'], 
                        df_cellphones['delta_5yr'], 
                        gdp_growth['2016']], axis=1)
df_scatter = df_scatter.rename(columns={'income_level': 'Income Level of Country'})
print(df_scatter['delta_5yr'].corr(df_scatter['2016']))
  
plt.figure(figsize=(12,8))
sns.scatterplot(x='delta_5yr', y='2016', 
                data=df_scatter, 
                hue='Income Level of Country',
                palette=['b','g','C1','r'])
plt.title('Infrastructure and GDP Growth')
plt.xlabel('Cellphones Growth Rate (2011 to 2016)')
plt.ylabel('GDP Growth Rate (2016)')
plt.legend(loc='lower right')
for i, label in enumerate(list(range(0,46))):
    plt.annotate(s=df_scatter['country_code'][i], 
                 xy=(df_scatter['delta_5yr'][i], df_scatter['2016'][i]),
                 size=9,
                 alpha=0.75)
plt.show()

    

    
    
    
    
### old matplotlib code ###
#plt.figure(figsize=(8,4))
#plt.scatter(df_cellphones['delta_5yr'], gdp_growth['2016'], alpha=0.6)
#plt.ylabel('GDP Growth Rate (2016)')
#plt.xlabel('Cellphone 5-Yr Growth Rate (2011 to 2016)')
#
#for i, label in enumerate(list(range(0,46))):
#    plt.annotate(s=gdp_growth['country_code'][i], 
#                 xy=(df_cellphones['delta_5yr'][i], gdp_growth['2016'][i]),
#                 size=9,
#                 alpha=0.75)
#plt.show()
#
#sns.scatterplot()














