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
from ..models import *
from ..exceptions.needs_verification import UserNeedsVerification
from ..exceptions.scenario_failed import ScenarioFailed
from ..exceptions.contact_admin import ContactAdmin


class TGHandler():
    conversation_machine = None

    def __init__(self, conv_machine):
        pass

    def handler_verified_users_only(self)->bool:
        return True

    def handler_private_chats_only(self)->bool:
        return True

    def _process_user_verification_check(self, user: User) -> None:
        if user.is_verified():
            return True

        if self.handler_verified_users_only():
            verification_pending = True # TODO: run verification pending check from database
            if verification_pending:
                raise ContactAdmin()
            raise UserNeedsVerification()

        return True

    def _process_is_private_chat_check(self, update: Update) -> None:
        pass

    def handle(self, update: Update, context: CallbackContext, user: User) -> None:
        print("Runned class", self.__class__.__name__)
        # TODO: add logging
        # Check if user may use the bot
        if self.handler_verified_users_only():
            self._process_user_verification_check(user)
        if self.handler_private_chats_only():
            self._process_is_private_chat_check(update)

        # Run handler logic
        self.run(update, context, user)

    def run(self, update: Update, context: CallbackContext, user: User) -> None:
        pass