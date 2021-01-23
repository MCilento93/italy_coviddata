# -*- coding: utf-8 -*-
"""
Created on Sat Oct 17 14:58:08 2020

@author: mario
"""

### MODULES

import datetime, pytz
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('seaborn-darkgrid')
plt.ioff()

### DEFs

def load_full_repository(day_start='20200224'):
    """ gluing data for regions """
    update_dataserver_time=datetime.time(18,0,0) # here the time *.csv are loaded from pcm-dpc
    current_time_italy=datetime.datetime.now().astimezone(pytz.timezone('Europe/Rome'))
    if current_time_italy.time()>update_dataserver_time:
        date_array=pd.date_range(start=day_start,end=current_time_italy.date())
    else:
        date_array=pd.date_range(start=day_start,end=current_time_italy.date()-datetime.timedelta(1))
    date_array_str=[i.strftime("%Y%m%d") for i in date_array]
    url_address='https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni-'
    url_addresses=[url_address+i+'.csv' for i in date_array_str]
    df=pd.DataFrame([])
    print('\nCollecting dataframes for regions: ')
    for i in url_addresses:
        print('   > '+i)
        df_partial = pd.read_csv(i, error_bad_lines=False)
        df=df.append(df_partial)
    df['data'] = pd.to_datetime(df['data'])
    df=df.set_index('data')
    return df

### CLASS

class CovidItalyRegion():
    def __init__(self,df,region,day_start):
        self.df=df
        self.region=region
        self.day_start=day_start
        self.df_region=self.get_df_region()
        self.add_daily_cases()

    def get_df_region(self):
        df_tmp=self.df[self.df['denominazione_regione']==self.region]
        return df_tmp.copy()

    def get_resume(self):
        time_str=self.df_region.index[-1].strftime('%d/%m/%Y')
        resume=f"""
*❗️ Situazione in {self.region} al {time_str} ❗️*
Attualmente in {self.region} ci sono {int(self.df_region['totale_positivi'].values[-1])} _positivi accertati_, di cui {int(self.df_region['nuovi_positivi'].values[-1])} _nuovi casi_.
Oggi sono stati effettuati {int(self.df_region['tamponi_giornalieri'].values[-1])} _nuovi tamponi_, di cui il {round(self.df_region['positivi_su_tamponi'].values[-1]*100,4)}% sono risultati positivi.
        
_Dati giornalieri_
🦠 Nuovi casi {int(self.df_region['nuovi_positivi'].values[-1])}
🚑 Terapia intensiva {int(self.df_region['terapia_intensiva'].values[-1])}
🏥 Ricoverati con sintomi {int(self.df_region['ricoverati_con_sintomi'].values[-1])}
🏠 In isolamento domiciliare {int(self.df_region['isolamento_domiciliare'].values[-1])}
😵 Nuovi deceduti {int(self.df_region['deceduti_giornalieri'].values[-1])}
        
_Dati totali_
🦠 Totale casi {int(self.df_region['totale_casi'].values[-1])}
🧪 Totale tamponi {int(self.df_region['tamponi'].values[-1])}
😌 Totale guariti {int(self.df_region['dimessi_guariti'].values[-1])}
☠️ Totale deceduti {int(self.df_region['deceduti'].values[-1])}
        
_Altri dati_
- Casi da sospetto diagnostico {int(self.df_region['casi_da_sospetto_diagnostico'].values[-1])}
- Casi da screening {int(self.df_region['casi_da_screening'].values[-1])}
- Casi testati {int(self.df_region['casi_testati'].values[-1])}
        """
        return resume

    def add_daily_cases(self):
        # tamponi_giornalieri
        tamponi=self.df_region['tamponi'].values
        daily_tamponi=np.diff(tamponi)
        self.df_region.loc[:,'tamponi_giornalieri']=np.concatenate(([daily_tamponi[0]],daily_tamponi))
        # positivi_su_tamponi
        self.df_region.loc[:,'positivi_su_tamponi']=np.round(self.df_region['nuovi_positivi'].values/self.df_region['tamponi_giornalieri'].values,4)
        # deceduti_giornalieri
        deceduti=self.df_region['deceduti'].values
        daily_deceduti=np.diff(deceduti)
        self.df_region.loc[:,'deceduti_giornalieri']=np.concatenate(([daily_deceduti[0]],daily_deceduti))

    def print_resume(self):
        print(self.get_resume())

    def plot_total_cases(self,save=False):
        fig=plt.figure()
        self.df_region['totale_casi'].plot(xlabel='Date',ylabel=self.region,title='Tot. cases for '+self.region)
        if save:
            plt.savefig('italy_coviddata_regions totale_casi '+self.region+'.png')
        return fig

    def plot_daily_cases(self,save=False):
        fig=plt.figure()
        self.df_region['nuovi_positivi'].plot(xlabel='Date',ylabel=self.region,title='Daily cases for '+self.region)
        if save:
            plt.savefig('italy_coviddata_regions nuovi_positivi '+self.region+'.png')
        return fig
    
    def plot_resume(self,save=False):
        # Data
        time_str=self.df_region.index[-1].strftime('%d/%m/%Y')
        
        # Figure
        fig = plt.figure(figsize = (6,9))
        fig.suptitle('Dati Covid-19 regione '+self.region+' agg.to '+time_str,
                     horizontalalignment='center',
                     verticalalignment='top',
                     fontweight='bold',
                     fontsize=14)
        grid_size = (3,2)
        fig.text(x=0.95,y=0.001, s='Source: @italycoviddataBot',
                  horizontalalignment='right',
                  color='#524939',
                  fontsize=10)
        top = plt.subplot2grid(grid_size, (0,0), colspan=2, rowspan=2)
        bottom_left=plt.subplot2grid(grid_size,(2,0))
        bottom_right=plt.subplot2grid(grid_size,(2,1))
    
        # Plot(0,0) - totale casi
        ax=self.df_region['totale_casi'].plot(lw=4,ax=top,
                                  legend=False,
                                  color='red',
                                  title='Totale casi',
                                  grid=True)
        ax.set(xlabel=None)
        ax.grid(color='grey', linestyle='-.',linewidth=.5)
        ax.spines['bottom'].set_visible(True)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.set_facecolor((0, 0, 0, .05))
    
        # Plot(0,1) - nuovi positivi
        ax=self.df_region['nuovi_positivi'].plot(lw=3,ax=bottom_left,
                                     legend=False,
                                     color='green',
                                     linestyle='dotted',
                                     title='Nuovi positivi',
                                     grid=True)
        ax.set(xlabel=None)
        ax.grid(color='grey',linestyle='-.',linewidth=.5)
        ax.grid(color='grey',linestyle='-.',linewidth=.5)
        plt.setp(ax.get_xticklabels(), visible=True)
        plt.setp(ax.get_yticklabels(), visible=True)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.set_facecolor((1, 0, 0, 0.2))
    
        # Plot(1,1) - terapia intensiva
        ax=self.df_region['terapia_intensiva'].plot(lw=3,ax=bottom_right,
                                legend=False,
                                color='blue',
                                grid=True,
                                linestyle='-.',
                                title='Terapia intensiva')
        ax.set(xlabel=None)
        ax.grid(color='grey',linestyle='-.',linewidth=.5)
        plt.setp(ax.get_xticklabels(), visible=True)
        plt.setp(ax.get_yticklabels(), visible=True)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.set_facecolor((0, 1, 0, 0.2))
        
        # Leaving
        plt.tight_layout()
        if save:
            plt.savefig('italy_coviddata_regions summary plot '+self.region+'.png')
        return fig

### MAIN

if __name__=='__main__':
    
    # Test-settings
    plt.ion()
    
    # Global
    SAVE_ALL=False
    
    # Loading data from server (it may take time)
    day_start='20200224' # format YYYYMMDD
    df=load_full_repository(day_start=day_start)

    # Construction of object and analysis for 'Salerno' province
    rd1=CovidItalyRegion(df, 'Campania', day_start)
    rd1.print_resume()
    rd1.plot_total_cases(save=SAVE_ALL)
    rd1.plot_daily_cases(save=SAVE_ALL)
    rd1.plot_resume(save=SAVE_ALL)
    
    # Construction of object and analysis for 'Milano' province
    rd2=CovidItalyRegion(df, 'P.A. Bolzano', day_start)
    rd2.plot_total_cases()
    rd2.plot_daily_cases()
    rd2.print_resume()
    rd2.plot_resume()