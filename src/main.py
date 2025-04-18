import asyncio
import logging
from pathlib import Path
import sys

import colorama
from colorama import Back, Style
from telethon import TelegramClient, events
from telethon.errors import PhoneNumberInvalidError, SessionPasswordNeededError
from telethon.tl.types import Channel, Chat

from src.config import api_id, api_hash, phone, keywords, result_channel_ID
from src.database import models, db_actions

logging.basicConfig(format='[%(levelname) %(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)


async def create_tg_client():
    print(Path(sys.executable).parent)

    if getattr(sys, 'frozen', False):
        session_path = Path(sys.executable).parent / "tg_session"
    else:
        session_path = Path(__file__).parent.parent / "tg_session"

    client = TelegramClient(session_path, api_id, api_hash, system_version="4.16.30-vxCUSTOM")
    #The client's telegram version is specified to bypass the session interruption. It may be the reason for the ban.
    try:
        await client.connect()
        if not await client.is_user_authorized():
            await client.send_code_request(phone)
            code = input(Back.RED + 'Enter the code you received: ' + Style.RESET_ALL)
            await client.sign_in(phone, code)
    except PhoneNumberInvalidError:
        logging.info('Invalid phone number.')
    except SessionPasswordNeededError:
        password = input(Back.RED + 'Enter your 2FA password: ' + Style.RESET_ALL)
        await client.sign_in(password=password)

    return client


async def send_tg_notification(client, chat_title, message, author):
    await client.send_message(result_channel_ID, f'New keyword mention: \n {chat_title} \n Author: @{author}\n{message}')


async def main():
    client = await create_tg_client()

    try:
        await models.create_db_and_tables()
    except OSError:
        print("Database is not running")
        return

    change_settings = (input(
        "You can change your chat settings right now. If you don't need it, press Enter.\n"
        "If you Want to Enter to the control menu? Enter 1.\nyour answer is:").strip())
    if change_settings != '' and int(change_settings) == 1:
        await db_actions.script_handler(client)

    monitored_chats_id = await db_actions.get_id_tracked_chats()
    if monitored_chats_id:

        @client.on(events.NewMessage(chats=monitored_chats_id, incoming=True))
        async def f(event):
            if any(word in event.message.message for word in keywords.split(',')):
                chat = await event.get_chat()
                author = await event.get_sender()
                if isinstance(chat, Channel) or isinstance(chat, Chat):
                    await send_tg_notification(client, chat.title, event.message.message, author.username)

        colorama.init()
        print(Back.YELLOW + "The bot is running and listening to messages in chats:" + Style.RESET_ALL)
        print(await db_actions.get_tracked_chats())

        await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
