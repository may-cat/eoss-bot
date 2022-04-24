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


def _need_verifiication(context, chat_id):
    """
    Сообщает пользователю, что необходимо пройти верификацию.
    :param context:
    :param chat_id:
    :return:
    """
    context.bot.send_message(
        chat_id,
        "Нужно пройти верификацию, чтобы раскрыть все функции бота. Напишите @i_tsupko.",
        parse_mode=ParseMode.HTML,
        reply_markup=ReplyKeyboardRemove()
    )


def _need_eoss_start(context, chat_id):
    """
    Сообщает пользователю, что он не запустил процесс формирования ЭОСС-голосования.
    :param context:
    :param chat_id:
    :return:
    """
    context.bot.send_message(
        chat_id,
        "Сначала надо запустить команду /eoss",
        parse_mode=ParseMode.HTML,
        reply_markup=ReplyKeyboardRemove()
    )