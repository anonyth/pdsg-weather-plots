#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#%%: import libraries
import pandas as pd
import seaborn as sns
import timeit
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

#%%: set increased ipython terminal width
pd.set_option('display.width', 200)
sns.set(style='white')

#%%: import full dataset
df_raw = pd.read_csv('data/details.csv')

#%%: clone base df with only relevant columns
df_base = df_raw[['YEAR', 'STATE', 'EVENT_TYPE', 'INJURIES_INDIRECT', \
                  # 'BEGIN_LAT', 'BEGIN_LON', 'END_LAT', 'END_LON', \
                  'DEATHS_DIRECT', 'DEATHS_INDIRECT', 'DAMAGE_PROPERTY']].copy()

#%%: clean up cases
df_base['STATE'] = df_base['STATE'].str.title()
renamed_columns = {'YEAR': 'year', 'STATE': 'state', 'EVENT_TYPE': 'event',
                   # 'BEGIN_LAT': 'beg_lat', 'BEGIN_LON': 'beg_lon', 'END_LAT': 'end_lat', 'END_LON': 'end_lon',
                   'INJURIES_INDIRECT': 'injury_ind', 'DEATHS_DIRECT': 'death_dir', 'DEATHS_INDIRECT': 'death_ind',
                   'DAMAGE_PROPERTY': 'damage'}
df_base.rename(columns=renamed_columns, inplace=True)

#%% isolate to only entries with lake effect damage
lake_effect = ['Lake-Effect Snow']
df_base = df_base[df_base['event'].isin(lake_effect)]

#%% strip abbreviating characters in damage and convert to integer
df_base['damage'] = (df_base['damage'].replace(r'[KM]+$', '', regex=True).astype(float) *\
                     df_base['damage'].str.extract(r'[\d\.]+([KM]+)', expand=False)\
                     .fillna(1)\
                     .replace(['K','M'], [10**3, 10**6]).astype(int))

#%% sort by most damaging lake-effect events
df_base.sort_values(['damage'], ascending=[False], inplace=True)

#%% change null damage reports to zeroes
df_base['damage'] = df_base['damage'].fillna(value=0)