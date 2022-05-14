import logging
from .settings import API_KEY, BUTTON_RUN, BUTTON_CANCEL

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
from handlers.receive_verification_request import ReceiveVerificationRequest
from handlers.start import Start
from exceptions.needs_verification import UserNeedsVerification
from exceptions.scenario_failed import ScenarioFailed
from exceptions.contact_admin import ContactAdmin
import jmespath


class ConversationMachine():
    menu = {
        "LABEL_EOSS_START": 'Запустить ЭОСС',
        "LABEL_STATS": 'Посмотреть результаты ЭОСС',
        "LABEL_LIST_MY_PROPERTY": 'Посмотреть свои объекты недвижимости',
        "LABEL_CHANGE_MY_PROPERTY": 'Изменить свои объекты недвижимости'
    }

    states = {}

    """
    Scenarios runned on exceptions
    """
    fallbacks = {
        UserNeedsVerification: {
            'function': ReceiveVerificationRequest.handle,
        },
        ScenarioFailed: {
            # TODO: ....
        },
        ContactAdmin: {
            'function': Help.handle
        },
        Exception: {
            'function': Help.handle
        }
    }

    def __init__(self):
        """
        Scenarios

        TODO: прописать next_possible
        """
        self.states = {}
        self.states['start'] = {
            1: {
                'class': CommandHandler,
                'filter': 'start',
                'handler': Start(self)
            }
        }
        self.states['eoss_initiate'] = {
            1: {
                '_comment': "Объясняем пользователю, как инициировать ЭОСС",
                'class': MessageHandler,
                'filter': Filters.regex(self.menu['LABEL_EOSS_START']),
                'handler': Eoss(self) ,
                'next_possible': ['eoss_initiate.2'],
            },
            2: {
                '_comment': "Получаем от пользователя опрос и в ответ предлагаем либо запустить его, либо отменить",
                'class': MessageHandler,
                'filter': Filters.poll,
                'handler': ReceivePoll(self),
                'next_possible': ['eoss_initiate.3','eoss_initiate.4']
            },
            3: {
                '_comment': "Пользователь заказал запуск опроса",
                'class': MessageHandler,
                'filter': Filters.regex(BUTTON_RUN),
                'handler': EossDataRecieved(self),
                'next_possible': ['help.1']
            },
            4: {
                '_comment': "Пользователь заказал отмену запуска опроса",
                'class': MessageHandler,
                'filter': Filters.regex(BUTTON_CANCEL),
                'handler': EossDataCancelled(self),
                'next_possible': ['help.1']
            },
        }
        self.states['poll_answering'] = {
            1: {
                '_comment': "Пользователи оставляют голоса в публичной группе",
                'class': PollAnswerHandler,
                'handler': ReceivePollAnswer(self)
            },
        },
        self.states['stats'] = {
            1: {
                'class': MessageHandler,
                'filter': Filters.regex(self.menu['LABEL_STATS']),
                'handler': EossStats(self)
            }
        }
        self.states['property_list'] = {
            1: {
                'class': MessageHandler,
                'filter': Filters.regex(self.menu['LABEL_LIST_MY_PROPERTY']),
                'handler': Help(self)
            }
        },
        self.states['property_edit'] = {
            1: {
                'class': MessageHandler,
                'filter': Filters.regex(self.menu['LABEL_CHANGE_MY_PROPERTY']),
                'handler': Help(self)
            }
        },
        self.states['help'] = {
            1: {
                'class': CommandHandler,
                'filter': 'help',
                'function': Help(self)
            }
        }


    """
    As soon as we filter not only by handler type, but also by current step and user's state
    we need an adapter, which catches messages, commands and poll answers
    and passes them through our business logic.
    """
    def register_handlers(self, dispatcher: Dispatcher):
        dispatcher.add_handler(MessageHandler(self._custom_message_handler))
        dispatcher.add_handler(CommandHandler(eoss_data_received)) # TODO: ...
        dispatcher.add_handler(PollAnswerHandler(eoss_data_received)) # TODO: ...

    def _custom_message_handler(self, update: Update, context: CallbackContext) -> None:
        self._basic_handler(update, context, MessageHandler)

    def _basic_handler(self, update: Update, context: CallbackContext, handler_type):
        # TODO: загружаем юзера
        user = User()

        try:
            user_state = user.get_dialog_state()
            for path, possible_state in self._get_next_possible_states(user_state, handler_type).items():
                if possible_state['filter'](update): # TODO: это сломается когда filter будет не указан, либо когда он будет строкой, а не объектом
                    possible_state['function'](update, context, user)
                    user.set_dialog_state(path)
                    return
            raise ScenarioFailed()
        except Exception as e:
            for exception_type in self.fallbacks.keys():
                if isinstance(e, exception_type):
                    self.fallbacks[exception_type]['function'](update=update, context=context)
                    pass

    """
    Возвращает какие шаги дальше могут быть
    """
    def _get_next_possible_states(self, path: str, handler_type):
        result = {}
        current_state = jmespath.search(path, self.states)
        next_possible = current_state['next_possible']
        for item in next_possible:
            next_state = jmespath.search(item, self.states)
            if next_state['class'] == handler_type:
                result[item] = next_state
        return result
