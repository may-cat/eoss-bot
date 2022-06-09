# import asyncio
# import os
# import threading
#
# import pytest
# from telethon import TelegramClient
# from telethon.sessions import StringSession
# from telethon.tl.custom.conversation import Conversation
# from telethon.tl.custom.message import Message, MessageButton
#
# """
# Обнуляем верификацию, стучимся к юзеру и проходим по сценарию верификации. Проставляем верификацию обратно.
# """
#
# @pytest.mark.asyncio
# async def test_start(conv: Conversation):
#     # TODO: надо реализовать
#     await conv.send_message("/start")
#     msg: Message = await conv.get_response()
#     assert "Добро пожаловать домой" in msg.text
#
#
#
