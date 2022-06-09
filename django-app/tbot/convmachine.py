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
from .handlers.silent import Silent
from .handlers.start import Start
from .handlers.menu import Menu
from .handlers.verification_pending import VerificationPending
from .handlers.verify_getflat import VerifyGetFlat
from .handlers.verify_getparking import VerifyGetParking
from .handlers.verify_getparking_none import VerifyGetParkingNone
from .handlers.verify_getstoreroom import VerifyGetStoreroom
from .handlers.verify_getstoreroom_none import VerifyGetStoreroomNone
from .handlers.verify_getcommerce import VerifyGetCommerce
from .handlers.verify_getcommerce_none import VerifyGetCommerceNone
from .handlers.verify_receivemessages import VerifyReceiveMessages
from .handlers.revert_poll_answer import RevertPollAnswer
from .handlers.you_should_verify_first import YouShouldVerifyFirst
from .lib.check import Check
from .checks.is_private_chat import IsPrivateChat
from .checks.run_filter import RunFilter
from .checks.is_verified import IsVerified
from .checks.data_equal import DataEqual
from .checks.previous_is import PreviousIs
from .checks.is_public_chat import IsPublicChat
from .checks.is_not_verified import IsNotVerified
from .checks.data_matches import DataMatches
from .checks.poll_answer_is_empty import PollAnswerIsEmpty
from .checks.poll_answer_is_not_empty import PollAnswerNotEmpty
from .checks.verification_request_pending import VerificationRequestPending
from .checks.verification_request_not_pending import VerificationRequestNotPending
from .exceptions.needs_verification import UserNeedsVerification
from .exceptions.silent_exception import SilentException
from .exceptions.scenario_failed import ScenarioFailed
from .exceptions.contact_admin import ContactAdmin
from .exceptions.fallback_to_menu import FallbackToMenu
import jmespath
import sys
import traceback


class ConversationMachine():
    menu = {
        "LABEL_EOSS_START": "Запустить ЭОСС",
        "LABEL_STATS": "Результаты ЭОСС",
        "LABEL_LIST_MY_PROPERTY": 'Посмотреть свои объекты недвижимости',
        "LABEL_CHANGE_MY_PROPERTY": 'Изменить свои объекты недвижимости'
    }

    states = {}
    fallbacks = {}

    def __init__(self):
        """
        Scenarios

        """
        self.states = {}
        self.states['start'] = [
            {
                # Говорит дратути
                # Если не заапрувлен — кидаем ему список квартир и он из них выбирает
                'class': MessageHandler,
                'handler': Start,
                'restrict': [
                    IsPrivateChat,
                    [RunFilter, Filters.regex("\/start")]
                ],
                'is_state': True,
            },
        ]
        self.states['verify_process'] = [
            {
                # 0
                # Нажал на кнопку с номером квартиры
                'class': CallbackQueryHandler,
                'handler': VerifyGetFlat,
                'restrict': [
                    IsPrivateChat,
                    IsNotVerified,
                    [PreviousIs, 'start[0]'],
                    [DataMatches, 'owning_flat_']
                ],
                'is_state': True,
            },
            {
                # 1
                # Прислал номер паркинга
                'class': MessageHandler,
                'handler': VerifyGetParking,
                'restrict': [
                    IsPrivateChat,
                    IsNotVerified,
                    [PreviousIs, 'verify_process[0]'],
                ],
                'is_state': True,
            },
            {
                # 2
                # Нажал на кнопку "нет паркинга"
                'class': CallbackQueryHandler,
                'handler': VerifyGetParkingNone,
                'restrict': [
                    IsPrivateChat,
                    IsNotVerified,
                    [PreviousIs, 'verify_process[0]'],
                ],
                'is_state': True,
            },
            {
                # 3
                # Прислал номер кладовки
                'class': MessageHandler,
                'handler': VerifyGetStoreroom,
                'restrict': [
                    IsPrivateChat,
                    IsNotVerified,
                    [PreviousIs, 'verify_process[1],verify_process[2]'],
                ],
                'is_state': True,
            },
            {
                # 4
                # Нажал на кнопку "кладовки нет"
                'class': CallbackQueryHandler,
                'handler': VerifyGetStoreroomNone,
                'restrict': [
                    IsPrivateChat,
                    IsNotVerified,
                    [PreviousIs, 'verify_process[1],verify_process[2]'],
                ],
                'is_state': True,
            },
            {
                # 5
                # Прислал инфу о коммерческом помещении
                'class': MessageHandler,
                'handler': VerifyGetCommerce,
                'restrict': [
                    IsPrivateChat,
                    IsNotVerified,
                    [PreviousIs, 'verify_process[3],verify_process[4]'],
                ],
                'is_state': True,
            },
            {
                # 6
                # Нажал на кнопку "нет коммерческого помещения"
                'class': CallbackQueryHandler,
                'handler': VerifyGetCommerceNone,
                'restrict': [
                    IsPrivateChat,
                    IsNotVerified,
                    [PreviousIs, 'verify_process[3],verify_process[4]'],
                ],
                'is_state': True,
            },
            {
                # 7
                # Сообщение в ответ на предыдущее.
                # Добавляем его к списку сообщений этого юзера в заявке
                # Пересылаем нужному админу
                # В ответ говорим, что сообщение передано
                'class': CallbackQueryHandler,
                'handler': VerifyReceiveMessages,
                'restrict': [
                    IsPrivateChat,
                    IsNotVerified,
                    [PreviousIs, 'validation_request[5],validation_request[6]'],
                ],
                'is_state': True,
            },
        ]
        self.states['eoss_initiate'] = [
            {
                # Объясняем пользователю, как инициировать ЭОСС
                'class': CallbackQueryHandler,
                'handler': Eoss,
                'restrict': [
                    IsPrivateChat,
                    IsVerified,
                    [DataEqual, self.menu['LABEL_EOSS_START']],
                ],
                'is_state': True,
            },
            {
                # Получаем от пользователя опрос и в ответ предлагаем либо запустить его, либо отменить
                'class': MessageHandler,
                'handler': ReceivePoll,
                'restrict': [
                    IsPrivateChat,
                    IsVerified,
                    [PreviousIs, 'eoss_initiate[0]'],
                    [RunFilter, Filters.poll],
                ],
                'is_state': True,
            },
            {
                # Пользователь заказал запуск опроса
                'class': MessageHandler,
                'handler': EossDataRecieved,
                'restrict': [
                    IsPrivateChat,
                    IsVerified,
                    [PreviousIs, 'eoss_initiate[1]'],
                    [RunFilter, Filters.regex(BUTTON_RUN)],
                ],
                'is_state': True,
            },
            {
                # Пользователь заказал отмену запуска опроса
                'class': MessageHandler,
                'handler': EossDataCancelled,
                'restrict': [
                    IsPrivateChat,
                    IsVerified,
                    [PreviousIs, 'eoss_initiate[1]'],
                    [RunFilter, Filters.regex(BUTTON_CANCEL)],
                ],
                'is_state': True,
            },
        ]
        self.states['poll_answering'] = [
            {
                # Пользователи оставляют голоса в публичной группе
                'class': PollAnswerHandler,
                'handler': ReceivePollAnswer,
                'restrict': [
                    PollAnswerNotEmpty,
                ],
                'is_state': False,
            },
            {
                # Пользователи оставляют голоса в публичной группе
                'class': PollAnswerHandler,
                'handler': RevertPollAnswer,
                'restrict': [
                    PollAnswerIsEmpty,
                ],
                'is_state': False,
            },
        ]
        self.states['stats'] = [
            {
                'class': CallbackQueryHandler,
                'handler': EossStats,
                'restrict': [
                    IsPrivateChat,
                    IsVerified,
                    [DataEqual, self.menu['LABEL_STATS']],
                ],
                'is_state': True,
            }
        ]
        self.states['property_list'] = [
            {
                'class': CallbackQueryHandler,
                'handler': Help,
                'restrict': [
                    IsPrivateChat,
                    IsVerified,
                    [DataEqual, self.menu['LABEL_LIST_MY_PROPERTY']]
                ],
                'is_state': True,
            }
        ]
        self.states['property_edit'] = [
            {
                'class': CallbackQueryHandler,
                'handler': Help,
                'restrict': [
                    IsPrivateChat,
                    IsVerified,
                    [DataEqual, self.menu['LABEL_CHANGE_MY_PROPERTY']]
                ],
                'is_state': True,
            }
        ]
        self.states['help'] = [
            {
                'class': CommandHandler,
                'handler': Help,
                'restrict': [
                    IsPrivateChat,
                    [RunFilter, Filters.regex("\/help")]
                ],
                'is_state': False,
            }
        ]
        self.states['pending'] = [
            {
                # Если присылает какое-то сообщение а он не аппрувлен, но с заявкой
                'class': MessageHandler,
                'handler': VerificationPending,
                'restrict': [
                    IsPrivateChat,
                    IsNotVerified,
                    VerificationRequestPending,
                ],
                'is_state': True,
            },
            {
                # Если присылает какое-то сообщение а он не аппрувлен, но с заявкой
                'class': MessageHandler,
                'handler': YouShouldVerifyFirst,
                'restrict': [
                    IsPrivateChat,
                    IsNotVerified,
                    VerificationRequestNotPending,
                ],
                'is_state': True,
            },
        ]

        """
        Scenarios runned on exceptions
        """
        self.fallbacks = {
            UserNeedsVerification: {
                'handler': ReceiveVerificationRequest(),
            },
            ScenarioFailed: {
                'handler': Menu()
            },
            SilentException: {
                'handler': Silent()
            },
            ContactAdmin: {
                'handler': Help()
            },
            Exception: {
                'handler': Help()
            },
            FallbackToMenu: {
                'handler': Menu()
            }
        }


    """
    As soon as we filter not only by handler type, but also by current step and user's state
    we need an adapter, which catches messages, commands and poll answers
    and passes them through our business logic.
    """
    def register_handlers(self, dispatcher: Dispatcher):
        dispatcher.add_handler(MessageHandler(Filters.all, self._custom_message_handler))
        dispatcher.add_handler(PollAnswerHandler(self._custom_poll_answer_handler))
        dispatcher.add_handler(CallbackQueryHandler(self._custom_button_handler))

    def _custom_message_handler(self, update: Update, context: CallbackContext) -> None:
        self._basic_handler(update, context, MessageHandler)

    def _custom_button_handler(self, update: Update, context: CallbackContext) -> None:
        self._basic_handler(update["callback_query"], context, CallbackQueryHandler)

    def _custom_poll_answer_handler(self, update: Update, context: CallbackContext) -> None:
        self._basic_handler(update, context, PollAnswerHandler)

    def _basic_handler(self, update: Update, context: CallbackContext, handler_type):
        user = self._get_user(update, context)
        try:
            for sckey, scenario in self.states.items():
                for stkey in range(0, len(scenario)):
                    step = scenario[stkey]
                    if step['class'] == handler_type:
                        passed = True
                        if 'restrict' in step:
                            passed = self._check_restrictions(update, context, handler_type, step, user)
                        if passed:
                            objStep = step['handler']()
                            print('user', user, 'starting step', step, 'run', objStep)
                            print(update)
                            print("\n\n")
                            if objStep.run(update=update, context=context, user=user) and step['is_state']:
                                user.set_dialog_state(sckey+"["+str(stkey)+"]")
                            return True
            if self._is_private_chat(update, context, handler_type):
                raise ScenarioFailed()
            else:
                raise SilentException()
        except:
            e = sys.exc_info()[0]
            caught = False
            for exception_type in self.fallbacks.keys():
                if e == exception_type:
                    print('fallback to ', exception_type)
                    print(e)
                    self.fallbacks[exception_type]['handler'].run(update=update, context=context, user=user)
                    user.set_dialog_state("")
                    caught = True
            if not caught:
                print("JOPA")
                print(sys.exc_info())
                print(traceback.format_exc())

                self.fallbacks[FallbackToMenu]['handler'].run(update=update, context=context, user=user)

    def _check_restrictions(self, update: Update, context: CallbackContext, handler_type, step, user: User) -> bool:
        for check in step['restrict']:
            check_result = False
            if not isinstance(check, list):
                obj_check = check()
                check_result = obj_check.run(update=update, context=context, handler_type=handler_type, step=step, user=user)
            elif isinstance(check, list):
                obj_check = check[0]()
                check_result = obj_check.run(update=update, context=context, handler_type=handler_type, step=step, user=user, options=check[1:])
            if not check_result:
                return False
        return True

    def _get_user(self, update: Update, context: CallbackContext) -> User:
        return User.factory_on_telegram_message(update)

    def _is_private_chat(self, update: Update, context: CallbackContext, handler_type):
        if hasattr(update,'message') and hasattr(update.message,'chat'):
            return update.message.chat.id>0
        return False

