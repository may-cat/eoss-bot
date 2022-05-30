## Переходим на гибкие сценарии

На данный момент:

Прописать нормальную логику

Проблемы:

0. `convmachine.py`, строка 293 — когда юзер пишет надо его имя фиксировать в БД правильно

1. у Телегама есть опция отзыва голоса, надо её реализовать нам в коде иначе получаются грёбаные дубли

```
(<class 'IndexError'>, IndexError('list index out of range'), <traceback object at 0x1098480c0>)
Traceback (most recent call last):
  File "/Users/igor.tsupko/web/may-cat.github/eoss-bot/django-app/tbot/convmachine.py", line 250, in _basic_handler
    objStep.run(update=update, context=context, user=user)
  File "/Users/igor.tsupko/web/may-cat.github/eoss-bot/django-app/tbot/handlers/receive_poll_answer.py", line 43, in run
    answer_id = answer.option_ids[0]
IndexError: list index out of range

2022-05-30 16:47:20,051 - telegram.ext.dispatcher - ERROR - No error handlers are registered, logging exception.
Traceback (most recent call last):
  File "/Users/igor.tsupko/web/may-cat.github/eoss-bot/django-app/tbot/convmachine.py", line 250, in _basic_handler
    objStep.run(update=update, context=context, user=user)
  File "/Users/igor.tsupko/web/may-cat.github/eoss-bot/django-app/tbot/handlers/receive_poll_answer.py", line 43, in run
    answer_id = answer.option_ids[0]
IndexError: list index out of range

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/usr/local/lib/python3.9/site-packages/telegram/ext/dispatcher.py", line 555, in process_update
    handler.handle_update(update, self, check, context)
  File "/usr/local/lib/python3.9/site-packages/telegram/ext/handler.py", line 198, in handle_update
    return self.callback(update, context)
  File "/Users/igor.tsupko/web/may-cat.github/eoss-bot/django-app/tbot/convmachine.py", line 234, in _custom_poll_answer_handler
    self._basic_handler(update, context, PollAnswerHandler)
  File "/Users/igor.tsupko/web/may-cat.github/eoss-bot/django-app/tbot/convmachine.py", line 274, in _basic_handler
    self.fallbacks[FallbackToMenu]['handler'].run(update=update, context=context, user=user)
  File "/Users/igor.tsupko/web/may-cat.github/eoss-bot/django-app/tbot/handlers/menu.py", line 44, in run
    update.message.reply_text("🏠 Добро пожаловать домой, выберите действие:", reply_markup=markup)
AttributeError: 'NoneType' object has no attribute 'reply_text'
```

2. Автотесты
3. Прописать сценарий запроса на аппрув и аппрув
4. Прописать меню управления своими объектами недвижимости
5. Поправить отображение результатов опроса: только последние 3-5