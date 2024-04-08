import asyncio
import os

from aiogram import Bot, Dispatcher

from Bot.routers.main_router import main_router
from Bot.routers.router500 import router500
from Bot.routers.router3000 import router3000
from Bot.routers.self_router import self_router

from dotenv import load_dotenv

load_dotenv()

bot = Bot(token=str(os.getenv('TOKEN')))

dp = Dispatcher()
dp.include_routers(
    main_router,
    router500,
    router3000,
    self_router

)

async def main():
    print('Бот запущен')
    await bot.delete_webhook(drop_pending_updates=False)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
