import asyncio
import logging

from telethon import TelegramClient, events
from telethon.errors import PhoneNumberInvalidError, SessionPasswordNeededError
from telethon.tl.types import Channel, Chat

from config import api_id, api_hash, phone
from database import models, db_actions
from search_settings import result_channel_ID, set_chats, keywords

logging.basicConfig(format='[%(levelname) %(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)


async def create_tg_client():
    client = TelegramClient("Your TG script", api_id, api_hash)
    try:
        await client.connect()
        if not await client.is_user_authorized():
            await client.send_code_request(phone)
            code = input('Enter the code you received: ')
            await client.sign_in(phone, code)
    except PhoneNumberInvalidError:
        logging.info('Invalid phone number.')
    except SessionPasswordNeededError:
        password = input('Enter your 2FA password: ')
        await client.sign_in(password=password)

    return client


async def send_tg_notification(client, text='New keyword mention'):
    await client.send_message(result_channel_ID, text)


async def main():
    client = await create_tg_client()
    await models.create_db_and_tables()

    print('Got client')
    monitored_chats_id = await set_chats(client)
    await db_actions.add_chat_to_db(monitored_chats_id, client)

    @client.on(events.NewMessage(chats=monitored_chats_id, incoming=True))
    async def f(event):
        if any(word in event.message.message for word in keywords):
            chat = await event.get_chat()
            if isinstance(chat, Channel) or isinstance(chat, Chat):
                await send_tg_notification(client)
                await client.send_message('me', f'{chat.title}: {event.message.message}')
                print(f'{chat.title}: {event.message.message}')

    print("The bot is running and listening to messages in chats:")
    print(await db_actions.get_tracked_chats())

    await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
