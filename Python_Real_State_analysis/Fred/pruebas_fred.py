from tkinter import Label
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from fredapi import Fred

plt.style.use('fivethirtyeight')
pd.set_option('display.max_columns', 200)
color_palet = plt.rcParams['axes.prop_cycle'].by_key()['color']

fred_key = 'lorem ipsum'

fred = Fred(api_key= fred_key)

#####################################################################################

# Código para pruebas

general_search = fred.search('MSACSR', filter= ('frequency', 'Monthly'))
general_query = general_search.query('seasonal_adjustment == "Seasonally Adjusted"').shape
print(general_search)

#####################################################################################


#fig, ax = plt.subplots() #esto sirver para crear tantos gráficos como quiera

# usa_new_house = fred.get_series(series_id='HOUST')
# usa_new_house.plot(ax=ax, label= 'Units Started', color=color_palet[1], linewidth=1)
# ax.legend(['Units Started'], loc=0)
# plt.title('USA New Privately-Owned Housing Units Started')

#usa_new_house_delivery = fred.get_series(series_id= 'MSACSR')
#print(usa_new_house_delivery.describe())


#usa_new_house_delivery.plot(ax=ax, label= 'Month Supply', color='Darkgreen', linewidth=1)
# ax.legend(['Month Supply'], loc=0)
# plt.title('Monthly Supply of New Houses in the United States')


#plt.show()



#Aquí estoy intentando formatear el eje x pero creo que no sale porque tendría que casar con los valores del dataframe
# l =np.arange(1920,2023)
# l1 = str(np.arange(1920,2023))
# lenx = range(len(l))