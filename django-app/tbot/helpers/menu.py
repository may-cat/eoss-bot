from telegram import (
    Poll,
    ParseMode,
    KeyboardButton,
    KeyboardButtonPollType,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    Updater,
    CommandHandler,
    PollAnswerHandler,
    PollHandler,
    MessageHandler,
    Filters,
    CallbackContext,
    CallbackQueryHandler
)

class Menu():

    LABEL_EOSS_START = 'Запустить ЭОСС'
    LABEL_STATS = 'Посмотреть результаты ЭОСС'
    LABEL_LIST_MY_PROPERTY = 'Посмотреть свои объекты недвижимости'
    LABEL_CHANGE_MY_PROPERTY = 'Изменить свои объекты недвижимости'

    pass
