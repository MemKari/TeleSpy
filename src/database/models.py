from contextlib import asynccontextmanager
from pathlib import Path
import sys
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import BigInteger

if getattr(sys, 'frozen', False):
    db_path = str(Path(sys.executable).parent / "database.db")
else:
    db_path = "database.db"

DATABASE_URL = f"sqlite+aiosqlite:///{db_path}"


class Base(DeclarativeBase):
    ...


class Chats(Base):
    __tablename__ = 'chats_info'

    chat_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    chat_name: Mapped[str] = mapped_column(nullable=False)

    def __repr__(self) -> str:
        return f"Chat(id={self.chat_id!r}, name={self.chat_name!r})"


# Создание таблиц в базе данных.
metadata = Base.metadata

engine = create_async_engine(DATABASE_URL)  # точка входа sql алхимии в приложение
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@asynccontextmanager
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
