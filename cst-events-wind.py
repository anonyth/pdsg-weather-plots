#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#%%: import libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#%%: set increased ipython terminal width
pd.set_option('display.width', 200)
sns.set(style='white')

#%%: import data as discrete dataframes
df_raw = pd.read_csv('data/detail_trim3.csv')
df_loc = pd.read_csv('data/locations.csv')

#%%: plot reduced event types
# plt.plot(df_raw.EVENT_REDUCED.value_counts())
# plt.xticks(rotation=90)

#%%: clone base df with only relevant columns
df_base = df_raw[['BEGIN_DATE_TIME', 'END_DATE_TIME', 'YEAR', 'MONTH_NAME', 'BEGIN_DAY', 'STATE', 'EVENT_REDUCED', 'CZ_TIMEZONE']].copy()

#%%: isolate to only CST time zones
df_base = df_base[df_base['CZ_TIMEZONE'] == 'CST']

#%%: total and breakout bars
wind_data = df_base.STATE[df_base['EVENT_REDUCED'] == 'Wind'].value_counts()
tornado_data = df_base.STATE[df_base['EVENT_REDUCED'] == 'Tornado'].value_counts()
event_data = df_base.STATE.value_counts()

#%%: plotting bar chart
plt.figure(figsize=(8,8))
sns.barplot(event_data, event_data.index, color='#333333')
sns.barplot(wind_data, wind_data.index, color='#666666')
sns.barplot(tornado_data, tornado_data.index, color='#999999')
plt.legend()