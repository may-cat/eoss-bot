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
from ..models import *
from ..lib.handler import TGHandler

class RevertPollAnswer(TGHandler):
    def run(self, update: Update, context: CallbackContext, user: User) -> bool:
        answer = update.poll_answer
        poll_id = answer.poll_id
        poll = Poll.objects.get(poll_id=poll_id)
        user_id = answer.user.id
        user = User.factory_on_telegram_message(update)
        Vote.objects.filter(
            poll=poll,
            user=user
        ).all().delete()

        return True
