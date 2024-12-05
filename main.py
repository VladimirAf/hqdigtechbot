import asyncio
from aiogram import Bot, Dispatcher
from config import API_TOKEN
from handlers import register_handlers
from database import create_table

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

async def main():
    await create_table()  # Создаем таблицы в БД
    register_handlers(dp)  # Регистрируем хэндлеры
    await dp.start_polling(bot)  # Запускаем бота

if __name__ == "__main__":
    asyncio.run(main())
