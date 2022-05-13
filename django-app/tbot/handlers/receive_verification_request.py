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


class ReceiveVerificationRequest(TGHandler):
    def handler_verified_users_only(self):
        return False

    def handler_private_chats_only(self) ->bool:
        return False

    def run(self, update: Update, context: CallbackContext, user: User) -> None:
        chat_id = update.message.chat_id

        """
        TODO: пользователь должен был прислать сюда сообщение в котором — его адрес. 
        Нам надо всё упаковать и отправить админу (???) или сохранить куда-то 
        как заявку на верификацию.
        """