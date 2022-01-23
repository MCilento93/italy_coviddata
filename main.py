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
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from ColoreRegioni import ColoreRegioni

# From package
import coviddata.world_coviddata as world_coviddata
import coviddata.italy_coviddata_curvefit as italy_coviddata_curvefit
import coviddata.italy_coviddata_regions as italy_coviddata_regions
import coviddata.italy_coviddata_provinces as italy_coviddata_provinces
import coviddata.italy_coviddata_cities as italy_coviddata_cities
import coviddata.italy_coviddata_vaccines as italy_coviddata_vaccines
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
    user_str=UsersDatabase.get_user_str(message.chat.id)
    logger.info(user_str + ' added to bot-database')

# Upload Dataframes

def __daily_bot_update(CallbackContext):
    # Update
    current_time_italy=datetime.datetime.now().astimezone(pytz.timezone('Europe/Rome'))
    date_now=current_time_italy.strftime('%Y-%m-%d %H:%M')
    print('\n- '+date_now+' daily update of dataframes ... ')
    load_df_italy()
    load_df_regions()
    load_df_provinces()
    load_df_vaccines()
    # Notification
    nuovi_positivi_italy=int(df_italy['nuovi_positivi'].values[-1])
    morti_giornalieri=int(df_italy['nuovi_deceduti'].values[-1])
    tot_dosi_somministrate=df_vax['dosi_somministrate'].sum()
    tot_popolazione=df_vax['tot_popolazione'].sum()
    percentuale_vaccinati=tot_dosi_somministrate/tot_popolazione/2
    notification_message=f"""
🦠COVID-19🧪 aggiornamento dati
{nuovi_positivi_italy} nuovi positivi e {morti_giornalieri} morti giornalieri in Italia  🇮🇹
Complessivamente sono stati distribuiti {int(tot_dosi_somministrate)} vaccini 💉
    """
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

def load_df_vaccines():
    global df_vax
    df_vax=italy_coviddata_vaccines.load_full_repository()

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
/ita - Dati nazionali aggiornati (e dati sui vaccini)
/reg - Seguito da nome della regione per i dati regionali (e dati sui vaccini)
/prov - Seguito da nome della provincia per i dati provinciali
/city - Seguito da nome della città desiderata per un tentativo di ricerca dati

*Custom-keyboards*
Sono arrivate le tastiere custom per @italycoviddataBot
Queste ti semplificheranno la vita enormemente ... farai a meno della tastiera del telefono
Digita /keyboards per avere la lista di tastiere disponibili

*Colore Regioni*
Vuoi conoscere il colore della tua regione e le rispettive restrizioni? Schiaccia subito /colore\_regioni

*About me*
Questo bot è basato sui dati della [protezione civile](https://github.com/pcm-dpc/COVID-19).
Il software è completamente gratuito e fa parte del progetto [italy_covidddata](https://github.com/MCilento93/italy_coviddata).
"""
    update.effective_message.reply_text(txt,parse_mode='Markdown',disable_web_page_preview=True)

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
    update.message.reply_text(italy_coviddata_curvefit.get_resume(df_italy),parse_mode='Markdown')
    update.message.reply_text(italy_coviddata_vaccines.get_italy_resume(df_vax),parse_mode='Markdown')
    user_str=UsersDatabase.get_user_str(update.message.chat.id)
    logger.info(user_str+' asked for italy-data')

def reg(update,context):
    reg_name=update.message.text.split(' ')[1:]
    reg_name=' '.join(reg_name)
    user_str=UsersDatabase.get_user_str(update.message.chat.id)
    if reg_name in df_regions.denominazione_regione.values:
        rd1=italy_coviddata_regions.CovidItalyRegion(df_regions, reg_name, day_start)
        fig=rd1.plot_resume()
        fig_bytes=fig2bytes(fig)
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=fig_bytes)
        resume=rd1.get_resume()
        update.message.reply_text(resume,parse_mode='Markdown')
        update.message.reply_text(italy_coviddata_vaccines.get_region_resume(df_vax, reg_name),parse_mode='Markdown')
        logger.info(user_str +' asked for '+reg_name+' data')
    else:
        reg_names_array=np.unique(df_regions.denominazione_regione.values)
        reg_names_str='\n'.join(reg_names_array)
        update.message.reply_text('🤔 Scrivi bene il nome della regione')
        update.message.reply_text('Le regioni consentite sono: \n'+reg_names_str)
        logger.warning(user_str+' typed a wrong region name ('+reg_name+')')

def prov(update,context):
    prov_name=update.message.text.split(' ')[1:]
    prov_name=' '.join(prov_name)
    user_str=UsersDatabase.get_user_str(update.message.chat.id)
    if prov_name in df_provinces.denominazione_provincia.values:
        pd1=italy_coviddata_provinces.CovidItalyProvince(df_provinces, prov_name, day_start)
        fig=pd1.plot_resume()
        fig_bytes=fig2bytes(fig)
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=fig_bytes)
        resume=pd1.get_resume()
        update.message.reply_text(resume,parse_mode='Markdown')
        logger.info(user_str+' asked for '+prov_name+' data')
    else:
        prov_names_array=np.unique(df_provinces.denominazione_provincia.values)
        prov_names_str='\n'.join(prov_names_array)
        update.message.reply_text('🤨 Scrivi bene il nome della provincia')
        update.message.reply_text('Le provincie consentite sono: \n'+prov_names_str)
        logger.warning(user_str+' typed a wrong province name ('+prov_name+')')

def city(update,context):
    city_name=update.message.text.split(' ')[1:]
    city_name=' '.join(city_name)
    update.message.reply_text('Mi vuoi mettere proprio alla prova 👨🏻‍💻, eh? ... provo ad estrarre i dati più aggiornati che trovo 🤔')
    update.message.reply_text(italy_coviddata_cities.get_resume(city_name),parse_mode='Markdown',disable_web_page_preview=True)
    user_str=UsersDatabase.get_user_str(update.message.chat.id)
    logger.info(user_str+' asked for '+city_name+' data')

def colore_regioni(update,context):
    colore_regioni=ColoreRegioni()
    dict_only_emoji=colore_regioni.emoji
    reply_with_emoji=''
    for key,value in dict_only_emoji.items():
        reply_with_emoji+=f"{value} {key}\n"
    reply_with_emoji+="""
[FAQ del Governo](http://www.governo.it/it/articolo/domande-frequenti-sulle-misure-adottate-dal-governo/15638?gclid=CjwKCAiAwrf-BRA9EiwAUWwKXicC1bzopYynHP9pvRxHUza7Ar4dte9hWHi55Uj4xfuAHanOCf7a1BoCTggQAvD_BwE)
"""
    update.message.reply_text(reply_with_emoji,parse_mode='Markdown',disable_web_page_preview=True)
    user_str=UsersDatabase.get_user_str(update.message.chat.id)
    logger.info(user_str+' asked for colore regioni')

def keyboards_message(update,context):
    user_str=UsersDatabase.get_user_str(update.message.chat.id)
    logger.info(user_str+' asked list of keyboards')
    list_keyboards=[]
    for member in getmembers(keyboards):
        if isfunction(member[1]):
            list_keyboards.append(member)
    list_keyboards_str=''.join([f'\n• /{keyboard_name[0]}' for keyboard_name in list_keyboards])
    update.message.reply_text("Lista delle ⌨️ keyboards-personalizzate disponibili:"+list_keyboards_str)

def echo_message(update,context):
    update.message.reply_text('🤨 Non capisco che stai dicendo ... 😵')
    update.message.reply_text('🤔 Bisogno di un aiutino? Tappa qui /help 🙄')
    user_str=UsersDatabase.get_user_str(update.message.chat.id)
    logger.info(user_str + 'typed a wrong message. It was echoed')

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
    message='@italycoviddataBot has '+str(len(users))+' users: \n'+users_str[-3000:]
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

    # Assign commands
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_))
    dispatcher.add_handler(CommandHandler("world", world))
    dispatcher.add_handler(CommandHandler("ita", ita))
    dispatcher.add_handler(CommandHandler("reg", reg))
    dispatcher.add_handler(CommandHandler("prov", prov))
    dispatcher.add_handler(CommandHandler("city", city))
    dispatcher.add_handler(CommandHandler("colore_regioni", colore_regioni))
    dispatcher.add_handler(CommandHandler("admin", admin)) # __ADMINS__
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
    load_df_vaccines()

    # Routine
    bot = telegram.Bot(token=config['BOT_SETTINGS']['TOKEN'])
    main()
