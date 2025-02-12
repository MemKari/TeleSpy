from sqlalchemy import select
from telethon.errors import RPCError

from src.database.models import get_async_session, Chats


async def add_chat_to_db(tg_chats: list, client):
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
