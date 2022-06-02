#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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
from ..helpers.telegramchats import Telegramchats
from ..models import *
from ..message_templates.message_templates import _need_verifiication, _need_eoss_start
from ..lib.handler import TGHandler


class EossStats(TGHandler):
    def run(self, update: Update, context: CallbackContext, user: User) -> bool:
        chat_id = update.message.chat_id

        """
        One report for each of last 3 EOSSes should be made
        """
        section = Section.objects.get(id=1) # TODO: тут вместо этого должен быть какой-то сценарий как из чата с пользователем восстановить чат подъезда
        polls = Poll.objects.filter(section_id=section.id)

        """
        Костыльная загрузка всех объектов недвижимости
        TODO: это надо потом переделать в нормальное хранение в базе
        """
        kostyl_users_estate = {}
        for estate in Estate.objects.all():
            for uw in estate._get_users_and_weights():
                kostyl_users_estate[uw['user_id']] = []
            for uw in estate._get_users_and_weights():
                kostyl_users_estate[uw['user_id']].append(estate.estate_code)

        """
        Для каждого из запущенных опросов проходимся по тому кто как голосовал, рассчитываем стату и отправляем пользователю
        """
        for poll_object in polls:
            """
            :var stats будет хранить массив того, что влияет на конечную статистику:
                        - какой человек
                        - от имени какого объекта недвижимости
                        - сколько голосов накинул
                        - и какой голос был
            """
            stats = []

            message = ""
            message = "<b>" + poll_object.question + "</b>\n"

            """
            Берём все голоса и обогащаем их
            """
            votes = Vote.objects.filter(poll=poll_object)
            has_some_votes = False
            weight_sums = {}
            for vote_object in votes:
                user_id = vote_object.get_user_id()
                try:
                    voted_user = User.objects.get(id=user_id)
                    if voted_user.is_verified():
                        for estate_code in kostyl_users_estate[voted_user.id]: # TODO: Тут алгоритмический пиздец и мне стыдно, исправим позже
                            estate_object = Estate.objects.get(estate_code=estate_code)
                            weight = estate_object.get_users_weight(user_id)
                            stats.append({
                                "user": voted_user,
                                "estate": estate_object,
                                "weight": weight,
                                "vote": vote_object
                            })
                            current_vote_id = vote_object.get_selected_vote_id()
                            if current_vote_id not in weight_sums.keys():
                                weight_sums[current_vote_id] = 0
                            weight_sums[current_vote_id] = weight_sums[current_vote_id] + weight
                            has_some_votes = True
                except User.DoesNotExist:
                    print("user doesn't exist")
                    voted_user = None

            for stat in stats: # TODO: по-хорошему тутаньки оно должно быть уже сортировано по объектам недвижимости
                message = message + stat["estate"].estate_code + ", " + stat["user"].name + " — " + str(stat["weight"]) + " голосов " + stat["vote"].get_selected_vote() + "\n"

            if has_some_votes:
                message = message + "\nСумма голосов:\n"
                k = 0
                for poll_option in poll_object.get_options():
                    if k in weight_sums.keys():
                        message = message + " - " + poll_option + " — " + str(weight_sums[k]) + " голосов\n"
                    k = k + 1
                # Отправляем сообщение (если есть из чего)
                context.bot.send_message(
                    chat_id,
                    message,
                    parse_mode=ParseMode.HTML
                )

        return True