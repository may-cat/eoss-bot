
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
from ..exceptions.fallback_to_menu import FallbackToMenu


class Start(TGHandler):
    def run(self, update: Update, context: CallbackContext, user: User) -> bool:
        chat_id = update.message.chat_id

        if user.is_verified():
            raise FallbackToMenu()



        # TODO: надо осуществлять проверку — заапрувленный ли юзер.
        #  TODO: Если да, то кидаем его в меню эксепшном или прямым вызовом
        # TODO: если не заапрувленный — пишем ему чото, чтобы он указал откуда он
        #  TODO: (возможно кнопки с выбором)

        """Inform user about what this bot can do"""
        update.message.reply_text(
            'Для того, чтобы запустить ЭОСС — используйте команду /eoss. '
            'Чтобы посмотреть результаты прошлых ЭОСС — используйте команду /eoss_stats. '
            'Обратите внимание, что все функции бота становятся доступными после того, как вы пройдёте верификацию. '
            'Если вы этого ещё не сделали — используйте команду /verify.'
        )
        return True
