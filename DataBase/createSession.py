from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from DataBase.db import engine

async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)()