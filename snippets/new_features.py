
### MODULES
import logging, telegram, configparser
from telegram import KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, Filters, MessageHandler, CommandHandler, CallbackQueryHandler, CallbackContext
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

### FOLDERS

MODULE_DIR = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
SW_DIR=os.path.dirname(MODULE_DIR)

# Settings
config = configparser.ConfigParser()
config.read(os.path.join(SW_DIR,'config.ini'))

### METHODs

def start(update: Update, context: CallbackContext) -> None:

    # Geolocation
    update.message.reply_text(text=location_info_from_coordinates().__str__())

    # Caller-data
    command=update.message.text.split(' ')[1:]
    command=' '.join(command)
    callback_data_dict={'id':update.message.chat.id,
                        'command':command}
    callback_data_dict_str=str(callback_data_dict)

    # Buttons
    keyboard = [
        # main commands
        [InlineKeyboardButton('Italy', callback_data=callback_data_dict_str)],
        [InlineKeyboardButton('Region', callback_data=callback_data_dict_str)],
        [InlineKeyboardButton('Province', callback_data=callback_data_dict_str)],
        [InlineKeyboardButton('City', callback_data=callback_data_dict_str)],
        # leaving
        [InlineKeyboardButton('start', callback_data='start'),
         InlineKeyboardButton('help', callback_data='help')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose:', reply_markup=reply_markup)


def inline_buttons(update: Update, context: CallbackContext) -> None:
    """ CallbackQueries need to be answered, even if no notification to the user is needed
    Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery """

    # Retreiving data
    import ast
    query = update.callback_query
    query.answer()
    callback_dat_dict=ast.literal_eval(query.data)
    print(callback_dat_dict)

    # Methods
    if callback_dat_dict=='start':
        start(update,context) # !!! not working !!!
    else:
        query.edit_message_text(text="Selected option: {}".format(callback_dat_dict))
    # query.edit_message_text(text="Selected option: {}".format(callback_dat_dict))

def shortcuts(update: Update, context: CallbackContext) -> None:

    # Fixed keyboard
    custom_keyboard = [
        # main commands
        ['1'],
        ['2'],
        ['3'],
        ['1'],
        ['2'],
        ['3'],
        ['1'],
        ['2'],
        ['3'],
        ['1'],
        ['2'],
        ['3'],
        ['1'],
        ['2'],
        ['3'],
        ['1'],
        ['2'],
        ['3'],
        ['1'],
        ['2'],
        ['3'],
        ['1'],
        ['2'],
        ['3'],
    ]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard,resize_keyboard=True)
    update.message.reply_text(text="Custom Keyboard Test",reply_markup=reply_markup)

def keyboard_query_location(update: Update, context: CallbackContext) -> None:
    location_keyboard = telegram.KeyboardButton(text="send location", request_location=True)
    contact_keyboard = telegram.KeyboardButton(text="send contact", request_contact=True)
    custom_keyboard = [[ location_keyboard, contact_keyboard ]]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    bot = telegram.Bot(token=TOKEN)
    bot.send_message(chat_id=update.message.chat.id,
                     text="Would you mind sharing your location and contact with me?",
                     reply_markup=reply_markup)

def test_location_1(update: Update, context: CallbackContext) -> None:
    if update.edited_message:
        message = update.edited_message
    else:
        message = update.message
    current_pos = (message.location.latitude, message.location.longitude)
    print(current_pos)

def test_location_2(bot, update):
    print(update.message.location)

def location_info_from_coordinates(lat=40.718220,long=14.718719):
    from geopy.geocoders import Nominatim
    geolocator = Nominatim(user_agent="just_a_test")
    coordinates=str(lat)+','+str(long)
    location = geolocator.reverse(coordinates)
    user_location={}
    user_location['country']=location.raw['address']['country']
    user_location['region']=location.raw['address']['state']
    user_location['province']=location.raw['address']['county']
    user_location['city']=location.raw['address']['town']
    user_location['address']=location.raw['display_name']
    print(user_location)
    return user_location

def send_location(update,context):
    print('ci siamo')
    print(update.message.location)

def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Commands
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('shortcuts', shortcuts))
    updater.dispatcher.add_handler(CommandHandler('test_location', keyboard_query_location))

    # Special-handlers
    updater.dispatcher.add_handler(MessageHandler(Filters.location, send_location))
    updater.dispatcher.add_handler(CallbackQueryHandler(inline_buttons))

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    updater.idle()

### MAIN

if __name__ == '__main__':
    TOKEN=config['TEST_BOT_SETTINGS']['TOKEN']
    main()
