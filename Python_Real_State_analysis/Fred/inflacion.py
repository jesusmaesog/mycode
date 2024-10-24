from tkinter import Label
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from fredapi import Fred

plt.style.use('fivethirtyeight')
pd.set_option('display.max_columns', 200)
color_palet = plt.rcParams['axes.prop_cycle'].by_key()['color']

fred_key = '9bf49a5620fc9111d8c2fad585e5f829'

fred = Fred(api_key= fred_key)

inflacion_search = fred.search('CPIAUCSL')
inflacion_suby_search = fred.search('CPILFESL')

usa_inf = fred.get_series(series_id='CPIAUCSL', observation_start= '2021-08-01' , observation_end= '2022-08-01')
print(usa_inf)
usa_inf_suby = fred.get_series(series_id='CPILFESL', observation_start= '2021-08-01' , observation_end= '2022-08-01')

print(usa_inf.head(20))

fig, ax = plt.subplots() #esto sirver para crear tantos gráficos como quiera
usa_inf.plot(ax=ax, label= 'general inflation', linewidth=1, marker= 'D', markersize= '5', figsize=(9,6), grid= True)
usa_inf_suby.plot(ax=ax, label= 'inflation (non food, energy)', color='red', linewidth=1, marker= 'o', markersize= '5', figsize=(9,6), grid= True)
ax.legend(['general inflation', 'inflation (non food, energy)'], loc=0)
plt.title('USA inflation 1947-2022')
fig.set_size_inches(9, 9)

plt.show()