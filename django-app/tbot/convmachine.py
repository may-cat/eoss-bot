import logging
from .settings import API_KEY, BUTTON_RUN, BUTTON_CANCEL
from .helpers.menu import Menu

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
    Dispatcher,
    CommandHandler,
    PollAnswerHandler,
    PollHandler,
    MessageHandler,
    Filters,
    CallbackContext,
    CallbackQueryHandler
)
from models import *
from handlers.eoss import Eoss
from handlers.eoss_data_cancelled import EossDataCancelled
from handlers.eoss_data_received import EossDataRecieved
from handlers.eoss_stats import EossStats
from handlers.help_handler import Help
from handlers.receive_poll import ReceivePoll
from handlers.receive_poll_answer import ReceivePollAnswer
from handlers.start import Start

class ConversationMachine():
    menu = {
        "LABEL_EOSS_START": 'Запустить ЭОСС',
        "LABEL_STATS": 'Посмотреть результаты ЭОСС',
        "LABEL_LIST_MY_PROPERTY": 'Посмотреть свои объекты недвижимости',
        "LABEL_CHANGE_MY_PROPERTY": 'Изменить свои объекты недвижимости'
    }

    states = {
        'start': {
            1: CommandHandler('start', Start.handle)
        },
        'eoss_initiate': {
            1: MessageHandler(Filters.regex(menu['LABEL_EOSS_START']), Eoss.handle),
            2: MessageHandler(Filters.poll, ReceivePoll.handle),
            3: MessageHandler(Filters.regex(BUTTON_RUN), EossDataRecieved.handle),
            # 3: MessageHandler(Filters.regex(BUTTON_CANCEL), EossDataCancelled.handle),
        },
        'poll_answering': {
            1: PollAnswerHandler(ReceivePollAnswer.handle),
        },
        'stats': {
            1: MessageHandler(Filters.regex(menu['LABEL_STATS']), EossStats.handle)
        },
        'property_list': {
            1: MessageHandler(Filters.regex(menu['LABEL_LIST_MY_PROPERTY']), Help.handle)
        },
        'property_edit': {
            1: MessageHandler(Filters.regex(menu['LABEL_CHANGE_MY_PROPERTY']), Help.handle)
        },
        'help': {
            1: CommandHandler('help', Help.handle)
        }
    }

    def __init__(self, states: dict):
        pass

    def register_handlers(self, dispatcher: Dispatcher):
        # TODO: run through all states and register handlers in dispacher
        pass

    def can_proceed(self, user: User):
        """
        TODO:
                Надо будет заюзать:
                https://stackoverflow.com/questions/2654113/how-to-get-the-callers-method-name-in-the-called-method
                На основании имени метода, который вызвал, сценария в self.states и состояния текущего юзера — надо понять можно ли продолжать
        :return:
        """
        pass