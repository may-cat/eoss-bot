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


class Help(TGHandler):
    def handler_verified_users_only(self):
        return False

    def handler_private_chats_only(self) ->bool:
        return False

    def run(self, update: Update, context: CallbackContext, user: User) -> None:
        chat_id = update.message.chat_id

        update.message.reply_text("По всем вопросам пишите @i_tsupko")
