# -*- coding: utf-8 -*-
"""
Created on Sun Nov  8 18:58:04 2020

@author: mario, pietro
"""

### MODULES

import os, configparser, time, requests, json

### START-UP

# Folders
MODULE_DIR = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
SW_DIR=os.path.dirname(MODULE_DIR)

# Configuration
config = configparser.ConfigParser()
config.read(os.path.join(SW_DIR,'config.ini'))

### DEFs

def world_cases(country_name):

    url = "https://covid-19-data.p.rapidapi.com/country"
    querystring = {"name":country_name}

    headers = {
        'x-rapidapi-key': config['WORLD_DATA']['x-rapidapi-key'],
        'x-rapidapi-host': config['WORLD_DATA']['x-rapidapi-host']
        }

    try:
        response = requests.request("GET", url, headers=headers, params=querystring)
        data = response.text[1:-1]
        dict_result = json.loads(data)
    except:
        dict_result=None
    return dict_result

def get_world_resume(country_name):
    resume=world_cases(country_name)
    if resume:
        resume_str=f"""
*❗️ Situazione in {resume['country']} al {resume['lastChange'][:10]} ❗️*
        
_Dati giornalieri_
🚑 Terapia intensiva {resume['critical']}
    
_Dati totali_
🦠 Totale casi {resume['confirmed']}
😌 Totale guariti {resume['recovered']}
☠️ Totale deceduti {resume['deaths']}
"""
    else:
        resume_str='Mi dispiace non ho trovato niente 😖'
    return resume_str

### MAIN

if __name__=='__main__':
       
    # Setup
    country_name='France'
    
    # Latest report for France
    print(get_world_resume(country_name))
    
    # Latest report for US
    time.sleep(1) # api-latency estimated at 26 ms
    print(get_world_resume('USA'))