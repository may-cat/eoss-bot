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


def eoss(update: Update, context: CallbackContext) -> None:
    """
    Работа команды /eoss.
    Запускает электронный ОСС, информирует человека, что именно нужно сделать, чтобы бот запустил опрос в группе.
    :param update:
    :param context:
    :return:
    """
    message_id = update.message.message_id
    chat_id = update.message.chat_id
    logging.info("EOSS %s: %s", message_id, chat_id)

    user_id = Telegramchats.get_user_id(update)
    user = User(user_id)
    if not user.is_verified():
        _need_verifiication(context, chat_id)

    if not Telegramchats.is_private_chat(update):
        return

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
