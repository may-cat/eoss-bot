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
from ..lib.handler import TGHandler


class Menu(TGHandler):
    def run(self, update: Update, context: CallbackContext, user: User) -> bool:
        keyboard = [
            [InlineKeyboardButton("Запустить ЭОСС", callback_data="Запустить ЭОСС")],
            [InlineKeyboardButton("Результаты ЭОСС", callback_data="Результаты ЭОСС")],
        ]
        markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text("🏠 Добро пожаловать домой, выберите действие:", reply_markup=markup)
        return True


