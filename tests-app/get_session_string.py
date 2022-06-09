from telethon import TelegramClient
from telethon.sessions import StringSession
import os

api_id = int(os.environ.get("TG_API_ID"))
api_hash = os.environ.get("TG_API_HASH")


with TelegramClient(StringSession(), api_id, api_hash) as client:
    print("Session string:", client.session.save())