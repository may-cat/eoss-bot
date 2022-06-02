import logging
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

from ..message_templates.message_templates import _need_verifiication, _need_eoss_start
from ..models import *
from ..exceptions.needs_verification import UserNeedsVerification
from ..exceptions.scenario_failed import ScenarioFailed
from ..exceptions.contact_admin import ContactAdmin


class TGHandler():
    conversation_machine = None

    def run(self, update: Update, context: CallbackContext, user: User) -> bool:
        """

        :param update:
        :param context:
        :param user:
        :return: bool Returns if user successfully passed this step. If did — current step may be written to user's state.
        If not – current state will not be written to user's state.
        """
        return True