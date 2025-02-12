from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from src.config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME

'''Переменная metadata действительно не нужна в вашем коде, так как вы используете декларативный стиль 
определения моделей с помощью SQLAlchemy ORM, который сам управляет метаданными. Убедитесь, 
что вы вызываете Base.metadata.create_all(engine) вместо metadata.create_all(engine) для создания таблиц.'''

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


class Base(DeclarativeBase):
    ...


class Chats(Base):
    __tablename__ = 'chats_info'

    chat_id: Mapped[int] = mapped_column(primary_key=True)
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


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


# async def get_user_db(session: AsyncSession = Depends(get_async_session)):
#     yield SQLAlchemyUserDatabase(session, User)
