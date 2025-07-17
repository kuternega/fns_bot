from aiogram import Router, Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
import os
from dotenv import load_dotenv

import app.other as oth

# Данный код работает с ботом B
load_dotenv()
token = os.getenv('TOKEN_B')
bot = Bot(token=token)
dp = Dispatcher()
router = Router()


#Инициализация группы. Добавляет id группы в список, чтобы в нее отправлять сообщения клиента, если оператор захочет установить с ним связь
@router.message(Command('init'))
async def initialize_group(message: Message):
    #Поиск создателя группы, чтобы добавить его в общий список и
    #сопоставлять с ним клиентов в будущем
    chtid = message.chat.id
    admins = await bot.get_chat_administrators(chat_id=chtid)
    creator = [admin.user.id for admin in admins if admin.status == 'creator']

    if creator:
        file = open('../indexing.env', 'r')
        matrix = oth.uncapsule_matrix(file)
        file.close()

        #Если создатель уже существует в файле, то добавляем в его строку, в конец, индексируемую
        #группу. Иначе добавляем его в конец списка с группой, которая только
        #что была проиндексирована
        i = oth.creator_exists(creator[0])
        if i != -1:
            if not oth.already_inited(i, chtid):
                matrix[i].append(str(chtid))
                file = open('../indexing.env', 'w')
                oth.incapsulate_changed_matrix(file, matrix)
                file.close()
        else:
            file = open('../indexing.env', 'r')
            file_is_empty = file.read() == ''
            file.close()
            if file_is_empty:
                file = open('../indexing.env', 'a')
                file.write(f"{creator[0]};{chtid}")
                file.close()
            else:
                file = open('../indexing.env', 'a')
                file.write(f"\n{creator[0]};{chtid}")
                file.close()

        await message.answer('Группа проиндексирована.')
    else:
        await message.answer('Не удалось найти создателя группы.')
