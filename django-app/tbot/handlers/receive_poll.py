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
from ..settings import BUTTON_RUN, BUTTON_CANCEL
import logging
from ..lib.handler import TGHandler


class ReceivePoll(TGHandler):
    def handler_verified_users_only(self):
        return True

    def handler_private_chats_only(self) ->bool:
        return True

    def run(self, update: Update, context: CallbackContext, user: User) -> None:
        chat_id = update.message.chat_id

        section = Section.objects.get(id=1) # TODO: тут вместо этого должен быть какой-то сценарий как из чата с пользователем восстановить чат подъезда

        draft = Draft.objects.get(chat_id=chat_id)
        if not draft.is_active():
            _need_eoss_start(context, chat_id)
        else:
            # Parse incoming poll and put it in memory
            options = []
            for opt in update.message.poll.options:
                options.append(opt.text)

            draft.set_options(options=options)
            draft.set_question(update.message.poll.question)
            logging.critical("Сейчас будем разбираться с секцией")
            logging.critical(section)
            draft.set_target_section(section)

            # Send message to user
            button = [[KeyboardButton(BUTTON_RUN), KeyboardButton(BUTTON_CANCEL)]]
            context.bot.send_message(
                chat_id,
                "Готов запустить ЭОСС. "
                "Опрос принят, мы готовы запустить его в 10-ой секции. "
                "Если всё ок — нажмите кнопку 'Запускай'.",
                parse_mode=ParseMode.HTML,
                reply_markup=ReplyKeyboardMarkup(button, one_time_keyboard=True)
            )

