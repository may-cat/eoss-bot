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


class ReceivePollAnswer(TGHandler):
    def run(self, update: Update, context: CallbackContext, user: User) -> bool:
        answer = update.poll_answer
        poll_id = answer.poll_id
        poll = Poll.objects.get(poll_id=poll_id)
        user_id = answer.user.id
        poll_options = poll.get_options()
        user = User.factory_on_telegram_message(update)
        answer_id = answer.option_ids[0]
        answer_str = poll.get_options()[answer_id]

        vote = Vote(
            poll=poll,
            user=user,
            selected_vote_id=answer_id,
            selected_vote=poll.get_options()[answer_id]
        )
        vote.save()
        return True
