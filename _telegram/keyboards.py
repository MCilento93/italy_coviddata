# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 13:00:58 2020

@author: mario
"""

### MODULES

import telegram

### GLOBALs

message_keyboard="Trovi sotto la chat la tua tastiera personalizzata ⌨️"

### DEFs

def keyboard_Cava_de_Tirreni(update,context):
    # Custom keyboard
    custom_keyboard = [
        # main commands
        ['/ita'],['/reg Campania'],['/prov Salerno'],["/city Cava de' Tirreni"],
        ['/city Nocera','/city Salerno','/city Vietri sul mare'],
        # leaving
        ['/start','/help','/keyboards'],
    ]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard,resize_keyboard=True)
    update.message.reply_text(text=message_keyboard,reply_markup=reply_markup)
    
def keyboard_Internazionale(update,context):
    # Custom keyboard
    custom_keyboard = [
        # main commands
        ['/world ita'],
        ['/world USA'],
        ['/world Germany'],
        ['/world China'],
        ['/world Russia'],
        ['/world UK'],
        ['/world Japan'],
        # leaving
        ['/start','/help','/keyboards'],
    ]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard,resize_keyboard=True)
    update.message.reply_text(text=message_keyboard,reply_markup=reply_markup)
    
def keyboard_Campania(update,context):
    # Custom keyboard
    custom_keyboard = [
        # main commands
        ['/ita'],['/reg Campania'],
        ['/prov Salerno','/prov Napoli','/prov Avellino','/prov Benevento','/prov Caserta'],
        # leaving
        ['/start','/help','/keyboards'],
    ]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard,resize_keyboard=True)
    update.message.reply_text(text=message_keyboard,reply_markup=reply_markup)
    
def keyboard_Lombardia(update,context):
    # Custom keyboard
    custom_keyboard = [
        # main commands
        ['/ita'],['/reg Lombardia'],
        ['/prov Milano','/prov Bergamo','/prov Brescia','/prov Como'],
        ['/city Milano'],
        # leaving
        ['/start','/help','/keyboards'],
    ]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard,resize_keyboard=True)
    update.message.reply_text(text=message_keyboard,reply_markup=reply_markup)
  
def keyboard_Sud_Italia(update,context):
    # Custom keyboard
    custom_keyboard = [
        # main commands
        ['/ita'],
        ['/reg Campania','/reg Puglia','/reg Sicilia','/reg Calabria','/reg Basilicata','/reg Molise'],
        ['/prov Napoli','/prov Salerno','/prov Bari','/prov Foggia'],
        ['/prov Messina','/prov Palermo','/prov Catania','/prov Agrigento'],
        ['/prov Potenza','/prov Campobasso','/prov Cosenza','/prov Reggio Calabria'],
        # leaving
        ['/start','/help','/keyboards'],
    ]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard,resize_keyboard=True)
    update.message.reply_text(text=message_keyboard,reply_markup=reply_markup)
  
    