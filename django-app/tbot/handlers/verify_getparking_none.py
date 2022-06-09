
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


class VerifyGetParkingNone(TGHandler):
    def run(self, update: Update, context: CallbackContext, user: User) -> bool:
        original_update = update
        MakingVerificationRequest.catch_no_parking(update, context, user)
        MakingVerificationRequest.ask_storeroom(original_update, context, user)
        return True
