import asyncio
import os
import threading
import logging
import pytest
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.custom.conversation import Conversation
from telethon.tl.custom.message import Message, MessageButton
from telethon.tl.types import InputMediaPoll, Poll, PollAnswer

"""
Формируем опрос, проходим по сценарию, получаем опрос в тестовой группе 
"""

@pytest.mark.asyncio
async def test_run_eoss(conv: Conversation, sectionchat: Conversation):
    await conv.send_message("/start")
    msg: Message = await conv.get_response()
    assert "Добро пожаловать домой," in msg.text
    await msg.click(0)
    msg: Message = await conv.get_response()
    assert "Готов запустить ЭОСС" in msg.text
    await conv.send_message(file=InputMediaPoll(
        poll=Poll(
            id=msg.chat_id,
            question="Choose variant:",
            answers=[PollAnswer("One", b'1'), PollAnswer("Two", b'2')]
        )
    ))
    msg: Message = await conv.get_response()
    assert "Готов запустить ЭОСС." in msg.text
    await msg.click(0)
    msg: Message = await conv.get_response()
    assert "Всё принято" in msg.text
    msg: Message = await sectionchat.get_response()
    # TODO: check that message appeared in "как будто группа подъезда", id = -716321959