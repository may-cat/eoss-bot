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
from ..models import *
from ..message_templates.message_templates import _need_verifiication, _need_eoss_start


class Usercheck():

    """
    """
    @staticmethod
    def run_user_check(update: Update, context: CallbackContext):
        chat_id = update.message.chat_id
        user_id = Telegramchats.get_user_id(update)

        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            user = User(
                user_id=user_id,
                name="", # TODO: set the goddamn name!
                verified=False
            )
            user.save()

        if not user.is_verified():
            verification_pending = False # TODO: это надо брать из базы откуда-то

            if verification_pending:
                # TODO: отправляем сообщение, что мол ждите, админ вас вот-вот заапрувит, контакты для связи с админом вот такие
                pass
            else:
                # TODO: отправляем пользователю инфу, что он должен прислать инфу о своём объекте недвижимости
                pass

            raise Exception("Пользователь ещё не аппрувлен") # TODO: сделать кастомный тип эксепшна
