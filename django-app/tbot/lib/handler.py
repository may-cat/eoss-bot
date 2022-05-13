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

from ..convmachine import ConversationMachine


class TGHandler():
    conversation_machine = None

    def __init__(self, conversation_machine: ConversationMachine):
        self.conversation_machine = conversation_machine

    def _if_can_proceed(self, user: User):
        return self.conversation_machine.can_proceed(user)

    def _get_user(self, update: Update, context: CallbackContext) -> User:
        user_id = Telegramchats.get_user_id(update)
        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            user = User(
                user_id=user_id,
                name="", # TODO: set the goddamn name!
                verified=False
            )
            user.save()
        return user

    def handler_verified_users_only(self)->bool:
        return True

    def handler_private_chats_only(self)->bool:
        return True

    def _process_user_verification_check(self, user: User) -> None:
        if not user.is_verified():
            verification_pending = False # TODO: это надо брать из базы откуда-то

        if verification_pending:
            # TODO: отправляем сообщение, что мол ждите, админ вас вот-вот заапрувит, контакты для связи с админом вот такие
            pass
        else:
            # TODO: отправляем пользователю инфу, что он должен прислать инфу о своём объекте недвижимости
            pass

        raise Exception("Пользователь ещё не аппрувлен") # TODO: сделать кастомный тип эксепшна

    def _process_is_private_chat_check(self, update: Update) -> None:
        pass

    def handle(self, update: Update, context: CallbackContext) -> None:
        # TODO: add logging
        user = self._get_user(update, context)
        if not self._if_can_proceed(user):
            """
            TODO: тут какой-то штук, что мол юзер не может продолжать потому что сломался сценарий.
            Наверное надо кидать ему сообщение об этом и выкидывать в основное меню
            """
            pass

        # Check if user may use the bot
        if self.handler_verified_users_only():
            self._process_user_verification_check(user)
        if self.handler_private_chats_only():
            self._process_is_private_chat_check(update)

        # Run handler logic
        self.run(update, context, user)

    def run(self, update: Update, context: CallbackContext, user: User) -> None:
        pass