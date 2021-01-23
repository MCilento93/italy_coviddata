# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
filename=r'Codici-statistici-e-denominazioni-al-01_07_2020.csv'
df=pd.read_csv(filename,sep=';',encoding='ISO-8859-1')
df.rename(columns={"Denominazione dell'Unità territoriale sovracomunale \r\n(valida a fini statistici)": 'Province',
                            "Denominazione in italiano":"Comuni",
                            "Denominazione Regione":"Regioni",
                            "Ripartizione geografica":'Zona'},
                   inplace=True)
df=df[['Province','Regioni','Comuni','Zona']]

# lista regioni
lista_reg=list(df.groupby('Regioni').groups.keys())

# lista province
lista_prov=list(df.groupby('Province').groups.keys())

# lista prov. per regione
reg='Marche'
lista_prov_xreg=list(df.groupby('Regioni').get_group(reg).groupby('Province').groups.keys())

# lista comune per prov.
prov='Salerno'
lista_city_xprov=list(df.groupby('Province').get_group(prov)['Comuni'])

print(lista_reg)
