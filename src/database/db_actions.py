from sqlalchemy import select, delete
from sqlalchemy.future import select as future_select
from telethon.errors import RPCError

from src.database.models import get_async_session, Chats
from src.search_settings import set_chats


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


async def delete_chats():
    async with get_async_session() as session:
        tracked_chats = await get_tracked_chats()
        if not tracked_chats:
            print("Right now, you are not monitoring any chats and cannot delete them.")
            return

        print('; '.join(tracked_chats))
        chat_names_to_delete = input(
            "Copy the names of the chats you want to delete and paste them separated by semicolon(;): ").split(';')
        chat_names_to_delete = [name.strip() for name in chat_names_to_delete if name.strip()]

        if not chat_names_to_delete:
            print("No valid chat names provided. Exiting...")
            return

        stmt = delete(Chats).where(Chats.chat_name.in_(chat_names_to_delete))
        await session.execute(stmt)
        await session.commit()
        print(f"Deleted chats: {', '.join(chat_names_to_delete)}")


async def get_tracked_chats() -> list:
    async with get_async_session() as session:
        chat_list = await session.execute(future_select(Chats.chat_name))
        result = chat_list.scalars().all()
        if not result:
            print("Right now, you are not tracking messages in any chats.")
        return result


async def get_id_tracked_chats() -> list:
    async with get_async_session() as session:
        chat_list = await session.execute(future_select(Chats.chat_id))
        result = chat_list.scalars().all()
        if not result:
            print("Right now, you are not tracking messages in any chats.")
        return result


async def script_handler(client) -> False or None:
    def choose_action() -> str:
        user_answer = input('''Please select one option and enter its number:
              1. I want to start tracking new chats.
              2. I want to see a list of all the chats I'm monitoring.
              3. I want to remove a chat from the monitored list.
              4. Exit.\nyour answer is:'''.strip())
        return user_answer

    try:
        action_number = int(choose_action())
    except ValueError:
        print('Enter a single digit that corresponds to the option you need. Do not enter any additional characters.')
        action_number = choose_action()

    if action_number == 1:
        monitored_chats_id = await set_chats(client)
        await add_chat_to_db(monitored_chats_id, client)
    if action_number == 2:
        await get_tracked_chats()
    if action_number == 3:
        await delete_chats()
    if action_number == 4:
        return False
