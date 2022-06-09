
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


class VerifyGetCommerceNone(TGHandler):
    def run(self, update: Update, context: CallbackContext, user: User) -> bool:
        MakingVerificationRequest.catch_no_commerce(update, context, user)
        return True
