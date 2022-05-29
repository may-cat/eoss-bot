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
    def handler_verified_users_only(self):
        return False

    def handler_private_chats_only(self) ->bool:
        return False

    def run(self, update: Update, context: CallbackContext, user: User) -> None:
        keyboard = [
            [InlineKeyboardButton("Запустить ЭОСС", callback_data="Запустить ЭОСС")],
            [InlineKeyboardButton("Результаты ЭОСС", callback_data="Результаты ЭОСС")],
        ]
        markup = InlineKeyboardMarkup(keyboard)

        Когда голосование то тут отстреливает, потому что нет никаокго message

        update.message.reply_text("🏠 Добро пожаловать домой, выберите действие:", reply_markup=markup)

    # TODO: ....

