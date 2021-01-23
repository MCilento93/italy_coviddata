
### MODULES

import telegram, configparser
from telegram import KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, Filters, MessageHandler, CommandHandler, CallbackQueryHandler, CallbackContext

### FOLDERS

MODULE_DIR = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
SW_DIR=os.path.dirname(MODULE_DIR)

# Settings
config = configparser.ConfigParser()
config.read(os.path.join(SW_DIR,'config.ini'))

### METHODS

def get_default_reply_markup(update,context):

    print(f'getting user {update.effective_message.chat_id} data ...')
    """
    user=UsersDatabase.get_user(update.effective_message.chat_id)
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

    if user.get('city',False):
        keyboard = [
            # main commands
        [InlineKeyboardButton('italia', callback_data="{'c':'ita'}")],
        [InlineKeyboardButton('tua regione', callback_data=f"{{'c':'reg','d':'{user['region']}'}}")],
        [InlineKeyboardButton('tua provincia', callback_data=f"{{'c':'prov','d':'{user['province']}'}}")],
        [InlineKeyboardButton('tua città', callback_data=f"{{'c':'city','d':'{user['city']}'}}")],
        [InlineKeyboardButton('start', callback_data="{'c':'start'}"),
         InlineKeyboardButton('geoconfig', callback_data="{'c':'geo','a':'start'}"),
         InlineKeyboardButton('keyboards', callback_data="{'c':'keyboards_message'}")],
        [InlineKeyboardButton('help', callback_data="{'c':'help'}")],
         ]
        reply_markup = InlineKeyboardMarkup(keyboard)
    else:
        keyboard = [
            # main commands
        [InlineKeyboardButton('italia', callback_data="{'c':'ita'}")],
        [InlineKeyboardButton('start', callback_data="{'c':'start'}"),
         InlineKeyboardButton('geoconfig', callback_data="{'c':'geo','a':'start'}"),
         InlineKeyboardButton('keyboards', callback_data="{'c':'keyboards_message'}")],
         [InlineKeyboardButton('help', callback_data="{'c':'help'}")],
         ]
        reply_markup = InlineKeyboardMarkup(keyboard)

    return reply_markup

def start(update, context):

    # Reply with inline buttons
    txt=""" Start you geoconfiguration by /geoconfig or click below: """
    # keyboard = [
    #     # main commands
    # [InlineKeyboardButton('start', callback_data="{'command':'start'}")],
    # [InlineKeyboardButton('geoconfig', callback_data="{'command':'geoconfig','action':'start'}")],
    #     # leaving
    #  [InlineKeyboardButton('help', callback_data="{'command':'help'}")]
    #  ]
    # reply_markup = InlineKeyboardMarkup(keyboard)
    reply_markup=get_default_reply_markup(update,context)

    # Reply
    update.effective_message.reply_text(txt, reply_markup=reply_markup)
    # bot.send_message(chat_id=update.effective_message.chat_id,
    # update.message.reply_text(txt, reply_markup=reply_markup)

def help(update,context):
    txt='Click /start to proceed'
    update.effective_message.reply_text(txt)

def geoconfig(update,context):
    location_keyboard = telegram.KeyboardButton(text="📍 Manda la tua posizione GPS", request_location=True)
    custom_keyboard = [[ location_keyboard]]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard,resize_keyboard=True)
    txt="""Vuoi condividere la tua posizione con me? Attiva il GPS ... Se ci sono problemi, mandamela direttamente tu, ok? ☺️"""
    bot.send_message(chat_id=update.effective_message.chat_id,
                     text=txt,
                     reply_markup=reply_markup)

def reg(update,context,reg_name=None):
    if reg_name:
        # new routine
        update.effective_message.reply_text('nuova routine per '+reg_name)
    else:
        # traditional routine (for getting reg_name)
        reg_name=update.message.text.split(' ')[1:]
        reg_name=' '.join(reg_name)
        update.effective_message.reply_text('routine tradizionale per '+reg_name)

def address_from_coordinates(longitude=14.718719,latitude=40.718220):
    from geopy.geocoders import Nominatim
    geolocator = Nominatim(user_agent="italycoviddataBot")
    coordinates=str(latitude)+','+str(longitude)
    location = geolocator.reverse(coordinates)
    print('#------User Location Sent------#')
    print(f'Coordinates: {coordinates}')
    print(f'Location: {location}')
    user_location={}
    user_location['reg']=location.raw['address'].get('state',None)
    user_location['prov']=location.raw['address'].get('county',None)
    try:
        user_location['city']=location.raw['address']['city']
    except:
        try:
            user_location['city']=location.raw['address']['town']
        except:
            try:
                user_location['city']=location.raw['address']['village']
            except:
                try:
                    user_location['city']=location.raw['address'].get('county')
                except:
                    print('cannot find city')
    user_location['address']=location.raw['display_name']
    print(f'Summary for italycoviddata: {user_location}')
    print('#------------------------------#')
    return user_location

def callback_location(update,context):

    # Collect location infos
    update.effective_message.reply_text('Posizione ricevuta!')
    location=update.message.location
    longitude=location['longitude']
    latitude=location['latitude']

    user_location=address_from_coordinates(longitude=longitude,latitude=latitude)

    # Reply with inline buttons
    txt=f""" Puoi confermare che sei a questo indirizzo: {user_location['address']}? """
    # longitude_str=str(longitude)
    # latitude_str=str(latitude)
    # yes_string=f"""{
    #                  {'command':'geoconfig',
    #                   'action':'save',
    #                   'longitude':longitude_str,
    #                   'latitude':latitude_str}
    #                  }"""
    yes_string="{{'c':'geo','a':'save','lon':{},'lat':{}}}".format(longitude,latitude)
    print(yes_string)

    keyboard = [
        # main commands
    [InlineKeyboardButton('Si', callback_data=yes_string)],
    [InlineKeyboardButton('No', callback_data="{'c':'geo','a':'repeat'}")],
     ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Reply
    update.effective_message.reply_text(txt, reply_markup=reply_markup)
    # bot.send_message(chat_id=update.effective_message.chat_id,
    #                  text=txt,
    #                  reply_markup=reply_markup)

def callback_inline_buttons(update,context):

    # Retreiving data
    chat_id=update.effective_message.chat_id
    query = update.callback_query
    query.answer()
    import ast
    callback_dict=ast.literal_eval(query.data)
    print("(InlineQuery dictionary: {})".format(callback_dict))

    # Methods
    if callback_dict.get('c')=='start':
        start(update,context)
    elif callback_dict.get('c')=='help':
        help(update,context)
    elif callback_dict.get('c')=='reg':
        reg(update,context,callback_dict['d'])
    elif callback_dict.get('c')=='geo':
        # Geoconfig
        if callback_dict.get('a')=='start':
            geoconfig(update,context)
        elif callback_dict.get('a')=='save':
            query.edit_message_text(text="Impostazioni salvate con successo 😇 (latitudine: {lat}, longitudine: {lon})".format(lat=callback_dict.get('lat'),lon=callback_dict.get('lon')))
            reply_markup=get_default_reply_markup(update, context)
            bot.send_message(chat_id=update.effective_message.chat_id,
                             text="Ecco le feature che ho filtrato con la tua posizione: ",
                             reply_markup=reply_markup)
        elif callback_dict.get('a')=='repeat':
            query.edit_message_text(text="Qualcosa è andato storto 🙃, ripetiamo ... puoi anche selezionare tu il punto dalla mappa")
            geoconfig(update,context)

def main():
    # Create the Updater
    updater = Updater(TOKEN, use_context=True)

    # Commands
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_handler(CommandHandler('geoconfig', geoconfig))
    updater.dispatcher.add_handler(CommandHandler('reg', reg))

    # Special-handlers
    updater.dispatcher.add_handler(MessageHandler(Filters.location, callback_location))
    updater.dispatcher.add_handler(CallbackQueryHandler(callback_inline_buttons))

    # Start the Bot
    updater.start_polling()

    # Run the bot
    updater.idle()

### MAIN

if __name__ == '__main__':
    TOKEN=config['TEST_BOT_SETTINGS']['TOKEN']
    bot = telegram.Bot(token=TOKEN)
    main()
