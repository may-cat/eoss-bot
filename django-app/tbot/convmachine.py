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
            1: { 'class': MessageHandler, 'filter': Filters.regex(menu['LABEL_EOSS_START']), 'function': Eoss.handle },
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

    def register_handlers(self, dispatcher: Dispatcher):
        """
        TODO: тут сложная хуёмбола.
                Надо пробежаться по всему, что у нас есть и зарегать все хэндлеры по классам, что объявлены.
                На наши кастомные хэндлеры.
                В этих наших кастомных хэндлерах надо
                    а) смотреть на состояние конкретного юзера
                    б) смотреть на объявленный фильтр, типа вот так:
                        filter(update)
                и исходя из этого запускать функцию указанную

        :param dispatcher:
        :return:
        """
        pass

    def _custom_handler(self, update: Update, context: CallbackContext) -> None:
        # TODO: загружаем юзера
        user = User()

        try:
            user_state = self._get_user_state(user)

            called = False
            for possible_state in self._get_next_possible_states(self.states, user_state):
                if self._does_message_match_state(update, context, possible_state):
                    self._run_state(update, context, possible_state)
                    called = True
            if not called:
                raise ScenarioFailed()
        except Exception as e:
            for exception_type in self.fallbacks.keys():
                if isinstance(e, exception_type):
                    self.fallbacks[exception_type]['function'](update=update, context=context)
                    pass

    def _get_user_state(self, user):
        # TODO: прочитать юзера, его свойство
        # TODO: проверить, что значения в свойстве хоть как-то укладывается в self.state, если нет — откатываем на какое-то другое состояние
        # TODO: превратить в UserState объект

        return ['start', 1]

    def _get_next_possible_states(self):
        return [
            { 'class': MessageHandler, 'filter': Filters.regex(BUTTON_RUN),               'function': EossDataRecieved.handle },
            { 'class': MessageHandler, 'filter': Filters.regex(BUTTON_CANCEL),            'function': EossDataCancelled.handle },
        ]

    def _does_message_match_state(self, update: Update, context: CallbackContext, state) -> bool:
        # TODO: ....
        return True

    def _run_state(self, update: Update, context: CallbackContext, state) -> None:
         pass
