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
plt.plot(df_raw.EVENT_REDUCED.value_counts())
plt.xticks(rotation=90)

#%%: clone base df with only relevant columns
df_base = df_raw[['BEGIN_DATE_TIME', 'END_DATE_TIME', 'YEAR', 'MONTH_NAME', 'BEGIN_DAY',\
                  'STATE', 'EVENT_REDUCED', 'CZ_TIMEZONE']].copy()

#%%: isolate to only CST time zones
df_base = df_base[df_base['CZ_TIMEZONE'] == 'CST']

#%%: total and breakout bars
data_wind = df_base.STATE[df_base['EVENT_REDUCED'] == 'Wind'].value_counts()
data_tornado = df_base.STATE[df_base['EVENT_REDUCED'] == 'Tornado'].value_counts()
data_heat = df_base.STATE[df_base['EVENT_REDUCED'] == 'Heat'].value_counts()
data_drought = df_base.STATE[df_base['EVENT_REDUCED'] == 'Drought'].value_counts()
data_events = df_base.STATE.value_counts()

#%%: plotting bar chart, a visually flawed approach
# Does not account for event types that have more values but are drawn after earlier types with less

plt.figure(figsize=(10,8))
sns.barplot(x=data_events, y=data_events.index, color='#666666')
            
layer_wind = sns.barplot(x=data_wind, y=data_wind.index, color='#047495')
layer_tornado = sns.barplot(x=data_tornado, y=data_tornado.index, color='#0485d1')
layer_heat = sns.barplot(x=data_heat, y=data_heat.index, color='#8c000f')
layer_drought = sns.barplot(x=data_drought, y=data_drought.index, color='#8c000f')

lgd_total = plt.Rectangle((0,0),1,1, fc='#666666', edgecolor = 'none')
lgd_wind = plt.Rectangle((0,0),1,1, fc='#047495', edgecolor = 'none')
lgd_tornado = plt.Rectangle((0,0),1,1, fc='#0485d1', edgecolor = 'none')
lgd_heat = plt.Rectangle((0,0),1,1, fc='#8c000f', edgecolor = 'none')
lgd_drought = plt.Rectangle((0,0),1,1, fc='#a83c09', edgecolor = 'none')

l = plt.legend([lgd_total, lgd_wind, lgd_tornado, lgd_heat, lgd_drought],\
               ['total events', 'wind', 'tornado', 'heat', 'drought'],\
               loc=4, ncol = 1, prop={'size':10})

l.draw_frame(False)
