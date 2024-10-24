#!/usr/bin/env python
# *-* coding: utf-8 es-es **

from pprint import pprint
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import csv
import locale
from currencies import Currency

df = pd.DataFrame()

def process_page(year = 0, month = 1, taric = 0):
    url = 'http://aduanas.camaras.org/index.phpc?impexp=E&anno=' + \
    '{year}&mes={month}&tipo=ORGDES&meses="{month}"&producto=TA&codprod={taric}'.format(year=year, month=month, taric=taric) + \
    '&areanacional=PR&codareanac=&areainternac=PS&codareainter=400&result=PR&orden=LOCAL&tipo=ORGDES'
    
    print(url)
    req = requests.get(url)
    sopa = BeautifulSoup(req.text, "html5lib")

    result = {}
    headers = {}

    table_data = sopa.find('table', {'class': 'modTb'})
    if table_data:

        try:
            [x.extract() for x in table_data.findAll('p', {'class' : 'tableLinks'})]
        except AttributeError:
            pass

        for n, th in enumerate(table_data.thead.tr.children):
            header = th
                  
            try:
                th.find('span').extract()
            except AttributeError:
                pass
        
            header = header.text.strip().rstrip('\n')
            if header != '':
                headers[n] = header
               
            
        for n, tr in enumerate(table_data.tbody.findAll('tr', {})):
            result[n] = {}
            for m, td in enumerate(tr.findAll('td', {})):
                result[n][m] = str(td.text)       

        data = []
        for n, row in result.items():
            data.append([])
            for m, column in row.items():
                data[n].append(column)

        f= pd.DataFrame(data, columns=headers.values())
        f.loc[:, 'Mes']=np.array([month]*len(f))
        f.loc[:, 'Anyo']=np.array(['20'+ str(year)]*len(f))
        f.loc[:, 'Precio Medio']=np.array(0)
        
        

        for i in range (0,len(f)):
            print(f.iloc[i, 0])
            f.iloc[i,1] = float(f.iloc[i,1].replace('.', '').replace(',', '.'))
            f.iloc[i,2] = float(f.iloc[i,2].replace('.', '').replace(',', '.'))
            f.iloc[i,5] = str(f.iloc[i,5].replace('01', 'January').replace('02', 'February').replace('03', 'March').replace('04', 'April')
            .replace('05', 'May').replace('06', 'June').replace('07', 'July').replace('08', 'August').replace('09', 'September').replace('10', 'October')
            .replace('11', 'November').replace('12', 'December'))

            if f.iloc[i,1] <=0:
                av_price = 0
            else:
                av_price = round(float(f.iloc[i,2]) / float(f.iloc[i,1]),2)
            f.iloc[i,7] = av_price

            
        f.sort_values(by=['Anyo'])
        resultado = pd.concat([df,f])
        return resultado

    else:
        
        print('Not found')
        return df

taric = '20057000'

for year in range(15, 23):
    for month in range(1, 13):
        if month >= 1 and month <= 9:
            month = '0' + str(month)
        df = process_page(str(year), str(month), taric)


correlativo = list(np.arange(0,len(df)))

dfsorted = df.sort_values(by= ['Provincia', 'Anyo', 'Mes'], ascending= True)

df = pd.DataFrame(dfsorted.values, index=[correlativo], columns = [df.columns])

df['Elasticity'] = np.zeros(len(df))

#print(df)

for i in range(0,len(df)):
    if int(i) < len(df):

        try:
            elasticidad = abs((float(df.iloc[i+1]['Precio Medio']) - float(df.iloc[i]['Precio Medio']) / float(df.iloc[i]['Precio Medio'])) \
            / float(df.iloc[i+1]['Peso']) - float(df.iloc[i]['Peso']) / float(df.iloc[i]['Peso']))
            df.at[i, 'Elasticity'] = elasticidad
         
        except ZeroDivisionError:
            pass
       

print(df)
                  
#df.to_csv('{}.csv'.format(taric +'_aceitunas2'), index= False, encoding='utf-8', sep=',', na_rep='Unknown')
