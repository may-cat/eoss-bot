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


class Check():
    def run(self, update: Update, context: CallbackContext, handler_type: object, step: dict, user: User, options: list=[]) -> bool:
        pass