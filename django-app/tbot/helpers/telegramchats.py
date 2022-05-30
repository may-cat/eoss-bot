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
        if hasattr(update, 'message') and hasattr(update.message,'chat'):
            return update.message.chat.id
        if hasattr(update, 'poll_answer') and hasattr(update.poll_answer,'user'):
            return update.poll_answer.user.id
        raise Exception("Почему-то нет айдишника юзера")

    """
    Проверяет, что указаный чат — 
    """
    @staticmethod
    def is_private_chat(update: Update):
        return update.message["chat"]["type"] == "private"
