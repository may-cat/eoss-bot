
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


class VerifyGetCommerce(TGHandler):
    def run(self, update: Update, context: CallbackContext, user: User) -> bool:
        MakingVerificationRequest.catch_commerce(update, context, user)
        # TODO: Собираем всё, что до этого нам прислал пользователь и говорим ему что мол вот всё. И кнопки "отправить заявку" или "отбой, всё сначала"
        return True
