import asyncio

from app.handlers import bot, dp
from app.handlers import router


# подключаем бота, вводим токен из BotFather
async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

# должно быть приветственное сообщение, но не выходит

 # @dp.message.handlers(content_types=["new_chat_members"])
 # async def new_member(message):
 #    await bot.send_message(message.chat_id, 'Добрый день! Нажмите кнопку "Начать"', reply_markup=kb.start)

ADMINS = [123456789, 987654321]
# для красоты в терминале, чтобы при остановке не ошибка, а текст
if __name__ == '__main__':
        try:
                asyncio.run(main())
        except KeyboardInterrupt:
                print('Бот выключен')

