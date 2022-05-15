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
from .helpers.telegramchats import Telegramchats
from .models import *
from .handlers.eoss import Eoss
from .handlers.eoss_data_cancelled import EossDataCancelled
from .handlers.eoss_data_received import EossDataRecieved
from .handlers.eoss_stats import EossStats
from .handlers.help_handler import Help
from .handlers.receive_poll import ReceivePoll
from .handlers.receive_poll_answer import ReceivePollAnswer
from .handlers.receive_verification_request import ReceiveVerificationRequest
from .handlers.start import Start
from .handlers.menu import Menu
from .exceptions.needs_verification import UserNeedsVerification
from .exceptions.scenario_failed import ScenarioFailed
from .exceptions.contact_admin import ContactAdmin
from .exceptions.fallback_to_menu import FallbackToMenu
import jmespath
import sys
import traceback


class ConversationMachine():
    menu = {
        "LABEL_EOSS_START": 'Запустить ЭОСС',
        "LABEL_STATS": 'Посмотреть результаты ЭОСС',
        "LABEL_LIST_MY_PROPERTY": 'Посмотреть свои объекты недвижимости',
        "LABEL_CHANGE_MY_PROPERTY": 'Изменить свои объекты недвижимости'
    }

    states = {}
    fallbacks = {}

    def __init__(self):
        """
        Scenarios

        TODO: прописать next_possible
        """
        self.states = {}
        self.states['start'] = [
            {},
            {
                'class': CommandHandler,
                'filter': Filters.regex("\/start"),
                'handler': Start(self)
            }
        ]
        self.states['eoss_initiate'] = [
            {},
            {
                '_comment': "Объясняем пользователю, как инициировать ЭОСС",
                'class': MessageHandler,
                'filter': Filters.regex(self.menu['LABEL_EOSS_START']),
                'handler': Eoss(self) ,
                'next_possible': ['eoss_initiate[2]'],
            },
            {
                '_comment': "Получаем от пользователя опрос и в ответ предлагаем либо запустить его, либо отменить",
                'class': MessageHandler,
                'filter': Filters.poll,
                'handler': ReceivePoll(self),
                'next_possible': ['eoss_initiate[3]','eoss_initiate[4]']
            },
            {
                '_comment': "Пользователь заказал запуск опроса",
                'class': MessageHandler,
                'filter': Filters.regex(BUTTON_RUN),
                'handler': EossDataRecieved(self),
                'next_possible': ['help[1]']
            },
            {
                '_comment': "Пользователь заказал отмену запуска опроса",
                'class': MessageHandler,
                'filter': Filters.regex(BUTTON_CANCEL),
                'handler': EossDataCancelled(self),
                'next_possible': ['help[1]']
            },
        ]
        self.states['poll_answering'] = [
            {},
            {
                '_comment': "Пользователи оставляют голоса в публичной группе",
                'class': PollAnswerHandler,
                'handler': ReceivePollAnswer(self)
            }
        ]
        self.states['stats'] = [
            {},
            {
                'class': MessageHandler,
                'filter': Filters.regex(self.menu['LABEL_STATS']),
                'handler': EossStats(self)
            }
        ]
        self.states['property_list'] = [
            {},
            {
                'class': MessageHandler,
                'filter': Filters.regex(self.menu['LABEL_LIST_MY_PROPERTY']),
                'handler': Help(self)
            }
        ]
        self.states['property_edit'] = [
            {},
            {
                'class': MessageHandler,
                'filter': Filters.regex(self.menu['LABEL_CHANGE_MY_PROPERTY']),
                'handler': Help(self)
            }
        ]
        self.states['help'] = [
            {},
            {
                'class': CommandHandler,
                'filter': Filters.regex("\/help"),
                'handler': Help(self)
            }
        ]

        """
        Scenarios runned on exceptions
        """
        self.fallbacks = {
            UserNeedsVerification: {
                'handler': ReceiveVerificationRequest(self),
            },
            ScenarioFailed: {
                # TODO: ....
            },
            ContactAdmin: {
                'handler': Help(self)
            },
            Exception: {
                'handler': Help(self)
            },
            FallbackToMenu: {
                'handler': Menu(self)
            }
        }


    """
    As soon as we filter not only by handler type, but also by current step and user's state
    we need an adapter, which catches messages, commands and poll answers
    and passes them through our business logic.
    """
    def register_handlers(self, dispatcher: Dispatcher):
        dispatcher.add_handler(MessageHandler(Filters.all, self._custom_message_handler))
        # dispatcher.add_handler(CommandHandler(Filters.all, self._custom_command_handler))
        dispatcher.add_handler(PollAnswerHandler(self._custom_poll_answer_handler))

    def _custom_message_handler(self, update: Update, context: CallbackContext) -> None:
        print('custom_message_handler')
        self._basic_handler(update, context, MessageHandler)

    def _custom_command_handler(self, update: Update, context: CallbackContext) -> None:
        print('custom_command_handler')
        self._basic_handler(update, context, CommandHandler)

    def _custom_poll_answer_handler(self, update: Update, context: CallbackContext) -> None:
        print('custom_poll_answer_handler')
        self._basic_handler(update, context, PollAnswerHandler)

    def _basic_handler(self, update: Update, context: CallbackContext, handler_type):
        print('basic_handler')
        user = self._get_user(update, context)
        try:
            user_state = user.get_dialog_state()
            print("user", user, "in state")
            print("[",user_state,"]")
                                            # TODO: а как быть когда человек прошёл всё и должен быть в стейте "я в главном меню"?
            possible_states = self._get_next_possible_states(user_state, handler_type)
            print("possible_states")
            print(possible_states.keys())
            for path, possible_state in possible_states.items():
                if possible_state['filter'](update): # TODO: это сломается когда filter будет не указан, либо когда он будет строкой, а не объектом
                    print('running state', path)
                    possible_state['handler'].handle(update=update, context=context, user=user)
                    user.set_dialog_state(path)
                    return
            raise ScenarioFailed()
        except:
            e = sys.exc_info()[0]
            caught = False
            for exception_type in self.fallbacks.keys():
                if e == exception_type:
                    print('fallback to ',exception_type)
                    print(e)
                    self.fallbacks[exception_type]['handler'].handle(update=update, context=context, user=user)
                    user.set_dialog_state("")
                    caught = True
            if not caught:
                print("JOPA")
                print(sys.exc_info())
                print(traceback.format_exc())

                self.fallbacks[FallbackToMenu]['handler'].handle(update=update, context=context, user=user)

    """
    Возвращает какие шаги дальше могут быть
    """
    def _get_next_possible_states(self, path: str, handler_type):
        result = {}
        if not path:
            for st in self.states.keys():
                result[st+"[1]"]=self.states[st][1]
        else:
            current_state = jmespath.search(path, self.states)
            # TODO: если путь в jmespath скормлен кривой — надо делать `raise FallbackToMenu`
            next_possible = current_state['next_possible']
            for item in next_possible:
                next_state = jmespath.search(item, self.states)
                if next_state['class'] == handler_type:
                    result[item] = next_state
        return result

    def _get_user(self, update: Update, context: CallbackContext) -> User:
        user_id = Telegramchats.get_user_id(update)
        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            user = User(
                user_id=user_id,
                name="", # TODO: set the goddamn name!
                verified=False
            )
            user.save()
        return user
