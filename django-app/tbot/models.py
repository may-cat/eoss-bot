from django.db import models
import json
import logging
from telegram import (
    Update,
)

"""
Хранилище информации об объекте недвижимости
"""

class Estate(models.Model):
    estate_code = models.CharField(max_length=255, null=False, default="")
    _total_real_space = models.FloatField(null=True)

    # TODO: when editing Estate — should show warning, if Estateownings has not enough space to fill _total_real_space (обрати внимание, что это сравнение float-ов!)

    def get_total_weight(self) -> float:
        sum_weight = 0.0
        for uw in self._get_users_and_weights():
            sum_weight = sum_weight + uw['weight']
        return sum_weight

    def get_users_weight(self, user_id) -> float:
        for uw in self._get_users_and_weights():
            if uw['user_id'] == user_id:
                return uw['weight']

    def _get_users_and_weights(self) -> list:
        estate_ownings = Estateowning.objects.filter(estate=self)
        result = []
        for estate_owning in estate_ownings:
            result.append({
                "user_id": estate_owning.user_id,
                "weight": estate_owning.owning_weight
            })
        return result

    def _set_users_and_weights(self, users_and_weights) -> None:
        # Получить полный список, чтобы потом узнать что нужно удалять
        ids_before = []
        for eo in Estateowning.objects.filter(estate=self):
            ids_before.append(eo.id)

        # Изменить что изменилось
        # Добавить что добавилось
        for uw in users_and_weights:
            try:
                estate_owning = Estateowning.objects.get(estate=self, user_id=int(uw['user_id']))
                estate_owning.owning_weight = float(uw['weight'])
                estate_owning.save()
                ids_before.remove(estate_owning.id)
            except Estateowning.DoesNotExist:
                eo = Estateowning(
                    user_id=int(uw['user_id']),
                    estate=self,
                    owning_weight=float(uw['weight'])
                )
                eo.save()

        # Удалить что удалилось
        for id in ids_before:
            Estateowning.objects.get(id=id).delete()

"""
Подъезд, для которого есть отдельный чат
"""


class Section(models.Model):
    chat_id = models.BigIntegerField(null=False, default=-716321959) # -716321959
    title = models.CharField(max_length=255, null=False, default="[unknown]")

    def get_chat_id(self):
        return self.chat_id

    def get_title(self):
        return self.title

"""
Модель, хранящая пользователей чата.
Скорее всего пользователь — это житель.
"""


class User(models.Model):
    user_id = models.BigIntegerField(null=False)
    name = models.CharField(max_length=255, null=False)
    verified = models.BooleanField(default=False)
    dialog_state = models.CharField(max_length=255, null=True, default="")
    """
    Возвращает свойство пользователя, которое на самом деле является путём в массиве ConvMachine.states.
    Значение свойства соответствует формату библиотеки jmespath
    """

    def is_verified(self):
        return self.verified

    def get_dialog_state(self):
        return self.dialog_state

    def set_dialog_state(self, state):
        self.dialog_state = state
        self.save()

    @staticmethod
    def factory_on_telegram_message(update: Update):
        # get user id from telegram message
        user_id = None
        if hasattr(update, 'message') and hasattr(update.message, 'chat'):
            user_id = update.message.chat.id
        elif hasattr(update, 'poll_answer') and hasattr(update.poll_answer, 'user'):
            user_id = update.poll_answer.user.id
        else:
            raise Exception("Почему-то нет айдишника юзера")

        # Try to get user based on user_id or except — create it
        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            # Get all info we can about user
            name = "unknown"
            try:
                name = User._extract_name(update.message.from_user)
            except AttributeError:
                pass
            try:
                name = User._extract_name(update.poll_answer.user)
            except AttributeError:
                pass

            user = User(
                user_id=user_id,
                name=name,
                verified=False,
                dialog_state="start"
            )
            user.save()
        return user

    @staticmethod
    def _extract_name(user_data):
        name = ""
        try:
            if user_data.username is not None:
                name = name + user_data.username + " "
        except AttributeError:
            pass
        try:
            if user_data.first_name is not None:
                name = name + user_data.first_name + " "
        except AttributeError:
            pass
        try:
            if user_data.last_name is not None:
                name = name + user_data.last_name + " "
        except AttributeError:
            pass
        return name


"""
У кого какие доли в объектах недвижимости
"""


class Estateowning(models.Model):
    estate = models.ForeignKey(Estate, null=True, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING)
    owning_weight = models.FloatField(null=True)


"""
Черновики ЭОСС
"""


class Draft(models.Model):
    chat_id = models.BigIntegerField(primary_key=True)
    target_section = models.OneToOneField(Section, on_delete=models.DO_NOTHING, null=True)
    active = models.BooleanField(default=False)
    options = models.TextField(default="{}") # NOTICE: вот это трэш, надо по-хорошему сохранять в более приличном виде
    question = models.TextField(default="")


    def activate(self):
        self.active = True
        self.save()

    def deactivate(self):
        self.active = False
        self.target_section = None
        self.options = "{}"
        self.question = ""
        self.save()

    def is_active(self) -> bool:
        return self.active

    def has_enough_data(self)->bool:
        logging.critical(bool(self.target_section))
        logging.critical(len(self.options) > 2)
        logging.critical(self.question>"")
        logging.critical(bool(self.active))
        return self.target_section and (len(self.options)>2) and (self.question>"") and self.active

    def get_question(self) -> str:
        return self.question

    def set_question(self, question):
        self.question = question
        self.save()

    def get_options(self) -> list:
        return json.loads(self.options)

    def set_options(self, options) -> None:
        self.options = json.dumps(options)
        self.save()

    def set_target_section(self, section: Section) -> None:
        self.target_section = section
        self.save()



"""
Опрос, запущенный где-то
Хранит информацию о том где он запущен и какие там есть варианты ответов
"""


class Poll(models.Model):
    poll_id = models.BigIntegerField(null=False, default=-1)
    options = models.TextField(default="{}")  # NOTICE: вот это трэш, надо по-хорошему сохранять в более приличном виде
    question = models.TextField(default="")
    section = models.ForeignKey(Section, null=True, on_delete=models.DO_NOTHING)

    """
    Кто как проголосовал в итоге
    """

    def get_options(self) -> list:
        return json.loads(self.options)

    def get_question(self) -> str:
        return self.question

    """
    Notice!
    There are no setters due they are useless. We don't change poll, that is already sent to users. 
    """


"""
Голос отданный пользователем за какой-то из вариантов голосования.
Хранит в себе как информацию о голосовании, так и указание на пользователя, так и его выбранный вариант
"""


class Vote(models.Model):
    poll = models.ForeignKey(Poll, null=True, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING)
    selected_vote_id = models.IntegerField(default=-1)
    selected_vote = models.TextField(default="")

    def get_user_id(self):
        return self.user.id

    def get_selected_vote(self):
        return self.selected_vote

    def get_selected_vote_id(self):
        return self.selected_vote_id


class VerificationRequest(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING)
    section = models.TextField(default="")
    flat = models.TextField(default="")
    parking = models.TextField(default="")
    storeroom = models.TextField(default="")
    commerce = models.TextField(default="")
