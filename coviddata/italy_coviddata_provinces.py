# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 17:04:12 2020

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
    """ gluing data for provinces """
    update_dataserver_time=datetime.time(18,0,0) # here the time *.csv are loaded from pcm-dpc
    current_time_italy=datetime.datetime.now().astimezone(pytz.timezone('Europe/Rome'))
    if current_time_italy.time()>update_dataserver_time:
        date_array=pd.date_range(start=day_start,end=current_time_italy.date())
    else:
        date_array=pd.date_range(start=day_start,end=current_time_italy.date()-datetime.timedelta(1))
    date_array_str=[i.strftime("%Y%m%d") for i in date_array]
    url_address='https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-province/dpc-covid19-ita-province-'
    url_addresses=[url_address+i+'.csv' for i in date_array_str]
    df=pd.DataFrame([])
    print('\nCollecting dataframes of provinces: ')
    for i in url_addresses:
        print('   > '+i)
        df_partial = pd.read_csv(i, error_bad_lines=False)
        df=df.append(df_partial)
    df['data'] = pd.to_datetime(df['data'])
    df=df.set_index('data')
    return df

### CLASS

class CovidItalyProvince():
    def __init__(self,df,province,day_start):
        self.df=df
        self.province=province
        self.day_start=day_start
        self.df_province=self.get_df_province()
        self.add_daily_cases()

    def get_df_province(self):
        df_tmp=self.df[self.df['denominazione_provincia']==self.province]
        return df_tmp.copy()

    def get_resume(self):
        time_str=self.df_province.index[-1].strftime('%d/%m/%Y')
        resume=f"""
*❗️ Situazione in provincia di {self.province} al {time_str} ❗️*
In provincia di {self.province} oggi sono stati registrati {int(self.df_province['casi_giornalieri'].values[-1])} _nuovi casi_ 🦠 su un _totale_ di {int(self.df_province['totale_casi'].values[-1])} casi da inizio pandemia.
        """
        return resume

    def add_daily_cases(self):
        tot_cases=self.df_province['totale_casi'].values
        daily_cases=np.diff(tot_cases)
        # self.df_province['casi giornalieri']=np.concatenate(([np.nan],daily_cases))
        self.df_province.loc[:,'casi_giornalieri']=np.concatenate(([np.nan],daily_cases))

    def print_resume(self):
        print(self.get_resume())

    def plot_total_cases(self,save=False):
        fig=plt.figure()
        self.df_province['totale_casi'].plot(xlabel='Date',ylabel=self.province,title='Tot. cases for '+self.province)
        if save:
            plt.savefig('italy_coviddata_provinces totale_casi '+self.province+'.png')
        return fig

    def plot_daily_cases(self,save=False):
        plt.figure()
        self.df_province['casi_giornalieri'].plot(xlabel='Date',ylabel=self.province,title='Daily cases for '+self.province)
        if save:
            plt.savefig('italy_coviddata_provinces casi_giornalieri '+self.province+'.png')
    
    def plot_resume(self,save=False):
        # Data
        time_str=self.df_province.index[-1].strftime('%d/%m/%Y')
        
        # Figure
        fig = plt.figure(figsize = (6,9))
        fig.suptitle('Dati Covid-19 in provincia di '+self.province+' agg.to '+time_str,
                     horizontalalignment='center',
                     verticalalignment='top',
                     fontweight='bold',
                     fontsize=14)
        grid_size = (2,1)
        fig.text(x=0.95,y=0.001, s='Source: @italycoviddataBot',
                  horizontalalignment='right',
                  color='#524939',
                  fontsize=10)
        top = plt.subplot2grid(grid_size, (0,0))
        bottom = plt.subplot2grid(grid_size, (1,0))
    
        # Plot(0,0) - totale_casi
        ax=self.df_province['totale_casi'].plot(lw=4,ax=top,
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
    
        # Plot(1,0) - casi_giornalieri
        ax=self.df_province['casi_giornalieri'].plot(lw=3,ax=bottom,
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
    
        # Leaving
        plt.tight_layout()
        if save:
            plt.savefig('italy_coviddata_provinces summary plot '+self.province+'.png')
        return fig
        
### MAIN

if __name__=='__main__':
    
    # Test-settings
    plt.ion()
    
    # Globals
    SAVE_ALL=False

    # Loading data from server (it may take time)
    day_start='20200224' # format YYYYMMDD
    df=load_full_repository(day_start=day_start)

    # Construction of object and analysis for 'Salerno' province
    plt.ion()
    pd1=CovidItalyProvince(df, 'Salerno', day_start)
    pd1.print_resume()
    pd1.plot_total_cases(save=SAVE_ALL)
    pd1.plot_daily_cases(save=SAVE_ALL)
    pd1.plot_resume(save=SAVE_ALL)
    
    # Construction of object and analysis for 'Milano' province
    pd2=CovidItalyProvince(df, 'Milano', day_start)
    pd2.plot_total_cases()
    pd2.plot_daily_cases()
    pd2.print_resume()
    pd2.plot_resume()