from django.db import models
import json
import logging

"""
Хранилище информации об объекте недвижимости
"""



class Estate(models.Model):
    estate_code = models.CharField(max_length=255, null=False, default="")
    _total_real_space = models.FloatField(null=True)
    users_and_weights = models.TextField(default="[]") # NOTICE: вот это трэш, надо по-хорошему сохранять в более приличном виде
    # TODO: вообще вот эту связь пользователей с недвижкой через веса надо тоже превратить в модель!

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
        return json.loads(self.users_and_weights)

    def _set_users_and_weights(self, users_and_weights) -> None:
        self.users_and_weights = json.dumps(users_and_weights)
        self.save()

"""
Подъезд, для которого есть отдельный чат
"""


class Section(models.Model):
    chat_id = models.BigIntegerField(null=False, default=-716321959) # -716321959
    title = models.CharField(max_length=255, null=False, default="[unknown]")

    def get_chat_id(self):
        #TODO: захардкодить инфу по этой секции, у нас только одна сейчас
        return self.chat_id

    def get_title(self):
        #TODO: захардкодить инфу по этой секции, у нас только одна сейчас
        return self.title

"""
Модель, хранящая пользователей чата.
Скорее всего пользователь — это житель.
"""


class User(models.Model):
    user_id = models.BigIntegerField(null=False)
    personal_chat_id = models.BigIntegerField(null=True) # TODO: надо как-то обогащать данные если их нет. Юзера могут создать когда проголосовали.
    name = models.CharField(max_length=255, null=False)
    verified = models.BooleanField(default=False)

    def is_verified(self):
        return self.verified


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
        print("optinons")
        print(self.options)
        print("JSON")
        print(json.loads(self.options))
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


"""
Хранилище всех голосов пользователей по какому-то из опросов


class Eossstats(models.Model):
    estate = models.ForeignKey(Estate, null=True, on_delete=models.CASCADE)
    poll = models.OneToOneField(Poll, null=True, on_delete=models.DO_NOTHING)

    # weight float
    # vote Vote() object
    def __init__(self, estate: Estate, weight: float, vote: Vote):
        pass

    def get_votes(self):
        return [Vote(), Vote(), Vote()]

    def get_estate_id(self):
        return 12123

    def get_weight(self):
        return 1231.1

    def get_vote_label(self):
        return "asdadasdada"

    def get_sum_for_option(self, option_string: str):
        # TODO: run through all Vote() objects and summ all weights
        pass
"""

