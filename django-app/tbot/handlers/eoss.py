import logging
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

from ..message_templates.message_templates import _need_verifiication, _need_eoss_start
from ..helpers.telegramchats import Telegramchats
from ..models import *
from ..lib.handler import TGHandler


class Eoss(TGHandler):
    def handler_verified_users_only(self):
        return True

    def handler_private_chats_only(self) ->bool:
        return True

    def run(self, update: Update, context: CallbackContext, user: User) -> None:
        chat_id = update.message.chat_id

        try:
            draft = Draft.objects.get(chat_id=chat_id)
        except Draft.DoesNotExist:
            draft = Draft(chat_id=chat_id)
            draft.save()
        draft.activate()

        context.bot.send_message(
            chat_id,
            "Готов запустить ЭОСС. Пришлите ответным сообщением опрос, который мы запустим в качестве ЭОСС.",
            parse_mode=ParseMode.HTML,
            reply_markup=ReplyKeyboardRemove()
        )
