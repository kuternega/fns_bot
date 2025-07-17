import asyncio

from app.handlers import bot, dp
from app.handlers import router


# Запуск бота
async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            print('Бот выключен')