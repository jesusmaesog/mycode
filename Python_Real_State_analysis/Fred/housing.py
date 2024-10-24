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

fed_rates_search = fred.search('FEDFUNDS')
mortg30_search = fred.search('MORTGAGE30US')
housing_price = fred.search('CSUSHPISA')
housing_inventory = fred.search('HOSINVUSM495N')
newhousing_stock = fred.search('MSACSR', filter= ('frequency', 'Monthly'))

usa_fed_rates = fred.get_series(series_id='FEDFUNDS', observation_start= '2015-01-01' , observation_end= '2022-08-01')
usa_mortg30 = fred.get_series(series_id='MORTGAGE30US', observation_start= '2015-01-01' , observation_end= '2022-08-01')
usa_newhousing_started = fred.get_series(series_id='HOUST', observation_start= '2020-04-01' , observation_end= '2022-08-01')
usa_housing_prices = fred.get_series(series_id='CSUSHPISA', observation_start= '2020-04-01' , observation_end= '2022-08-01')
usa_housing_sales = fred.get_series(series_id='HOSINVUSM495N', observation_start= '2020-04-01' , observation_end= '2022-08-01')
usa_newhousing_stock = fred.get_series(series_id='MSACSR', observation_start= '2020-04-01' , observation_end= '2022-08-01')

############################################################################################################################

# fig, ax = plt.subplots()
# fig.set_size_inches(15, 15)
# ax = plt.subplot()
# usa_fed_rates.plot(ax=ax, label= 'USA Fed Rates', linewidth=1)
# usa_mortg30.plot(ax=ax, label= 'USA Mortgate Rates', color=color_palet[1], linewidth=1)
# ax.legend(['USA Fed Rates', 'USA Mortgate Rates'], loc=0)
# plt.xlim('2014-12-01', '2022-09-01' )
# plt.title('Fed Rates vs. Mortgate 30Y Rates. Source: fred.stlouisfed.org')
# plt.savefig("FED_Rates_vs_Mortg30_Rates.png", dpi=300)


################################################################################################################

# fig, ax = plt.subplots()
# fig.set_size_inches(15, 15)
# ax = plt.subplot()
# usa_newhousing_started.plot(ax=ax, label= 'nº of units. Source: fred.stlouisfed.org', linewidth=1, marker= 'D', markersize= '5', figsize=(9,6), grid= True)
# plt.title('New Private Housing started')
# plt.legend(['thousand of units started. Source: fred.stlouisfed.org'], loc= 4)
# plt.xlim('2020-03-01', '2022-09-01' )
# plt.savefig("US_Private_Houses_Started.png", dpi=300)

#####################################################################################################################

# fig, ax = plt.subplots()
# fig.set_size_inches(15, 15)
# ax = plt.subplot()
# usa_housing_prices.plot(ax=ax, label= 'nº of units. Source: fred.stlouisfed.org', color= 'red', linewidth=1, marker= 'D', markersize= '5', figsize=(9,6), grid= True)
# plt.title('S&P/Case-Shiller U.S. National Home Price Index')
# plt.legend(['thousand of US$. Source: fred.stlouisfed.org'], loc= 4)
# plt.xlim('2020-03-01', '2022-09-01' )
# plt.savefig("US_National_Price_Index.png", dpi=300)

#######################################################################################################################

fig, ax = plt.subplots()
fig.set_size_inches(15, 15)
ax = plt.subplot()
plt.ylim(0, 1400000)
usa_housing_sales.plot(ax=ax, label= 'nº of units. Source: fred.stlouisfed.org', color= 'orange', linewidth=1, marker= 'D', markersize= '5', figsize=(9,6), grid= True)
plt.title('Existing Home Sales')
plt.xlim('2021-08-01', '2022-09-01' )
plt.legend(['Source: fred.stlouisfed.org'], loc= 4)
plt.ylabel('Existing units sold (K)')
plt.savefig("Existing_Home_Sales.png", dpi=300)

########################################################################################################################

# fig, ax = plt.subplots()
# fig.set_size_inches(15, 15)
# ax = plt.subplot()
# usa_newhousing_stock.plot(ax=ax, label= 'house stock in months. Source: fred.com', linewidth=1, marker= 'D', markersize= '4', color= 'darkgreen', figsize=(9,6), grid= True)
# plt.title('Housing Stock vs. Housing Sales')
# plt.legend(['house stock in months. Source: fred.stlouisfed.org'], loc= 4)
# plt.xlim('2020-03-01', '2022-09-01' )
# plt.savefig("House_stock_in_months.png", dpi=300)
