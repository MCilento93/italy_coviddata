# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 19:55:52 2020

@author: mario, pietro
"""

### MODULES

import GoogleNews
import humanize

### DEFs

def gnews_covid_search(city_name):
    
    # Setup    
    googlenews = GoogleNews.GoogleNews()
    googlenews.set_lang('it')
    googlenews.set_period('15d')
    googlenews.set_encode('utf-8')
    
    # Search
    # googlenews.get_news(f'covid positivi {city_name}')
    googlenews.search(f'covid positivi {city_name}')
    gnews_results=googlenews.results(sort=True)
    
    return gnews_results

def filter_gnews_results(gnews_results,city_name):
    # Filters
    results=[]
    for gnew in gnews_results:
        if city_name.lower() in gnew['desc'].lower() and 'positivi' in gnew['desc'].lower():
            results.append(gnew)
    # Delete repeated news
    # results=list(dict.fromkeys(results))
    results = [i for n, i in enumerate(results) if i not in results[n + 1:]]
    return results[:5]

def get_resume(city_name):
    """
    Assumptions: 
        - first page of google news
        - fixed keywords for the research
        - 'Approfondimenti' fetched too easily tackled
    """
    humanize.i18n.activate('it_IT')
    gnews_results=gnews_covid_search(city_name)
    gnews_results_filtered=filter_gnews_results(gnews_results, city_name)
    if gnews_results_filtered!=[]:
        resume=f"""
Questo è quello che son riuscito a trovare in rete 🌐 in merito ai dati covid sulla città di {city_name}😁   
Ti elenco alcuni articoli ed i rispettivi link per approfondire 🧐 (ho fatto una bella pulitina 🧹 per te)
        """
        resume_gnews=''
        for gnew in gnews_results_filtered:
            resume_gnews+=f"\n*{humanize.naturaltime(gnew['datetime'])}*\n{gnew['desc']} ([link]({gnew['link']}))\n"
    else:
        resume=f"Mi dispiace non ho trovato dati sulla citta di {city_name} 😕.\n Puoi provare a scrivere meglio?"
        resume_gnews=''
    return resume+resume_gnews
    
### MAIN

if __name__=='__main__':
    
    # Example for Cava De' Tirreni
    city_name="cava de' tirreni"
    gnews_results=gnews_covid_search(city_name)
    gnews_results_filtered=filter_gnews_results(gnews_results, city_name)
    
    # Telegram-bot resum for Pontecagnano (short for previous code)
    print(get_resume("Vietri sul Mare"))