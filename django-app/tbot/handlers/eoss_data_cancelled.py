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


def eoss_data_cancelled(update: Update, context: CallbackContext) -> None:
    """
    Cancel EOSS draft
    :param update:
    :param context:
    :return:
    """
    chat_id = update.message.chat_id
    if not Telegramchats.is_private_chat(update):
        return
    context.bot.send_message(
        chat_id,
        "Сорян, это ещё не реализовали :) ",
        parse_mode=ParseMode.HTML
    )

    # TODO: cancel scenario!
