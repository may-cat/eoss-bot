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

class Telegramchats():

    @staticmethod
    def get_user_id(update: Update):
        return update.message.chat.id

    """
    Проверяет, что указаный чат — 
    """
    @staticmethod
    def is_private_chat(update: Update):
        return update.message["chat"]["type"] == "private"
