from sqlalchemy import select
from sqlalchemy.future import select as future_select
from telethon.errors import RPCError

from src.database.models import get_async_session, Chats


async def add_chat_to_db(tg_chats: list, client) -> None:
    async with get_async_session() as session:
        async with session.begin():
            for chat in tg_chats:
                try:
                    entity = await client.get_entity(chat)
                    new_entry = Chats(chat_id=chat, chat_name=entity.title)
                except RPCError as some_error:
                    print(f"Error receiving the chat {chat}: {some_error}")
                    continue
                except Exception as some_error:
                    print(f"Unknown error with the chat {chat}: {some_error}")
                    continue

                result = await session.execute(select(Chats).where(Chats.chat_id == chat))
                if result.scalar():
                    print(f"The {chat} is already in the database, skipping it.")
                    continue

                session.add(new_entry)


async def get_tracked_chats() -> list:
    async with get_async_session() as session:
        chat_list = await session.execute(future_select(Chats.chat_name))
        return chat_list.scalars().all()


async def script_handler():
    def choose_action() -> str:
        user_answer = input('''Please select one option and enter its number:
              1. I want to start tracking new chats.
              2. I want to see a list of all the chats I'm monitoring.
              3. I want to remove the chat from the monitored list.'''.strip())
        return user_answer

    try:
        action_number = int(choose_action())
    except ValueError:
        print('Enter a single digit that corresponds to the option you need. Do not enter any additional characters.')
        action_number = choose_action()
