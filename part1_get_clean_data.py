#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 21:09:08 2018

@author: kgedney
"""
# this file imports the data, reshapes the data, and does quality checks and EDA


#- set working directory
import os
project_root = '/Users/kgedney/Documents/georgetown/anly503/project/'
os.chdir(project_root)

# prep
import io
import wbdata
import zipfile
import scipy
import requests
import unidecode
import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
from pandas.api.types import CategoricalDtype

import seaborn as sns
sns.set()

# import filters
subs_african_countries = ['Angola',	'Benin', 'Botswana',
                          'Burkina Faso', 'Burundi', 'Cabo Verde',
                          'Cameroon', 'Central African Republic',
                          'Chad', 'Comoros', 'Congo, Dem. Rep.', 'Congo, Rep.',
                          "Cote d'Ivoire", 'Equatorial Guinea', 'Eritrea','Ethiopia',
                          'Gabon', 'Gambia, The', 'Ghana', 'Guinea', 
                          'Guinea-Bissau', 'Kenya', 'Lesotho', 'Liberia',
                          'Madagascar', 'Malawi', 'Mali', 'Mauritania', 
                          'Mauritius', 'Mozambique', 'Namibia', 'Niger',         
                          'Nigeria', 'Rwanda', 'Sao Tome and Principe', 
                          'Senegal', 'Seychelles', 'Sierra Leone', 'Somalia',
                          'South Africa', 'South Sudan','Sudan', 
                          'Swaziland', 'Tanzania','Togo', 
                          'Uganda', 'Zambia', 'Zimbabwe']
 
country_codes = dict({'Angola': 'AO',	'Benin': 'BJ', 'Botswana': 'BW', 'Burkina Faso':'BF', 'Burundi':'BI', 
'Cabo Verde':'CV','Cameroon'  :'CM', 'Central African Republic':'CF','Chad'   :'TD', 'Comoros':'KM', 
'Congo, Dem. Rep.': 'CD', 'Congo, Rep.': 'CG', "Cote d'Ivoire" : 'CI', 'Equatorial Guinea' : 'GQ', 'Eritrea': 'ER',
'Ethiopia':'ET','Gabon':'GA', 'Gambia, The':'GM', 'Ghana':'GH', 'Guinea':'GN', 'Guinea-Bissau':'GW',
'Kenya':   'KE', 'Lesotho': 'LS', 'Liberia':  'LR','Madagascar': 'MG', 'Malawi': 'MW', 'Mali': 'ML', 
'Mauritania': 'MR', 'Mauritius' : 'MU', 'Mozambique': 'MZ' , 'Namibia': 'NM', 'Niger': 'NE','Nigeria': 'NG', 
'Rwanda': 'RW', 'Sao Tome and Principe': 'ST', 'Senegal':'SN', 'Seychelles': 'SC', 'Sierra Leone': 'SL', 'Somalia': 'SO',
'South Africa' : 'ZA', 'South Sudan' : 'SS','Sudan': 'SD', 'Swaziland': 'SZ', 'Tanzania': 'TZ',
'Togo': 'TG', 'Uganda': 'UG', 'Zambia': 'ZM', 'Zimbabwe': 'ZW'})

# import country income level data from world bank
url = 'http://api.worldbank.org/v2/en/indicator/AG.LND.AGRI.ZS?downloadformat=csv'
r   = requests.get(url)
zf  = zipfile.ZipFile(io.BytesIO(r.content))
zf.extractall('data/wb_metadata')

df_meta  = pd.read_csv('data/wb_metadata/Metadata_Country_API_AG.LND.AGRI.ZS_DS2_en_csv_v2_10136399.csv', encoding = 'utf-8')
df_meta['TableName'] = df_meta['TableName'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
df_meta       = df_meta[df_meta['TableName'].isin(subs_african_countries)]
income_levels = dict(zip(df_meta['TableName'], df_meta['IncomeGroup']))


# helper functions
def get_df_by_year(indicator, indicator_name):
    indicator = {indicator: indicator_name}
    df = wbdata.get_dataframe(indicator, convert_date=False).reset_index()
    df = df[df['country'].isin(subs_african_countries)]
    df = df.pivot(index='country', columns='date', values=indicator_name)
    return(df)

def get_flat_df_by_year(indicator, indicator_name):
    indicator = {indicator: indicator_name}
    df = wbdata.get_dataframe(indicator, convert_date=False).reset_index()
    df = df[df['country'].isin(subs_african_countries)]
    return(df)

# load datasets (gdp, pop, df_internet, df_electric)
gdp           = get_df_by_year('NY.GDP.MKTP.CD', 'gdp')
gdp_growth    = get_df_by_year('NY.GDP.MKTP.KD.ZG', 'gdp_growth')
pop           = get_df_by_year('SP.POP.TOTL', 'total_pop')
df_electric   = get_df_by_year('1.1_ACCESS.ELECTRICITY.TOT', 'electricity_access')
df_internet   = get_df_by_year('IT.NET.USER.ZS', 'internet')
df_cellphones = get_df_by_year('IT.CEL.SETS.P2', 'cellphones')
# df_hospitals  = get_df_by_year('SH.MED.BEDS.ZS', 'hospital_beds')
# df_doctors    = get_df_by_year('SH.MED.PHYS.ZS', 'doctors')
gdp_growth_flat = get_flat_df_by_year('NY.GDP.MKTP.KD.ZG', 'gdp_growth')

# log values
log_gdp = gdp.copy()
for year in gdp.columns[1:-1]:
    log_gdp[year] = np.log10(log_gdp[year])

log_pop = pop.copy()
for year in pop.columns[1:-1]:
    log_pop[year] = np.log10(log_pop[year])
    
# map country code to all datasets
for df in [gdp, pop, df_electric, df_internet, df_cellphones, log_pop, log_gdp, gdp_growth, gdp_growth_flat]:
    df['country_code'] = df.index.map(country_codes)

# map income level to all datasets
cat_type = CategoricalDtype(categories=['High income', 'Upper middle income', 'Lower middle income', 'Low income'], 
                            ordered=True)
for df in [gdp, pop, df_electric, df_internet, df_cellphones, log_pop, log_gdp, gdp_growth, gdp_growth_flat]:
    df['income_level'] = df.index.map(income_levels).astype(cat_type)



###################
# explore datasets, run stats

# check how many missing values in each df
gdp.isnull().sum().sum()
pop.isnull().sum().sum()
df_electric.isnull().sum().sum()
df_cellphones.isnull().sum().sum()

# subset on 2016 data
df_2016 = pd.DataFrame({
    'log_pop'      : log_pop['2016'],
    'log_gdp'      : log_gdp['2016'],
    'electric'     : df_electric['2016'],
    'internet'     : df_internet['2016'],
    'cellphones'   : df_cellphones['2016'],
  #  'hospital_beds': df_hospitals['2016'],
  #  'doctors'      : df_doctors['2016'],
    'income_level' : df_cellphones['income_level']
})

# check missing values
df_2016.isnull().sum().sum()

# check correlations
df_2016.corr()

# plot 1: run pairplot
tmp = df_2016.copy()
tmp = tmp[tmp.isnull().sum(axis=1) == 0]
sns.pairplot(tmp)

# plot 2: run boxplots
df_2016.describe()
df_2016.boxplot(column=['electric', 'internet', 'cellphones'])

# check ranges
# the range for infrastructure indicators is high
years = [str(x) for x in list(range(1990,2017))]
for year in years:
    print(year, round(df_electric[year].min(),2), round(df_electric[year].max(),2))

# plot 3: run 2016 data by income level
print(df_2016.groupby('income_level').count())
df_avg = df_2016.groupby('income_level').mean()
df_avg = df_avg.T
df_avg.plot(kind='bar', figsize=(8,5), title='Indicators by Income Level of Country',
            color=['b','g','C1','r'])

# check for statistical significance among income-levels
for colname in df_2016.columns[2:-1]:
    high   = df_2016[colname][df_2016['income_level'] =='High income']
    upmid  = df_2016[colname][df_2016['income_level'] =='Upper middle income']
    lowmid = df_2016[colname][df_2016['income_level'] =='Lower middle income']
    low    = df_2016[colname][df_2016['income_level'] =='Low income']
    
    _, p = scipy.stats.f_oneway(high, upmid, lowmid, low)
    print(colname + ': ', p)


# check growth rates since 2000 of key indicators (all but docs, elec have grown across all countries)
for df in [gdp, pop, df_electric, df_internet, df_cellphones]:
    df['delta_2000'] = df['2016'] - df['2000']
    print(df['delta_2000'].min())

# check countries for which electricity has decreased
df_electric['delta_2000']



#################
# save datasets
gdp.to_csv('data/gdp.csv')
pop.to_csv('data/pop.csv')
df_electric.to_csv('data/electric.csv')
df_internet.to_csv('data/internet.csv')
df_cellphones.to_csv('data/cellphones.csv')
#df_hospitals.to_csv('data/hospitals.csv')
#df_doctors.to_csv('data/doctors.csv')

log_gdp.to_csv('data/log_gdp.csv')
log_pop.to_csv('data/log_pop.csv')

gdp_growth.to_csv('data/gdp_growth.csv')
gdp_growth_flat.to_csv('data/gdp_growth_flat.csv')

## datasets used but not imported in python
# https://data.worldbank.org/indicator/NY.GDP.MKTP.KD.ZG
# 










