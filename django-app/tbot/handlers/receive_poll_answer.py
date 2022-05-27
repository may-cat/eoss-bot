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
    def handler_verified_users_only(self):
        return False

    def handler_private_chats_only(self) -> bool:
        return False

    def run(self, update: Update, context: CallbackContext, user: User) -> None:
        answer = update.poll_answer
        poll_id = answer.poll_id
        poll = Poll.objects.get(poll_id=poll_id)
        user_id = answer.user.id
        poll_options = poll.get_options()

        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            user = User(
                user_id=user_id,
                name=answer.user.name
            )
            user.save()

        answer_id = answer.option_ids[0]
        answer_str = poll.get_options()[answer_id]

        print("poll")
        print(poll)
        print("answer_id")
        print(answer_id)
        print("answer_str")
        print(answer_str)

        vote = Vote(
            poll=poll,
            user=user,
            selected_vote_id=answer_id,
            selected_vote=poll.get_options()[answer_id]
        )
        vote.save()
        print("vote")
        print(vote)
