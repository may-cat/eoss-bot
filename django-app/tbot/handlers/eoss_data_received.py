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
import logging
import json
from ..lib.handler import TGHandler


class EossDataRecieved(TGHandler):
    def handler_verified_users_only(self):
        return True

    def handler_private_chats_only(self) ->bool:
        return True

    def run(self, update: Update, context: CallbackContext, user: User) -> None:
        chat_id = update.message.chat_id

        draft = Draft.objects.get(chat_id=chat_id)
        section = Section.objects.get(id=1) # TODO: тут вместо этого должен быть какой-то сценарий как из чата с пользователем восстановить чат подъезда
        logging.critical("Section")
        logging.critical(section)
        logging.critical("Draft")
        logging.critical(draft)

        if not draft.has_enough_data():
            raise Exception("Пытаемся инициировать опрос, а данных не хватает")

        # Tell user, that we will start now
        context.bot.send_message(
            chat_id,
            "Всё принято, сейчас запустим ЭОСС в группе " + section.get_title() +
            "Чтобы узнать результаты — используйте команду /eoss_stats",
            parse_mode=ParseMode.HTML,
            reply_markup=ReplyKeyboardRemove()
        )

        # Send poll to relevant section chat and save data about it to our storage for future use
        message = context.bot.send_poll(
            section.get_chat_id(),
            draft.get_question(),
            draft.get_options(),
            is_anonymous=False,
            allows_multiple_answers=False,
            reply_markup=ReplyKeyboardRemove()
        )
        poll_id = message.poll.id

        # зафиксировать в базе, что он создан
        poll_object = Poll(
            poll_id=poll_id,
            options=json.dumps(draft.get_options()), # TODO: тут некрасивое, палим как в модели на самом деле хранятся данные. Надо бы пофиксить когда-нибудь
            question=draft.get_question(),
            section=section
        )
        poll_object.save()

        # deactivate draft
        draft.deactivate()
