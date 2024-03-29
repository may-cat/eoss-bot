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
from ..lib.handler import TGHandler
from ..models import *


class EossDataCancelled(TGHandler):
    def run(self, update: Update, context: CallbackContext, user: User) -> bool:
        chat_id = update.message.chat_id

        context.bot.send_message(
            chat_id,
            "Сорян, это ещё не реализовали :) ",
            parse_mode=ParseMode.HTML
        )
        return True