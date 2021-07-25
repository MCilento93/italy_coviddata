# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 18:40:31 2020

@author: mario
"""

### MODULES

import requests, io
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.integrate import quad
plt.style.use('seaborn-darkgrid')
plt.ioff()

### DEFs

# Curve fitting
def power_law_model(x,a,b,c):
    """ To be used to fit 'overall' cases """
    return a*np.exp(b*(x-c))

def logistic_model(x,a,b,c):
    """ To be used to fit 'overall' cases """
    return c/(1+np.exp(-(x-b)/a))

def gauss_model(x, a, b, c):
    """ To be used to fit new daily cases """
    return a*np.exp(-(x-b)**2/(2*c**2))

# Dataframe
def load_dataframe():
    # update every day at 6 PM
    print('\nDownloading italy dataframe: ')
    url="https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale.csv"
    df=pd.read_csv(io.StringIO(requests.get(url).content.decode('utf-8')),
                   sep=',',
                   usecols=lambda column : column not in ['note'],
                   parse_dates=['data'],date_parser=pd.to_datetime,
                   dtype={'stato':str,'note':'str'}) #dict(zip(range(0,17),['str']*2+['float64']*14 + ['str'])))
    df['data'] = pd.to_datetime(df['data'])
    i=df.columns[df.dtypes=='int64']
    df[i]=df[i].astype('float64')
    df=df.set_index('data')
    return df

def add_derivated_labels(df):
    # nuovi tamponi
    tot_tamponi=df['tamponi'].values
    nuovi_tamponi=np.diff(tot_tamponi)
    df.loc[:,'nuovi_tamponi']=np.concatenate(([np.nan],nuovi_tamponi))
    # positivi_su_tamponi = nuovi_positivi/nuovi_tamponi
    df.loc[:,'positivi_su_tamponi']=np.round(df['nuovi_positivi'].values/df['nuovi_tamponi'].values,4)
    # nuovi_deceduti
    tot_deceduti=df['deceduti'].values
    nuovi_deceduti=np.diff(tot_deceduti)
    df.loc[:,'nuovi_deceduti']=np.concatenate(([np.nan],nuovi_deceduti))
    return df

def plot_dataframe(df,label,save=False):
    fig=plt.figure()
    df[label].plot(xlabel='Time',ylabel=label,title='Data for Italy')
    if save:
        plt.savefig('italy_coviddata_curvefit data.png')
    return fig

def plot_resume(df,save=False):

    # Data
    time_str=df.index[-1].strftime('%d/%m/%Y')

    # Figure
    fig = plt.figure(figsize = (6,9))
    fig.suptitle('Dati Covid-19 Italia agg.to '+time_str,
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

    # Plot(0,0) - totale_casi
    ax=df['totale_casi'].plot(lw=4,ax=top,
                              legend=False,
                              color='red',
                              title='Totale casi',
                              grid=True)
    ax.set(xlabel=None)
    ax.grid(color='grey', linestyle='-.',linewidth=.5)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.set_facecolor((0, 0, 0, .05))

    # Plot(0,1) - nuovi_positivi
    ax=df['nuovi_positivi'].plot(lw=3,ax=bottom_left,
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

    # Plot(1,1) - terapia_intensiva
    ax=df['terapia_intensiva'].plot(lw=3,ax=bottom_right,
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
        plt.savefig('italy_coviddata_curvefit summary plot.png')
    return fig

def get_resume(df,print_=False):
    time_str=df.index[-1].strftime('%d/%m/%Y')
    resume=f"""
🇮🇹 *Situazione ITALIA al {time_str}* 🇮🇹
Attualmente in Italia ci sono {int(df['totale_positivi'].values[-1])} _positivi accertati_, di cui {int(df['nuovi_positivi'].values[-1])} _nuovi casi_.
Oggi sono stati effettuati {int(df['nuovi_tamponi'].values[-1])} _nuovi tamponi_, di cui il  {round(df['positivi_su_tamponi'].values[-1]*100,2)}% sono risultati positivi.

_Dati giornalieri_
🦠 Nuovi casi {int(df['nuovi_positivi'].values[-1])}
🧪 Nuovi tamponi {int(df['nuovi_tamponi'].values[-1])}
🚑 Terapia intensiva {int(df['terapia_intensiva'].values[-1])}
🏥 Ricoverati con sintomi {int(df['ricoverati_con_sintomi'].values[-1])}
🏠 In isolamento domiciliare {int(df['isolamento_domiciliare'].values[-1])}
😵 Nuovi deceduti {int(df['nuovi_deceduti'].values[-1])}

_Dati totali_
🦠 Totale casi {int(df['totale_casi'].values[-1])}
🧪 Totale tamponi {int(df['tamponi'].values[-1])}
😌 Totale guariti {int(df['dimessi_guariti'].values[-1])}
☠️ Totale deceduti {int(df['deceduti'].values[-1])}
    """
    return resume

def value_at_day(df,day,label):
    """This function returns the value of a column at specific day (str)"""
    return int(df.loc[day][label].values)

def count_days(df,day_start,day_desired):
    return df.loc[day_start:day_desired].size

### CLASS

class CovidCurveFit():
    def __init__(self,label,dataframe,day_start,day_end):
        self.label=label
        if day_start and day_end:
            self.df=dataframe.loc[day_start:day_end]
            self.day_start=day_start
            self.day_end=day_end
        else:
            self.df=dataframe
            self.day_start=self.df.index[0].strftime('%Y-%m-%d')
            self.day_end=self.df.index[-1].strftime('%Y-%m-%d')
        # Flags
        self.__fitting_YN=False
        self.__integrate_YN=False

    def calculate_fitting_parameters(self,func_name):
        # function type : str
        # options: 'gauss_model', 'power_law_model', 'logistic_model'
        print('\n'+self.label+' analysis: ')
        print('   > value at '+self.day_start+' is: '+str(value_at_day(self.df,self.day_start,self.label)))
        print('   > value at '+self.day_end+' is: '+str(value_at_day(self.df,self.day_end,self.label)))
        ydata=self.df[self.label].values
        xdata=np.arange(start=1,stop=len(ydata)+1,step=1)
        if func_name=='gauss_model':
            popt, pcov = curve_fit(eval(func_name), xdata, ydata)
        elif func_name=='logistic_model' or func_name=='power_law_model':
            popt, pcov = curve_fit(eval(func_name), xdata, ydata,bounds=(0,np.inf))
        # Results
        self.popt=popt
        self.func_name=func_name
        self.xdata_fitting=xdata
        self.ydata_fitting=ydata
        self.__fitting_YN=True

    def plot_fitting_results(self,save=False,day_offset=15):
        """
        Parameters
        ----------
        save : Bool, optional
            If True the method will save the result. The default is False.
        day_offset : Int, optional
            Days from day_end which extend the projection to. The default is 15.
        """
        print('\nPlotting results of curve fitting by '+self.func_name+' on '+self.label+': ')
        plt.figure()
        plt.plot(self.xdata_fitting, self.ydata_fitting, 'b-', label='Data')
        plt.xlabel('days from '+self.day_start+' to '+self.day_end)
        plt.ylabel(patient_type)
        xdata_offset=np.arange(self.xdata_fitting[-1]+1,cf1.xdata_fitting[-1]+day_offset+1)
        xdata_conca=np.concatenate((self.xdata_fitting, xdata_offset),axis=0)
        plt.plot(xdata_conca, eval(self.func_name+'(xdata_conca, *self.popt)'), 'r-',
                 label='fitted with '+self.func_name)
        plt.legend()
        if save:
            plt.savefig('italy_coviddata_curvefit fitting.png')

    def fitting_results(self,xdata):
        if self.__fitting_YN:
            return eval(self.func_name+'(xdata,*self.popt)')
        else:
            print('Do fitting first ...')

    def fitting_results_day_desired(self,day_desired):
        if self.__fitting_YN:
            xvalue=count_days(self.df, self.day_start, day_desired)
            res=self.fitting_results(xvalue)
            print('\nResults fitting for '+day_desired+': ')
            print('   > Value the '+day_desired+' is :'+str(value_at_day(self.df, day_desired, self.label)))
            print('   > Fit value the '+day_desired+' is :'+str(res))
            return res
        else:
            print('Do fitting first ...')

    def calculate_integrate_curve(self):
        self.yfit_integrate=[quad(eval(func_name), 1, i, args=(self.popt[0],self.popt[1],self.popt[2]))[0] for i in self.xdata_fitting]
        self.__integrate_YN=True

    def plot_integrate_results(self,save=False):
        plt.figure()
        plt.plot(self.xdata_fitting,self.yfit_integrate,label=self.func_name+' integration')
        plt.plot(self.xdata_fitting,self.ydata_fitting.cumsum(),'+r',label='real data')
        plt.xlabel('days')
        plt.ylabel(patient_type+' integration')
        plt.title('integration')
        plt.legend()
        if save:
            plt.savefig('italy_coviddata_curvefit integration.png')

### MAIN

if __name__=='__main__':

    # Test-settings
    plt.ion()

    # Globals
    SAVE_ALL=False

    # Inputs
    patient_type='nuovi_positivi'
        # options: 'ricoverati_con_sintomi', 'terapia_intensiva',
        #     'totale_ospedalizzati', 'isolamento_domiciliare', 'totale_positivi',
        #     'variazione_totale_positivi', 'nuovi_positivi', 'dimessi_guariti',
        #     'deceduti', 'casi_da_sospetto_diagnostico', 'casi_da_screening',
        #     'totale_casi', 'tamponi', 'casi_testati'
    func_name='gauss_model'
        # options: 'gauss_model', 'power_law_model', 'logistic_model'
    day_start='2020-10-01' # day for fitting to start
    day_end='2020-11-06' # day for fitting to finish
    # day_end='2020-06-01' # day for fitting to finish

    # Opening data from server
    df=load_dataframe()
    df=add_derivated_labels(df) # include useful derivatives
    get_resume(df,print_=True)
    plot_dataframe(df,label=patient_type,save=SAVE_ALL)
    plot_resume(df,save=SAVE_ALL)

    # Costruction of class for analysis
    cf1=CovidCurveFit(label=patient_type,dataframe=df,day_start=day_start,day_end=day_end)
    cf1.calculate_fitting_parameters(func_name)
    cf1.calculate_integrate_curve()

    # Relevant results
    cf1.plot_fitting_results(save=SAVE_ALL,day_offset=15)
    cf1.fitting_results_day_desired(day_end)
    cf1.plot_integrate_results(save=SAVE_ALL)
