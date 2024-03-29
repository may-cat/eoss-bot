
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
from ..lib.handler import TGHandler
from ..models import *
from ..exceptions.fallback_to_menu import FallbackToMenu
from ..helpers.making_verification_request import MakingVerificationRequest


class Start(TGHandler):
    def run(self, update: Update, context: CallbackContext, user: User) -> bool:
        chat_id = update.message.chat_id

        if user.is_verified():
            raise FallbackToMenu()

        MakingVerificationRequest.ask_flat(update, context, user)
        return True
