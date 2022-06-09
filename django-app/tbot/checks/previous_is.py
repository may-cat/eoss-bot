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
from ..helpers.telegramchats import Telegramchats
from ..models import *
from ..message_templates.message_templates import _need_verifiication, _need_eoss_start
from ..settings import BUTTON_RUN, BUTTON_CANCEL
import logging
from ..lib.check import Check


class PreviousIs(Check):
    def run(self, update: Update, context: CallbackContext, handler_type: object, step: dict, user: User, options: list=[]) -> bool:
        print('check')
        user_state = user.get_dialog_state()
        if ',' in options[0]:
            variants = options[0].split(',')
            return user_state in variants
        else:
            return user_state == options[0]
