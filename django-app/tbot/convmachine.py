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

    """
    Scenarios
    """
    states = {
        'start': {
            1: { 'class': CommandHandler, 'filter': 'start', 'function': Start.handle }
        },
        'eoss_initiate': {
            1: { 'class': MessageHandler, 'filter': Filters.regex(menu['LABEL_EOSS_START']), 'function': Eoss.handle , 'next_possible': ['eoss_initiate.4','eoss_initiate.5'] },
            2: { 'class': MessageHandler, 'filter': Filters.poll,                            'function': ReceivePoll.handle },
            3: { 'class': MessageHandler, 'filter': Filters.regex(BUTTON_RUN),               'function': EossDataRecieved.handle },
            # 3: MessageHandler(Filters.regex(BUTTON_CANCEL), EossDataCancelled.handle),
        },
        'poll_answering': {
            1: { 'class': PollAnswerHandler, 'function': ReceivePollAnswer.handle },
        },
        'stats': {
            1: { 'class': MessageHandler, 'filter': Filters.regex(menu['LABEL_STATS']), 'function': EossStats.handle }
        },
        'property_list': {
            1: { 'class': MessageHandler, 'filter': Filters.regex(menu['LABEL_LIST_MY_PROPERTY']), 'function': Help.handle }
        },
        'property_edit': {
            1: { 'class': MessageHandler, 'filter': Filters.regex(menu['LABEL_CHANGE_MY_PROPERTY']), 'function': Help.handle }
        },
        'help': {
            1: {'class': CommandHandler, 'filter': 'help', 'function': Help.handle }
        }
    }

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

    def __init__(self, states: dict):
        pass

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
                if possible_state['filter'](update):
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
