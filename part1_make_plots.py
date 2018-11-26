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
import pandas as pd
import matplotlib.pyplot as plt
from pandas.api.types import CategoricalDtype

import seaborn as sns
sns.set_style('darkgrid')
sns.set(font_scale=1.25)


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
gdp_growth     = pd.read_csv('data/gdp_growth.csv')
inflation_gdpd = pd.read_csv('data/inflation_gdpd.csv')

# add category info back to files
cat_type = CategoricalDtype(categories=['High income', 'Upper middle income', 
                                        'Lower middle income', 'Low income'], 
                            ordered=True)
for df in [gdp, pop, df_electric, df_internet, df_cellphones, log_pop, log_gdp, gdp_growth, inflation_gdpd]:
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

# create new features: delta_5yr
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
plt.title('Internet and GDP Growth')
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
sns.scatterplot(x='delta_5yr', 
                y='2016', 
                data=df_scatter, 
                hue='Income Level of Country',
                palette=['b','g','C1','r'])
plt.title('Cellphones and GDP Growth')
plt.xlabel('Cellphones Growth Rate (2011 to 2016)')
plt.ylabel('')
plt.legend(loc='lower right')
for i, label in enumerate(list(range(0,46))):
    plt.annotate(s=df_scatter['country_code'][i], 
                 xy=(df_scatter['delta_5yr'][i], df_scatter['2016'][i]),
                 size=9,
                 alpha=0.75)
plt.show()

    
### PIE CHART ###

# Plot 7 (Pie Chart for Income Levels)
income_levels = ['High income', 'Upper middle income', 
            'Lower middle income', 'Low income']
pie_df = gdp.groupby('income_level').count()
total  = sum(pie_df['country'])

plt.figure(figsize=(8,8))
plt.pie(pie_df['country'], autopct=lambda p:'{:.0f}'.format(p * total / 100), 
        labels=income_levels, 
        colors=['b','g','C1','r'],
        textprops={'fontsize': 14, 'color':'w'})
plt.title('Country Count by Income Level (2016)', fontsize=14)
plt.legend(income_levels)
plt.show()
    
   
### LOLLIPOP ###
# Plot 8 (Lollipop Plot for GDP Deflator measure of Inflation)

# inflation_gdpd[inflation_gdpd['country'] == 'Congo, Dem. Rep.'].T #check outlier
outlier_countries = ['Congo, Dem. Rep.', 'Angola', 'Somalia']
inflation_gdpd    = inflation_gdpd.drop(columns=[str(x) for x in list(range(1960,1990))])

# part 1
inflation_gdpd1        = inflation_gdpd[~inflation_gdpd['country'].isin(outlier_countries)]
inflation_gdpd1['avg'] = inflation_gdpd1.iloc[:,1:29].mean(axis=1)

plt.figure(figsize=(10,14))
my_range = list(range(1, 45))
plt.hlines(y=my_range, xmin=0, xmax=inflation_gdpd1['avg'], color='skyblue')
plt.plot(inflation_gdpd1['avg'], my_range, "o")
plt.yticks(my_range, inflation_gdpd1['country'])
plt.title('Average Inflation 1990-2016 (%) - GDP Deflator', loc='left', fontsize=14)
plt.xlabel('Inflation (%)')
plt.ylabel('Country')
plt.show()

# part 2: outlier countries
inflation_gdpd2        = inflation_gdpd[inflation_gdpd['country'].isin(outlier_countries)]
inflation_gdpd2['avg'] = inflation_gdpd2.iloc[:,1:29].mean(axis=1)

plt.figure(figsize=(10,1))
my_range2 = list(range(1, 4))
plt.hlines(y=my_range2, xmin=0, xmax=inflation_gdpd2['avg'], color='darkblue')
plt.plot(inflation_gdpd2['avg'], my_range2, "o")
plt.yticks(my_range2, inflation_gdpd2['country'])
#plt.title('Outlier Countries', loc='left', fontsize=14)
plt.xlabel('Inflation (%)')
plt.ylabel('Outlier Countries')
plt.show()













