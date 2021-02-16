# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 12:31:08 2021

@author: mario
"""

### MODULES

import pandas as pd

### DEFs

def load_full_repository():

    # loading
    print('\nCollecting dataframes for regions (vaccines): ')
    url_address='https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/vaccini-summary-latest.csv'
    df = pd.read_csv(url_address, error_bad_lines=False)

    # index & renaming
    df=df.set_index('nome_area')
    dict_names={'Friuli-Venezia Giulia':'Friuli Venezia Giulia',
                'Provincia Autonoma Bolzano / Bozen':'P.A. Bolzano',
                'Provincia Autonoma Trento':'P.A. Trento',
                "Valle d'Aosta / Vallée d'Aoste":"Valle d'Aosta"} # from name of vaccines repo to name in pcm-dpc/COVID-19
    df.rename(index=dict_names,inplace=True)

    # add column with number of (region) citizens
    df=add_column_number_citizens(df)

    return df

def add_column_number_citizens(df_vax):

    # Filling with data from https://www.tuttitalia.it/regioni/
    df_vax['tot_popolazione']=float('Nan')
    df_vax.at['Abruzzo','tot_popolazione']=1293941
    df_vax.at["Basilicata",'tot_popolazione']=553254
    df_vax.at["Calabria",'tot_popolazione']=1894110
    df_vax.at["Campania",'tot_popolazione']=5712143
    df_vax.at["Emilia-Romagna",'tot_popolazione']=4464119
    df_vax.at["Friuli Venezia Giulia",'tot_popolazione']=1206216
    df_vax.at["Lazio",'tot_popolazione']=5755700
    df_vax.at["Liguria",'tot_popolazione']=1524826
    df_vax.at["Lombardia",'tot_popolazione']=10027602
    df_vax.at["Marche",'tot_popolazione']=1512672
    df_vax.at["Molise",'tot_popolazione']=300516
    df_vax.at['P.A. Bolzano','tot_popolazione']=532644
    df_vax.at['P.A. Trento','tot_popolazione']=545425
    df_vax.at["Piemonte",'tot_popolazione']=4311217
    df_vax.at["Puglia",'tot_popolazione']=3953305
    df_vax.at["Sardegna",'tot_popolazione']=1611621
    df_vax.at["Sicilia",'tot_popolazione']=4875290
    df_vax.at["Toscana",'tot_popolazione']=3692555
    df_vax.at["Umbria",'tot_popolazione']=870165
    df_vax.at["Valle d'Aosta",'tot_popolazione']=125034
    df_vax.at["Veneto",'tot_popolazione']=4879133

    # Tot rateo
    df_vax['rateo_somministrazioni']=df_vax['dosi_somministrate']/df_vax['tot_popolazione']

    return df_vax

def get_italy_resume(df_vax):
    date_last_update=df_vax.ultimo_aggiornamento[0]
    tot_dosi_somministrate=df_vax['dosi_somministrate'].sum()
    tot_popolazione=df_vax['tot_popolazione'].sum()
    percentuale_vaccinati=tot_dosi_somministrate/tot_popolazione/2
    resume=f"""
*Distribuzione vaccini in Italia 🇮🇹 al {date_last_update}*
Complessivamente sono stati distribuiti {int(tot_dosi_somministrate)} vaccini (circa il {round(percentuale_vaccinati,4)*100}% della popolazione è attualmente vaccinata).
    """
    return resume

def get_region_resume(df_vax,reg_name):
    date_last_update=df_vax.ultimo_aggiornamento[0]
    tot_dosi_somministrate=df_vax.loc[reg_name]['dosi_somministrate']
    tot_dosi_consegnate=df_vax.loc[reg_name]['dosi_consegnate']
    tot_popolazione=df_vax.loc[reg_name]['tot_popolazione']
    percentuale_vaccinati=tot_dosi_somministrate/tot_popolazione/2
    resume=f"""
*Distribuzione vaccini in {reg_name} al {date_last_update}*
📦 Dosi consegnate {int(tot_dosi_consegnate)}
💉 Dosi somministrate {int(tot_dosi_somministrate)}
_({round(percentuale_vaccinati,3)*100}% degli abitanti è attualmente vaccinato)_
    """
    return resume

### MAIN

if __name__=='__main__':

    # Loading data from server (it may take time)
    df_vax=load_full_repository()

    # Print italy resume
    print(get_italy_resume(df_vax))

    # Print regions report
    print(get_region_resume(df_vax,'Campania'))
    print(get_region_resume(df_vax,'P.A. Bolzano'))
