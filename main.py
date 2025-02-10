import asyncio
import logging

from telethon import TelegramClient, events
from telethon.errors import PhoneNumberInvalidError, SessionPasswordNeededError
from telethon.tl.types import Channel, Chat

logging.basicConfig(format='[%(levelname) %(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

from config import api_id, api_hash, phone
from search_settings import result_channel_ID, set_chats, keywords


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

    print('Got client')
    monitored_chats_id = await set_chats(client)
    print(monitored_chats_id)


    @client.on(events.NewMessage(chats=monitored_chats_id, incoming=True))
    async def f(event):
        if any(word in event.message.message for word in keywords):
            chat = await event.get_chat()
            if isinstance(chat, Channel) or isinstance(chat, Chat):
                await send_tg_notification(client)
                await client.send_message('me', f'{chat.title}: {event.message.message}')
                print(f'{chat.title}: {event.message.message}')

    print("The bot is running and listening to messages...")
    await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
