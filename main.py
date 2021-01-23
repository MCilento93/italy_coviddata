# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 19:42:58 2020

@author: mario, pietro
"""

### MODULES

# From env
import os, json, datetime, pytz, time, sys, logging, configparser
import numpy as np
from inspect import getmembers, isfunction
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from geopy.geocoders import Nominatim
    
# From this package
import coviddata.world_coviddata as world_coviddata
import coviddata.italy_coviddata_curvefit as italy_coviddata_curvefit
import coviddata.italy_coviddata_regions as italy_coviddata_regions
import coviddata.italy_coviddata_provinces as italy_coviddata_provinces
import coviddata.italy_coviddata_cities as italy_coviddata_cities
from _telegram.users_database import UsersDatabase
import _telegram.keyboards as keyboards

### START-UP

# Setting current timezone
os.environ["TZ"] = "Europe/Rome"
time.tzset()

# Foldering
CWD_DIR=os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

# Settings
config = configparser.ConfigParser()
config.read('config.ini')

# Logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(CWD_DIR+'/logs/logfile.log')
formatter    = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.debug('*** Bot restarted! ***')

# Bot
ADMIN_IDS=[1379464630, 65182504,124006141]

### DEFs

# Auxiliary

def fig2bytes(fig):
    """Convert a Matplotlib figure to bytes on memory"""
    import io
    buf = io.BytesIO()
    fig.savefig(buf)
    buf.seek(0)
    return buf

def send_message(chat_id, text):
    try:
        bot.send_message(chat_id,text=text)
    except:
        # error occurring when bot join the bot
        user_str=UsersDatabase.get_user_str(chat_id)
        logger.error('Error \'' + str(sys.exc_info()[0])  + '\' sending a message to '+ user_str)

def send_message_all_users(text):
    users=UsersDatabase.get_users()
    for user in users:
        send_message(user['chat_id'], text)

def store_user_data(message):
    # collecting infos
    chat_id = message.chat.id
    reg_date = message.date.strftime('%Y-%m-%d')
    username = message.chat.username
    f_name = message.chat.first_name
    l_name = message.chat.last_name
    # MySQL database
    UsersDatabase.add_user(chat_id,reg_date,username,f_name,l_name)
    # dump for visualization
    with open("users_dump.json", "w") as write_file:
        json.dump(UsersDatabase.get_users(), write_file,indent=4)
    user_str=UsersDatabase.get_user_str(message.chat.id)
    logger.info(user_str + ' added to bot-database')

def store_user_lon_lat(chat_id:int,longitude:float,latitude:float):
    print('to do list') # !!! write

def address_from_coordinates(longitude=14.718719,latitude=40.718220):
    geolocator = Nominatim(user_agent="https://t.me/italycoviddataBot")
    coordinates=str(latitude)+','+str(longitude)
    logger.info('searching location info at: '+coordinates)
    location = geolocator.reverse(coordinates)
    print('#------User Location Sent------#')
    print(f'Coordinates: {coordinates}')
    print(f'Location: {location}')
    addr=location.raw['address']
    user_location={}
    user_location['reg']=addr.get('state')
    user_location['prov']=addr.get('county')
    user_location['city']=addr.get('city',addr.get('town',addr.get('village',addr.get('county'))))
    user_location['address']=location.raw['display_name']
    print(f'Summary for italycoviddata: {user_location}')
    print('#------------------------------#')
    logger.info('location results: '+user_location.__str__())
    return user_location

# Upload Dataframes

def __daily_bot_update(CallbackContext):
    # Update
    current_time_italy=datetime.datetime.now().astimezone(pytz.timezone('Europe/Rome'))
    date_now=current_time_italy.strftime('%Y-%m-%d %H:%M')
    print('\n- '+date_now+' daily update of dataframes ... ')
    load_df_italy()
    load_df_regions()
    load_df_provinces()
    # Notification
    nuovi_positivi_italy=int(df_italy['nuovi_positivi'].values[-1])
    notification_message='🦠COVID19🦠 aggiornamento dati ...\n' +str(nuovi_positivi_italy)+' nuovi casi in Italia  🇮🇹\nSempre al tuo servizio 😎 .. con nuove funzioni'
    send_message_all_users(notification_message)
    logger.debug('Daily update completed')

def load_df_italy():
    global df_italy
    df_italy=italy_coviddata_curvefit.load_dataframe()
    df_italy=italy_coviddata_curvefit.add_derivated_labels(df_italy) # include positivi/tampone

def load_df_regions():
    global df_regions
    df_regions=italy_coviddata_regions.load_full_repository(day_start=day_start)

def load_df_provinces():
    global df_provinces
    df_provinces=italy_coviddata_provinces.load_full_repository(day_start=day_start)

# Handlers

def start(update,context):
    
    # Updating database
    users=UsersDatabase.get_users()
    chat_ids=[i['chat_id'] for i in users]
    if update.message.chat.id not in chat_ids:
        store_user_data(update.message)
    user_str=UsersDatabase.get_user_str(update.message.chat.id)
    logger.info(user_str+' started the bot')
    
    # Reply
    txt="""
Ciao sono il bot che ti informa sulle statistiche nazionali per il Covid19.
I miei comandi sono estremamente semplici ed intuitivi :D

*Comandi del bot*
/start - Messaggio di Benvenuto
/help - Puoi schiacciare me in caso di difficoltà
/world - Provo a cercare i dati sulle altre nazioni (nome inglese del paese)
/ita - Dati nazionali aggiornati
/reg - Seguito da nome della regione per i dati regionali
/prov - Seguito da nome della provincia per i dati provinciali
/city - Seguito da nome della città desiderata per un tentativo di ricerca dati

*Custom-keyboards*
Sono arrivate le tastiere custom per @italycoviddataBot
Queste ti semplificheranno la vita enormemente ... farai a meno della tastiera del telefono
Digita /keyboards per avere la lista di tastiere disponibili

*Geoconfig*
Mandami la tua posizione così che mi preparo al meglio per servirti i dati della tua zona.
Clicca /geoconfig subito!
    
*About me*
Questo bot è basato sui dati della [protezione civile](https://github.com/pcm-dpc/COVID-19).
Il software è completamente gratuito e fa parte del progetto [italy_covidddata](https://github.com/MCilento93/italy_coviddata).
"""
    reply_markup=get_default_reply_markup(update,context,default=True)
    update.effective_message.reply_text(txt,
                              parse_mode=telegram.ParseMode.MARKDOWN,
                              reply_markup=reply_markup,
                              disable_web_page_preview=True)

def help_(update,context):
    txt=""" Hai problemi? Clicca /start per cominciare 🤓 """
    update.effective_message.reply_text(txt,parse_mode=telegram.ParseMode.MARKDOWN)
    user_str=UsersDatabase.get_user_str(update.message.chat.id)
    logger.info(user_str+' asked for help')

def world(update,context):
    country_name=update.message.text.split(' ')[1:]
    country_name=' '.join(country_name)
    update.message.reply_text('... provo ad estrarre i dati più aggiornati che trovo 🤔')
    update.message.reply_text(world_coviddata.get_world_resume(country_name),parse_mode='Markdown')
    user_str=UsersDatabase.get_user_str(update.message.chat.id)
    logger.info(user_str+' asked for '+country_name+' data')
    
def ita(update,context):
    fig_bytes=fig2bytes(italy_coviddata_curvefit.plot_resume(df_italy))
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=fig_bytes)
    update.effective_message.reply_text(italy_coviddata_curvefit.get_resume(df_italy),parse_mode='Markdown')
    user_str=UsersDatabase.get_user_str(update.message.chat.id)
    logger.info(user_str+' asked for italy-data')

def reg(update,context,reg_name=None):
    if not reg_name:
        reg_name=update.message.text.split(' ')[1:]
        reg_name=' '.join(reg_name)
    user_str=UsersDatabase.get_user_str(update.message.chat.id)
    if reg_name in df_regions.denominazione_regione.values:
        rd1=italy_coviddata_regions.CovidItalyRegion(df_regions, reg_name, day_start)
        fig=rd1.plot_resume()
        fig_bytes=fig2bytes(fig)
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=fig_bytes)
        resume=rd1.get_resume()
        update.effective_message.reply_text(resume,parse_mode='Markdown') # !!! da qui in poi ho cambiato per le 3 prox def quando serviva un reply update.message in update.effective_message
        logger.info(user_str +' asked for '+reg_name+' data')
    else:
        reg_names_array=np.unique(df_regions.denominazione_regione.values)
        reg_names_str='\n'.join(reg_names_array)
        update.effective_message.reply_text('🤔 Scrivi bene il nome della regione')
        update.effective_message.reply_text('Le regioni consentite sono: \n'+reg_names_str)
        logger.warning(user_str+' typed a wrong region name ('+reg_name+')')

def prov(update,context,prov_name=None):
    if not prov_name:
        prov_name=update.message.text.split(' ')[1:]
        prov_name=' '.join(prov_name)
    user_str=UsersDatabase.get_user_str(update.message.chat.id)
    if prov_name in df_provinces.denominazione_provincia.values:
        pd1=italy_coviddata_provinces.CovidItalyProvince(df_provinces, prov_name, day_start)
        fig=pd1.plot_resume()
        fig_bytes=fig2bytes(fig)
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=fig_bytes)
        resume=pd1.get_resume()
        update.effective_message.reply_text(resume,parse_mode='Markdown')
        logger.info(user_str+' asked for '+prov_name+' data')
    else:
        prov_names_array=np.unique(df_provinces.denominazione_provincia.values)
        prov_names_str='\n'.join(prov_names_array)
        update.effective_message.reply_text('🤨 Scrivi bene il nome della provincia')
        update.effective_message.reply_text('Le provincie consentite sono: \n'+prov_names_str)
        logger.warning(user_str+' typed a wrong province name ('+prov_name+')')

def city(update,context,city_name=None):
    if not city_name:
        city_name=update.message.text.split(' ')[1:]
        city_name=' '.join(city_name)
    update.effective_message.reply_text('Mi vuoi mettere proprio alla prova 👨🏻‍💻, eh? ... provo ad estrarre i dati più aggiornati che trovo 🤔')
    update.effective_message.reply_text(italy_coviddata_cities.get_resume(city_name),parse_mode='Markdown')
    user_str=UsersDatabase.get_user_str(update.message.chat.id)
    logger.info(user_str+' asked for '+city_name+' data')
    
def keyboards_message(update,context):
    user_str=UsersDatabase.get_user_str(update.message.chat.id)
    logger.info(user_str+' asked list of keyboards')
    list_keyboards=[]
    for member in getmembers(keyboards):
        if isfunction(member[1]):
            list_keyboards.append(member)
    list_keyboards_str=''.join([f'\n• /{keyboard_name[0]}' for keyboard_name in list_keyboards])
    update.message.reply_text("Lista delle ⌨️ keyboards-personalizzate disponibili:"+list_keyboards_str) 

def geoconfig(update,context):
    location_keyboard = telegram.KeyboardButton(text="📍 Manda la tua posizione GPS", request_location=True)
    custom_keyboard = [[ location_keyboard]]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard,resize_keyboard=True)
    txt="""Vuoi condividere la tua posizione con me? Attiva il GPS ... Se ci sono problemi, mandamela direttamente tu, ok? ☺️"""
    bot.send_message(chat_id=update.effective_message.chat_id, 
                     text=txt, 
                     reply_markup=reply_markup)

def get_default_reply_markup(update,context,default=False):
    # !!! qualsiasi utente che starta il bot deve avere la inline. Se non ci ha dato
    # la location, dobbiamo avere una di default. se ci da una location, possono 
    # esserci problemi, ma voglio cmq dargliela. L'expect sotto non mi piace tantissimo,
    # va strutturato meglio?
    if default:
        keyboard = [
        [InlineKeyboardButton('italia', callback_data="{'c':'ita'}")],
        [InlineKeyboardButton('start', callback_data="{'c':'start'}"),
         InlineKeyboardButton('geoconfig', callback_data="{'c':'geo','a':'start'}"),
         InlineKeyboardButton('keyboards', callback_data="{'c':'keyboards_message'}")],
         [InlineKeyboardButton('help', callback_data="{'c':'help'}")],
         ]
    else:
        """
        user=    {
            "chat_id": 1021123652,
            "reg_date": "2020-10-26",
            "username": None,
            "f_name": "Ciro",
            "l_name": None,
            "country": 'Italia',
            "region":'Campania',
            "province":'Salerno',
            "city":"firenze",
        }
        """
        user=UsersDatabase.get_user(update.effective_message.chat_id) # !!! get longitude and latitude as well
        u_loc=address_from_coordinates(longitude=user['lon'],latitude=user['lat'])
        try:
            keyboard = [
                # main commands
            [InlineKeyboardButton('italia', callback_data="{'c':'ita'}")],
            [InlineKeyboardButton('tua regione', callback_data=f"{{'c':'reg','d':'{u_loc['reg']}'}}")],
            [InlineKeyboardButton('tua provincia', callback_data=f"{{'c':'prov','d':'{u_loc['prov']}'}}")],
            [InlineKeyboardButton('tua città', callback_data=f"{{'c':'city','d':'{u_loc['city']}'}}")],
            [InlineKeyboardButton('start', callback_data="{'c':'start'}"),
             InlineKeyboardButton('geoconfig', callback_data="{'c':'geo','a':'start'}"),
             InlineKeyboardButton('keyboards', callback_data="{'c':'keyboards_message'}")],
            [InlineKeyboardButton('help', callback_data="{'c':'help'}")],
             ]
        except:
            # default again
            keyboard = [
        [InlineKeyboardButton('italia', callback_data="{'c':'ita'}")],
        [InlineKeyboardButton('start', callback_data="{'c':'start'}"),
         InlineKeyboardButton('geoconfig', callback_data="{'c':'geo','a':'start'}"),
         InlineKeyboardButton('keyboards', callback_data="{'c':'keyboards_message'}")],
         [InlineKeyboardButton('help', callback_data="{'c':'help'}")],
         ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup

def echo_message(update,context):
    update.message.reply_text('🤨 Non capisco che stai dicendo ... 😵')
    update.message.reply_text('🤔 Bisogno di un aiutino? Tappa /help 🙄')
    user_str=UsersDatabase.get_user_str(update.message.chat.id)
    logger.info(user_str + 'typed a wrong message. It was echoed')

# Callbacks

def callback_inline_buttons(update,context):
    # !!! importante: per tutte le funzioni richiamate qui, ho sostituito update.message on update.effective_message per i reply
    # Retreiving data
    # chat_id=update.effective_message.chat_id
    query = update.callback_query
    query.answer()
    import ast
    callback_dict=ast.literal_eval(query.data)
    print("(InlineQuery dictionary: {})".format(callback_dict)) # !!! solo per testing
    
    # Methods
    if callback_dict.get('c')=='start':
        start(update,context)
    elif callback_dict.get('c')=='help':
        help_(update,context)
    elif callback_dict.get('c')=='ita':
        ita(update,context)
    elif callback_dict.get('c')=='reg':
        reg(update,context,callback_dict['d'])
    elif callback_dict.get('c')=='prov':
        prov(update,context,callback_dict['d'])
    elif callback_dict.get('c')=='city':
        city(update,context,callback_dict['d'])
    elif callback_dict.get('c')=='geo':
        # Geoconfig routine
        if callback_dict.get('a')=='start':
            geoconfig(update,context)
        elif callback_dict.get('a')=='save':
            query.edit_message_text(text="Impostazioni salvate con successo 😇 (longitudine: {lon}, latitudine: {lat})".format(lon=callback_dict.get('lon'),lat=callback_dict.get('lat')))
            # !!! salvare sul database le colonne. ho salvato per ora solo lat e long perchè troppi chars per passare alle inline, e anche per avere il tempo di testare meglio geopy
            store_user_lon_lat(chat_id=update.effective_message.chat_id,
                               longitude=callback_dict.get('lon'),
                               latitude=callback_dict.get('lat'))
            reply_markup=get_default_reply_markup(update, context)
            bot.send_message(chat_id=update.effective_message.chat_id, 
                             text="🤖 Ecco le feature che ho filtrato con la tua posizione: ", 
                             reply_markup=reply_markup)
        elif callback_dict.get('a')=='repeat':
            query.edit_message_text(text="Qualcosa è andato storto 🙃, ripetiamo ... puoi anche selezionare tu il punto sulla mappa")
            geoconfig(update,context)
           
def callback_location(update,context):
    
    # Collect location infos
    update.effective_message.reply_text('Posizione ricevuta!')
    location=update.message.location
    longitude=location['longitude']
    latitude=location['latitude']
    user_location=address_from_coordinates(longitude=longitude,latitude=latitude)
    
    # Reply with inline buttons
    txt=f""" Puoi confermare che sei a questo indirizzo: {user_location.get('address',user_location['city'])}? """ 
    keyboard = [
        # main commands
    [InlineKeyboardButton('Si', callback_data="{{'c':'geo','a':'save','lon':{},'lat':{}}}".format(longitude,latitude))],
    [InlineKeyboardButton('No', callback_data="{'c':'geo','a':'repeat'}")],
     ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Reply
    update.effective_message.reply_text(txt, reply_markup=reply_markup)
    
# Admin

def message(update, context):
    """
    By typing /admin message id blabla you can send a message to user with chat_id = 'id' having
    access the bot. /broadcast is hidden telegram-command and only user 1379464630
    has permissions to use it.
    """

    if update.message==None:
        return

    if update.message.text==None:
        return

    if update.message.chat.id in ADMIN_IDS:
        chat_id=update.message.text.split()[2]
        text=update.message.text[update.message.text.find(' ', 15):]
        send_message(chat_id, text)
        user_str=UsersDatabase.get_user_str(update.message.chat.id)
        logger.info(user_str+' sent a message to ' +chat_id)

def broadcast(update,context):
    """
    By typing /admin broadcast blabla you can send a message to all users having
    access the bot. /broadcast is hidden telegram-command and only admins
    have permission to use it.
    """

    if update.message==None:
        return

    if update.message.text==None:
        return

    if update.message.chat.id in ADMIN_IDS:
        text=update.message.text[17:]
        send_message_all_users(text)
        user_str=UsersDatabase.get_user_str(update.message.chat.id)
        logger.info(user_str+' wrote a broadcast message')

def print_users(update, context):
    """
    By typing /admin print_users administrator can receive the list of users in the db
    """
    users=UsersDatabase.get_users()
    users_str=''
    for user in users:
        users_str=users_str+'\n'+user.__str__()
    message='@italycoviddataBot has '+str(len(users))+' users: '+users_str
    bot.send_message(chat_id=update.message.chat.id,text=message)
    user_str=UsersDatabase.get_user_str(update.message.chat.id)
    logger.info(user_str+' ran admin print_users')

def admin(update,context):
    """
    Message the bot with '/admin command_name' for administrators functions.
    """
    if update.message==None:
        return

    if update.message.text==None:
        return
    else:
        command = update.message.text.split()[1]

    if update.message.chat.id not in ADMIN_IDS:
        text='Non sei autorizzato, mi dispiace. Contatta gli admins!'
        bot.send_message(chat_id=update.message.chat.id,text=text)
        user_str=UsersDatabase.get_user_str(update.message.chat.id)
        logger.warning(user_str + 'tryied to launch some admin-functions')
        return

    current_module = sys.modules[__name__]
    func = getattr(current_module, command, -1)
    if func == -1:
        text='Il comando \'' + command + '\' non esiste, riprova con un comando valido.'
        bot.send_message(chat_id=update.message.chat.id,text=text)
    else:
        func(update, context)

# Main

def main():

    # Instancing updated and dispatcher
    updater= Updater(config['BOT_SETTINGS']['TOKEN'], use_context=True)
    dispatcher = updater.dispatcher

    # Daily updater
    d = datetime.datetime.now()
    timezone = pytz.timezone("Europe/Rome")
    d_aware = timezone.localize(d)
    notify_time = datetime.time(18, 5, 0, 0, tzinfo=d_aware.tzinfo)
    updater.job_queue.run_daily(__daily_bot_update, time=notify_time)

    # Handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_))
    dispatcher.add_handler(CommandHandler('geoconfig', geoconfig))
    dispatcher.add_handler(CommandHandler("world", world))
    dispatcher.add_handler(CommandHandler("ita", ita))
    dispatcher.add_handler(CommandHandler("reg", reg))
    dispatcher.add_handler(CommandHandler("prov", prov))
    dispatcher.add_handler(CommandHandler("city", city))
    dispatcher.add_handler(CommandHandler("admin", admin)) # __ADMINS__
    
    # Special handlers
    dispatcher.add_handler(MessageHandler(Filters.location, callback_location))
    dispatcher.add_handler(CallbackQueryHandler(callback_inline_buttons))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo_message))
    
    # Custom keyboards
    dispatcher.add_handler(CommandHandler("keyboards", keyboards_message))
    for member in getmembers(keyboards):
        if isfunction(member[1]):
            dispatcher.add_handler(CommandHandler(member[0], member[1]))

    # Polling
    updater.start_polling()
    updater.idle()

### MAIN

if __name__=='__main__':
    
    # Loading data from server
    day_start='20200224' # format YYYYMMDD. To start .csv data of provinces.
    load_df_italy()
    load_df_regions()
    load_df_provinces()

    # Routine
    bot = telegram.Bot(token=config['BOT_SETTINGS']['TOKEN'])
    main()
