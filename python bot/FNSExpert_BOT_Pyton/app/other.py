import re
import os
from aiogram.types import ContentType, BufferedInputFile, InputMediaPhoto, InputMediaVideo
import requests
separator1 = '\x1F'
separator2 = '\x1E'
separator3 = '\x1D'



#Превращает матрицу {matrix} в текст и записывает его в текстовый файл {file}
def incapsulate_changed_matrix(file, matrix):
    matrix_text = ''
    for row in matrix:
        if matrix.index(row) != 0:
            matrix_text += f"\n"
        for element in row:
            if row.index(element) != 0:
                matrix_text += f";{element}"
            else:
                matrix_text += f"{element}"
    file.write(matrix_text)


#Превращает текст из {file} в матрицу и возвращает ее
def uncapsule_matrix(file):
    content = file.read()
    rows = content.strip().split('\n')
    matr = [row.split(';') for row in rows]
    return matr


#Проверка, есть ли {client_id} в первом столбце матрицы в файле "routing.env"
def user_asked_for_help(client_id):
    file = open('../routing.env', 'r', encoding='utf-8')
    matrix_client = uncapsule_matrix(file)
    file.close()
    matr_client0 = [row[0] for row in matrix_client if row]
    if str(client_id) in matr_client0:
        return True
    else:
        return False


#Возвращает индекс стоки из файла "routing.env", содержащую в первом столбце {client_id}
def user_index(client_id):
    file = open('../routing.env', 'r', encoding='utf-8')
    matrix_client = uncapsule_matrix(file)
    file.close()
    index = [matrix_client.index(row) for row in matrix_client if str(client_id) in row]
    if index:
        return index[0]
    else:
        return -1


#Проверка, воззвращающая True, если в файле "routing.env" у клиента {user_id} есть оператор
def user_in_dialog(user_id):
    file = open('../routing.env', 'r', encoding='utf-8')
    matrix_client = uncapsule_matrix(file)
    file.close()
    matr_client0 = [row for row in matrix_client if str(user_id) in row]
    if matr_client0 and len(matr_client0[0]) > 2:
        return True
    else:
        return False


#Проверка, находится ли бот {bot} в группе {chat_id} (учитывая, что бот может не иметь соответствующего чата)
async def bot_in_chat(chat_id, bot):
    try:
        chat_members = await bot.get_chat_administrators(chat_id)
        for member in chat_members:
            if member.user.id == bot.id:
                return True
        return False
    except Exception:
        return False


# Ищет первую свободную группу у оператора, находящегося на {i}-ой строке файла "indexing.env"
# Проверка проходит путем поиска групп из соответствующей строки из файла "indexing.env"
# в файле "routing.env", по очереди (сначала проверяется, есть ли первая группа в файле "routing.env",
# затем вторая и тд)
def free_group_index(i):
    file = open('../routing.env', 'r', encoding='utf-8')
    matrix_client = uncapsule_matrix(file)
    file.close()
    file = open('../indexing.env', 'r', encoding='utf-8')
    matrix = uncapsule_matrix(file)
    file.close()
    matr_client1 = [row[2] for row in matrix_client if len(row) > 2]
    for elem in matrix[i]:
        if matrix[i].index(elem) != 0 and elem not in matr_client1:
            return matrix[i].index(elem)
    return -1


# Возвращает id строки оператора, работающего с {first_id}. {message} нужен для проверки, от кого пришло
# обращение к методу: от оператора или от клиента
def get_second_id_by_first_id(first_id, message):
    file = open('../routing.env', 'r', encoding='utf-8')
    matrix_client = uncapsule_matrix(file)
    file.close()
    if is_operator(message):
        matr_client0 = [row[2] for row in matrix_client]
        i = matr_client0.index(str(first_id))
        return matrix_client[i][0]
    else:
        matr_client0 = [row[0] for row in matrix_client]
        i = matr_client0.index(str(first_id))
        return matrix_client[i][2]


#Возвращает id строки из файла "routing.env", в которой находится {user_id}
def connection_exists_for_user(user_id):
    file = open('../routing.env', 'r', encoding='utf-8')
    matrix_client = uncapsule_matrix(file)
    file.close()
    connected = [matrix_client.index(row) for row in matrix_client if str(user_id) in row]
    return connected[0]


#Превращает текст в файле "capsule.env" в матрицу и возвращает её
def uncapsule_capsule():
    file = open('../capsule.env', 'r', encoding='utf-8')
    rows = file.read().split('\n')
    matr = [row.split(separator3) for row in rows]
    return matr


#Превращает матрицу {capsule} в соответственно размеченный текст и помещает его в файл "capsule.env"
def incapsulate_changed_capsule(capsule):
    file = open('../capsule.env', 'w', encoding='utf-8')
    capsule_text = ''
    for row in capsule:
        if capsule.index(row) != 0:
            capsule_text += f"\n"
        for element in row:
            if row.index(element) != 0:
                capsule_text += separator3+f"{element}"
            else:
                capsule_text += f"{element}"
    file.write(capsule_text)


#Проверка, находится ли в файле "capsule.env" комбинация {client_id} + {ident} + {chat_id}
def is_in_capsule(client_id, ident, chat_id):
    file = open('../capsule.env', 'r', encoding='utf-8')
    capsule_matrix = uncapsule_capsule()
    file.close()
    for row in capsule_matrix:
        if row[0] == str(client_id) and row[1] == str(ident) and row[2] == str(chat_id):
            return True
    return False


#Возвращает индекс строки из файла "capsule.env", в которой есть {client_id}
def row_in_capsule_index(client_id):
    file = open('../capsule.env', 'r', encoding='utf-8')
    capsule_matrix = uncapsule_capsule()
    file.close()
    index = [capsule_matrix.index(row) for row in capsule_matrix if str(client_id) in row]
    if index:
        return index[0]
    else:
        return -1


#Возвращает {chat_id} по {client_id} (выбор ведется в файле "routing.env")
def get_chat_id_by_client_id(client_id):
    file = open('../routing.env', 'r', encoding='utf-8')
    matrix_client = uncapsule_matrix(file)
    file.close()
    matr_client0 = [row[0] for row in matrix_client]
    i = matr_client0.index(str(client_id))
    caht_id = matrix_client[i][2]
    return caht_id


#Возвращает {ID} по {client_id} (выбор ведется в файле "routing.env")
def get_ID_by_client_id(client_id):
    file = open('../routing.env', 'r', encoding='utf-8')
    matrix_client = uncapsule_matrix(file)
    file.close()
    matr_client0 = [row[0] for row in matrix_client]
    i = matr_client0.index(str(client_id))
    ident = matrix_client[i][1]
    print(ident)
    return ident


# Полученное сообщение message инкапсулируется в файл "capsule.env"
# Сначала проверяется тип сообщения, а затем инкапсулируется содержимое
# Первые три элемента - это client_id, ident и соответствующий по файлу "routing.env" идентификатор chat_id
# Четвертый элемент - это лог сообщений
# Если комбинации client_id + ident + chat_id нет в файле capsule, то она записывается и ей добавляется лог.
# Если есть, к логу добавляются новое сообщение
async def incapsulate_message(message):
    client_id = message.from_user.id
    chat_id = get_chat_id_by_client_id(client_id)
    ident = get_ID_by_client_id(client_id)
    mes_text = if_empty_text(message)
    log_for_capsulation = ''

    if message.forward_date:
        msg_frvrd = forward_from_id(message)
        file_name = get_file_info(message)
        log_for_capsulation = str(client_id) + separator1 + 'пересылка' + separator1 + str(msg_frvrd) + separator1 + file_name[0]
    elif message.reply_to_message:
        file_name = get_file_info(message)
        reply_file_name = get_file_info(message.reply_to_message)
        mes_text = if_empty_text(message)
        rep_mes_text = if_empty_text(message.reply_to_message)
        log_for_capsulation = str(client_id) + separator1 + 'ответ' + separator1 + rep_mes_text + separator1 \
                              + mes_text + separator1 + reply_file_name[0] + separator1 + file_name[0]
    elif message.sticker:
        log_for_capsulation = str(client_id) + separator1 + 'стикер' + separator1 + message.sticker.file_id
    elif message.content_type == ContentType.TEXT:
        log_for_capsulation = str(client_id) + separator1 + 'сообщение' + separator1 + mes_text
    elif message.content_type == ContentType.PHOTO:
        file_name = f"photo_{message.photo[-1].file_id}.jpg"
        log_for_capsulation = str(client_id) + separator1 + 'изображение' + separator1 + file_name + separator1 + mes_text
    elif message.content_type == ContentType.VIDEO:
        file_name = message.video.file_name
        log_for_capsulation = str(client_id) + separator1 + 'видео' + separator1 + file_name + separator1 + mes_text
    elif message.content_type == ContentType.DOCUMENT:
        file_name = message.document.file_name
        log_for_capsulation = str(client_id) + separator1 + 'документ' + separator1 + file_name + separator1 + mes_text
    elif message.content_type == ContentType.VOICE:
        file_name = f"voice_{message.voice.file_id}.mp3"
        log_for_capsulation = str(client_id) + separator1 + 'голосовое' + separator1 + file_name + separator1 + mes_text
    elif message.content_type == ContentType.AUDIO:
        file_name = message.audio.file_name
        log_for_capsulation = str(client_id) + separator1 + 'аудио' + separator1 + file_name + separator1 + mes_text
    elif message.content_type == ContentType.ANIMATION:
        file_name = message.animation.file_name
        log_for_capsulation = str(client_id) + separator1 + 'анимация' + separator1 + file_name + separator1 + mes_text
    capsulate_log(log_for_capsulation, client_id, chat_id, ident)


# Экранирование текста {text}, чтобы не возникало конфликтов с parse_mode='MarkdownV2'
def escape_markdown_v2(text):
    escape_chars = r'(?!\*\*\*)&(?!___)&[_*[\]()~`>#+-=|{}.!]'
    return re.sub(escape_chars, r'\\\g<0>', text)


# Экранирование текста {text} и отправка сообщения {message} получателю {destination} ботом {bot}.
# Здесь учитываются уникальные отправки сообщений различных типов:
# Стикер, текст, картинка, видео, документ, голосовое сообщение, аудио, анимация (гиф файлы)
async def resending_message_of_type(bot, message, destination, text):
    if text:
        text = escape_markdown_v2(text)
    if message.content_type == ContentType.STICKER:
        await bot.send_sticker(chat_id=destination, sticker=message.sticker.file_id)
    elif message.content_type == ContentType.TEXT:
        await bot.send_message(chat_id=destination, text=text, parse_mode='MarkdownV2')
    elif message.content_type == ContentType.PHOTO:
        await send_photo_message(bot, message, destination, text)
    elif message.content_type == ContentType.VIDEO:
        await send_video_message(bot, message, destination, text)
    elif message.content_type == ContentType.DOCUMENT:
        await send_document_message(bot, message, destination, text)
    elif message.content_type == ContentType.VOICE:
        await send_voice_message(bot, message, destination, text)
    elif message.content_type == ContentType.AUDIO:
        await send_audio_message(bot, message, destination, text)
    elif message.content_type == ContentType.ANIMATION:
        await send_animation_message(bot, message, destination, text)


# Метод подготовки и отправки картинки
async def send_photo_message(bot, message, destination, text):
    file_id = message.photo[-1].file_id
    file_name = f"photo_{file_id}.jpg"
    file_got = await bot.get_file(file_id)
    file_data = await bot.download_file(file_got.file_path)
    file_binary = file_data.read()
    image = BufferedInputFile(file_binary, filename=file_name)
    await bot.send_photo(chat_id=destination, photo=image, caption=text, parse_mode='MarkdownV2')


# Метод подготовки и отправки видео
async def send_video_message(bot, message, destination, text):
    file_id = message.video.file_id
    file_name = message.video.file_name
    file_got = await bot.get_file(file_id)
    file_data = await bot.download_file(file_got.file_path)
    file_binary = file_data.read()
    video = BufferedInputFile(file_binary, filename=file_name)
    await bot.send_video(chat_id=destination, video=video, caption=text, parse_mode='MarkdownV2')


# Метод подготовки и отправки документа
async def send_document_message(bot, message, destination, text):
    file_id = message.document.file_id
    file_name = message.document.file_name
    file_got = await bot.get_file(file_id)
    file_data = await bot.download_file(file_got.file_path)
    file_binary = file_data.read()
    document = BufferedInputFile(file_binary, filename=file_name)
    await bot.send_document(chat_id=destination, document=document, caption=text, parse_mode='MarkdownV2')


# Метод подготовки и отправки голосового сообщения
async def send_voice_message(bot, message, destination, text):
    file_id = message.voice.file_id
    file_name = f"voice_{file_id}.mp3"
    file_got = await bot.get_file(file_id)
    file_data = await bot.download_file(file_got.file_path)
    file_binary = file_data.read()
    voice = BufferedInputFile(file_binary, filename=file_name)
    await bot.send_voice(chat_id=destination, voice=voice, caption=text, parse_mode='MarkdownV2')


# Метод подготовки и отправки аудио
async def send_audio_message(bot, message, destination, text):
    file_id = message.audio.file_id
    file_name = message.audio.file_name
    file_got = await bot.get_file(file_id)
    file_data = await bot.download_file(file_got.file_path)
    file_binary = file_data.read()
    audio = BufferedInputFile(file_binary, filename=file_name)
    await bot.send_audio(chat_id=destination, audio=audio, caption=text, parse_mode='MarkdownV2')


# Метод подготовки и отправки анимации
async def send_animation_message(bot, message, destination, text):
    file_id = message.animation.file_id
    file_name = message.animation.file_name
    file_got = await bot.get_file(file_id)
    file_data = await bot.download_file(file_got.file_path)
    file_binary = file_data.read()
    animation = BufferedInputFile(file_binary, filename=file_name)
    await bot.send_animation(chat_id=destination, animation=animation, caption=text, parse_mode='MarkdownV2')


# Проверка, является ли текст сообщения {message} "None". Т.е. если ткста не было, то вместо "None"
# будет отправлен пустой текст ""
def if_empty_text(message):
    if message.content_type == ContentType.TEXT:
        if message.text:
            return message.text
        else:
            return ''
    if file_of_certain_type(message):
        if message.caption:
            return message.caption
        else:
            return ''


# Отправка файла из {message} на сервер по {url} ботом {bot}. Для доступа передаются логин {serv_log} и
# пароль {serv_pas}
async def saving_file_on_server(bot, message, url, serv_log, serv_pas):
    file_info = get_file_info(message)
    file_id = file_info[1]
    file_name = file_info[0]
    file_got = await bot.get_file(file_id)
    file_data = await bot.download_file(file_got.file_path)
    file_binary = file_data.read()
    data = {
        'code': '50',
        'file_name': f'{file_name}'
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.post(url, data=data, headers=headers, auth=(serv_log, serv_pas))
    if response.text == '0':
        data = {
            'code': '5',
            'file_name': f'{file_name}',
            'file': f'{file_binary}'
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        requests.post(url, data=data, headers=headers, auth=(serv_log, serv_pas))


# Получение file_name и file_id из сообщения {message}
def get_file_info(message):
    if message.content_type == ContentType.TEXT:
        return ['', '']
    elif message.content_type == ContentType.PHOTO:
        file_id = message.photo[-1].file_id
        return [f"photo_{file_id}.jpg", file_id]
    elif message.content_type == ContentType.VIDEO:
        file_id = message.video.file_id
        return [message.video.file_name, file_id]
    elif message.content_type == ContentType.DOCUMENT:
        file_id = message.document.file_id
        return [message.document.file_name, file_id]
    elif message.content_type == ContentType.VOICE:
        file_id = message.voice.file_id
        return [f"voice_{file_id}.mp3", file_id]
    elif message.content_type == ContentType.AUDIO:
        file_id = message.audio.file_id
        return [message.audio.file_name, file_id]
    elif message.content_type == ContentType.ANIMATION:
        file_id = message.animation.file_id
        return [message.animation.file_name, file_id]


# Проверка, является ли тип сообщения одним из следующих:
# Картинка, видео, документ, голосовое сообщение, аудио, анимация (гиф файлы)
def file_of_certain_type(message):
    if message.content_type == ContentType.PHOTO or message.content_type == ContentType.VIDEO or message.content_type == ContentType.DOCUMENT or message.content_type == ContentType.VOICE or message.content_type == ContentType.AUDIO or message.content_type == ContentType.ANIMATION:
        return True
    else:
        return False


# Корректная запись текста в "capsule.env". Если файл пустой, то записываем {capsulated_text} с начала.
# Если файл не пустой, то делаем отступ, а лишь затем записываем {capsulated_text}.
def capsulate_new_text(capsulated_text):
    file = open('../capsule.env', 'r', encoding='utf-8')
    file_is_empty = file.read() == ''
    file.close()
    if file_is_empty:
        file = open('../capsule.env', 'w', encoding='utf-8')
        file.write(capsulated_text)
        file.close()
    else:
        file = open('../capsule.env', 'a', encoding='utf-8')
        capsulated_text = '\n' + capsulated_text
        file.write(capsulated_text)
        file.close()


# Проверка, есть ли в "capsule.env" комбинация из client_id + ident + chat_id. Если есть,
# то дописываем новый лог {log_for_capsulation} в конец существующего. Иначе записываем его на новую строку
def capsulate_log(log_for_capsulation, client_id, chat_id, ident):
    if is_in_capsule(client_id, ident, chat_id):
        log_for_capsulation = separator2 + log_for_capsulation
        capsule = uncapsule_capsule()
        i = row_in_capsule_index(client_id)
        capsule[i][2] += log_for_capsulation
        incapsulate_changed_capsule(capsule)
    else:
        log_for_capsulation = str(client_id) + separator3 + str(ident) + separator3 + chat_id + separator3 + log_for_capsulation
        capsulate_new_text(log_for_capsulation)


#Отдельная проверка на то, отправленно {message} из  беседы или из группы
def forward_from_id(message):
    if message.forward_from_chat:
        return message.forward_from_chat.id
    elif message.forward_from:
        return message.forward_from.id


# Проверка на то, является ли {text} словом-триггером из списка triggers
def trigger_wording(text):
    triggers = ['Каталог услуг', 'Скачать прайс', 'Контакты', 'Заказать звонок', 'ЗАКОНЧИТЬ ДАННЫЙ ДИАЛОГ', 'Вернуться в главное меню', 'Связаться с оператором']
    if text in triggers:
        return True
    else:
        return False


# Данный метод возвращает лог и состояние по комбинации client_id  + ident + operator_id
# из файла "capsule.env"
def get_log_by_id(client_id, ident, operator_id):
    file = open('../capsule.env', 'r', encoding='utf-8')
    capsule_matrix = uncapsule_capsule()
    file.close()
    i = [capsule_matrix.index(row) for row in capsule_matrix if str(client_id) == row[0] and str(ident) == row[1] and str(operator_id) == row[2]]

    if i:
        i = i[0]
        return [capsule_matrix[i][3], 'Завершена']
    else:
        return ['', 'Отказ']


# Проверка на то, является ли отправитель {message} оператором (если id чата отправителя
# есть в файле "indexing.env", то он считается оператором)
def is_operator(message):
    file = open('../indexing.env', 'r', encoding='utf-8')
    matrix = uncapsule_matrix(file)
    file.close()
    matr0 = [row for row in matrix if str(message.chat.id) != row[0] and str(message.chat.id) in row ]
    if matr0 or str(message.chat.id) == str(os.getenv('GROUPCHATID')):
        return True
    else:
        return False
