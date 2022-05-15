
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
from ..lib.handler import TGHandler
from ..models import *


class Start(TGHandler):
    def handler_verified_users_only(self):
        return False

    def handler_private_chats_only(self) ->bool:
        return False

    def run(self, update: Update, context: CallbackContext, user: User) -> None:
        chat_id = update.message.chat_id

        """Inform user about what this bot can do"""
        update.message.reply_text(
            'Для того, чтобы запустить ЭОСС — используйте команду /eoss. '
            'Чтобы посмотреть результаты прошлых ЭОСС — используйте команду /eoss_stats. '
            'Обратите внимание, что все функции бота становятся доступными после того, как вы пройдёте верификацию. '
            'Если вы этого ещё не сделали — используйте команду /verify.'
        )
