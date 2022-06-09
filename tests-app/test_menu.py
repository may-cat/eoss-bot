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
# Тыкаемся в бота и получаем менюху.
# """
#
# @pytest.mark.asyncio
# async def test_start(conv: Conversation):
#     await conv.send_message("любое сообщение")
#     msg: Message = await conv.get_response()
#     assert "Добро пожаловать домой" in msg.text
#
#
#
