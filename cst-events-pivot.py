#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#%%: import libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import ListedColormap

#%%: set increased ipython terminal width
pd.set_option('display.width', 200)
sns.set(style='white')

#%%: import data as discrete dataframes
df_raw = pd.read_csv('data/detail_trim2.csv')
df_loc = pd.read_csv('data/locations.csv')

#%%: clone base df with only relevant columns
df_base = df_raw[['BEGIN_DATE_TIME', 'END_DATE_TIME', 'YEAR', 'MONTH_NAME', 'BEGIN_DAY',\
                  'STATE', 'EVENT_REDUCED', 'CZ_TIMEZONE']].copy()

#%%: isolate to only CST time zones, clean up case, isolate to western states
df_base = df_base[df_base['CZ_TIMEZONE'] == 'PST']
df_base['STATE'] = df_base['STATE'].str.title()
western_states = ['Hawaii', 'California', 'Oregon', 'Washington', 'Alaska']
df_base = df_base[df_base['STATE'].isin(western_states)]

#%%: pivot into new dataframe
event_types = pd.pivot_table(df_base,\
                             index=['STATE'],\
                             values=['YEAR'],\
                             columns=['EVENT_REDUCED'], aggfunc=len, fill_value=0)

#%%: plot counts as stacked histogram
pst_types = event_types.T.plot(kind='bar', stacked=True,
                               colormap=ListedColormap(sns.color_palette("GnBu", 10)), 
                               figsize=(10,10),
                               logy=True,
                               sort_columns=True,
                               legend=True)
pst_types.set_xlabel('Raw count of stacked weather events by type in western states 1996 forward')
pst_types.set_xticklabels( ('debris', 'drought', 'flood', 'hail', 'heat', \
                            'lightning', 'other', 'rain', 'tornado', 'tropical storm', 'wave/surge', \
                            'wildfire/smoke', 'wind', 'winter storm', 'winter weather') )
L = pst_types.legend()
plt.show()