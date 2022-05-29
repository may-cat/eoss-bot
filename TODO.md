## Переходим на гибкие сценарии

На данный момент:

Удалось запустить общую логику управления.
Удалось запустить ЭОСС
Удалось запустить стату
И стейт-машину с горем пополам

Проблемы:

1. В некоторых случаях не нажимаются кнопки с первого раза. Скорее всего — из-за ограничений на next_state

2. Кажется, что у нас ошибка в логике, запрещающая нам перескочить на другую ветку.

3. Голоса не проходят, скорее всего из-за того же

```
basic_handler
get_user_id
{'poll_answer': {'user': {'last_name': 'Цупко', 'id': 24442585, 'is_bot': False, 'first_name': 'Игорь', 'language_code': 'ru', 'username': 'i_tsupko'}, 'poll_id': '5226957452427133380', 'option_ids': [1]}, 'update_id': 617129490}
user User object (1) in state
[ eoss_initiate[3] ]
handler_type
<class 'telegram.ext.pollanswerhandler.PollAnswerHandler'>
possible_states
dict_keys([])
fallback to  <class 'tbot.exceptions.silent_exception.SilentException'>
<class 'tbot.exceptions.silent_exception.SilentException'>
Runned class Silent
basic_handler
get_user_id
{'poll_answer': {'user': {'id': 325806629, 'is_bot': False, 'first_name': 'petr', 'username': 'paintthetow'}, 'poll_id': '5226957452427133380', 'option_ids': [0]}, 'update_id': 617129492}
user User object (3) in state
[ menu ]
fallback to  <class 'tbot.exceptions.fallback_to_menu.FallbackToMenu'>
<class 'tbot.exceptions.fallback_to_menu.FallbackToMenu'>
Runned class Menu
2022-05-27 16:42:55,153 - telegram.ext.dispatcher - ERROR - No error handlers are registered, logging exception.
Traceback (most recent call last):
  File "/Users/igor.tsupko/web/may-cat.github/eoss-bot/django-app/tbot/convmachine.py", line 200, in _basic_handler
    possible_states = self._get_next_possible_states(user_state, handler_type)
  File "/Users/igor.tsupko/web/may-cat.github/eoss-bot/django-app/tbot/convmachine.py", line 251, in _get_next_possible_states
    raise FallbackToMenu
tbot.exceptions.fallback_to_menu.FallbackToMenu

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/usr/local/lib/python3.9/site-packages/telegram/ext/dispatcher.py", line 555, in process_update
    handler.handle_update(update, self, check, context)
  File "/usr/local/lib/python3.9/site-packages/telegram/ext/handler.py", line 198, in handle_update
    return self.callback(update, context)
  File "/Users/igor.tsupko/web/may-cat.github/eoss-bot/django-app/tbot/convmachine.py", line 190, in _custom_poll_answer_handler
    self._basic_handler(update, context, PollAnswerHandler)
  File "/Users/igor.tsupko/web/may-cat.github/eoss-bot/django-app/tbot/convmachine.py", line 222, in _basic_handler
    self.fallbacks[exception_type]['handler'].handle(update=update, context=context, user=user)
  File "/Users/igor.tsupko/web/may-cat.github/eoss-bot/django-app/tbot/lib/handler.py", line 68, in handle
    self.run(update, context, user)
  File "/Users/igor.tsupko/web/may-cat.github/eoss-bot/django-app/tbot/handlers/menu.py", line 44, in run
    update.message.reply_text("🏠 Добро пожаловать домой, выберите действие:", reply_markup=markup)
AttributeError: 'NoneType' object has no attribute 'reply_text'
```


Что нужно сделать

- Протестировать все правильные сценарии
- Протестировать неправильные сценарии (например, отправку опроса не вовремя или не там)