import os
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine

from dotenv import load_dotenv


load_dotenv()

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

# Create ASYNC Engine

engine = create_async_engine(
    url='postgresql+asyncpg://hui:TnqlbevWlfuFkxoZ6wYG3zMA6KzMRRv3@dpg-cns54jud3nmc739b4lc0-a.oregon-postgres.render.com/words_vp5q', #f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
    echo=True,
)

class Base(DeclarativeBase):
    pass