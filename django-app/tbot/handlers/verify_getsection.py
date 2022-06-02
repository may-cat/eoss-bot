
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


class VerifyGetSection(TGHandler):
    def run(self, update: Update, context: CallbackContext, user: User) -> bool:
        chat_id = update.message.chat_id

        # TODO: ....

        """Inform user about what this bot can do"""
        update.message.reply_text(
            'Для того, чтобы запустить ЭОСС — используйте команду /eoss. '
            'Чтобы посмотреть результаты прошлых ЭОСС — используйте команду /eoss_stats. '
            'Обратите внимание, что все функции бота становятся доступными после того, как вы пройдёте верификацию. '
            'Если вы этого ещё не сделали — используйте команду /verify.'
        )
        return True
