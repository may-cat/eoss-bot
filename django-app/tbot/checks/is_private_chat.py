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


class IsPrivateChat(Check):
    def run(self, update: Update, context: CallbackContext, handler_type: object, step: dict, user: User, options: list=[]) -> bool:
        if hasattr(update, 'message') and hasattr(update.message, 'chat'):
            return update.message.chat.id > 0
        return False

