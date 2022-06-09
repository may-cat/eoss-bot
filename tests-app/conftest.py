import asyncio
import os
import threading
import pytest
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.custom.conversation import Conversation

@pytest.fixture(autouse=True, scope="session")
def bot():
    """Start bot to be tested."""
    stop_event = threading.Event()
    yield
    stop_event.set()

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def telegram_client():
    api_id = int(os.environ.get("TG_API_ID"))
    api_hash = os.environ.get("TG_API_HASH")
    session_str = os.environ.get("TG_SESS")
    client = TelegramClient(
        StringSession(session_str), api_id, api_hash, sequential_updates=True
    )
    await client.connect()
    await client.get_me()
    await client.get_dialogs()
    yield client
    await client.disconnect()
    await client.disconnected


@pytest.fixture(scope="session")
async def conv(telegram_client) -> Conversation:
    """Open conversation with the bot."""
    async with telegram_client.conversation(
            "@express_tenants_meeting_bot", timeout=10, max_messages=10000
    ) as conv:
        conv: Conversation
        yield conv

@pytest.fixture(scope="session")
async def sectionchat(telegram_client) -> Conversation:
    """Open conversation with the bot."""
    async with telegram_client.conversation(
            -716321959, timeout=10, max_messages=10000
    ) as conv:
        conv: Conversation

        # await conv.send_message("/start")
        # await conv.get_response()  # Welcome message
        yield conv
