
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
from ..helpers.making_verification_request import MakingVerificationRequest


class YouShouldVerifyFirst(TGHandler):
    def run(self, update: Update, context: CallbackContext, user: User) -> bool:
        update.message.reply_text(
            'Сперва нужно подать заявку на верификацию, нажмите /start'
        )
        return True
