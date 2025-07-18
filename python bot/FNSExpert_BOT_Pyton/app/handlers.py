import os
import requests
import re
from dotenv import load_dotenv
from aiogram import F, Router, Bot, Dispatcher
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, FSInputFile
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import app.keyboards as kb
import app.content_text as ct
import app.other as oth

# Данный код работает с ботом A
load_dotenv()
token = os.getenv('TOKEN_A')
bot = Bot(token=token)
dp = Dispatcher()
router = Router()
serv_log = os.getenv('serv_log')
serv_pas = os.getenv('serv_pas')
url = os.getenv('url')


class Register(StatesGroup):
    name = State()
    pers_data = State()
    question = State()
    req_type = State()


# простой ответ
@router.message(CommandStart())
async def cmd_start(message: Message):
    if not oth.is_operator(message):
        sent_message = await bot.send_message(message.chat.id, "Бот может сохранять ваши персональные данные.")
        await bot.pin_chat_message(chat_id=message.chat.id, message_id=sent_message.message_id)
        await message.answer(f'{ct.Hello_text}, {message.from_user.first_name}\\! {ct.Hello_text1}', reply_markup=kb.main, parse_mode='MarkdownV2')


# узнаем id юзера и чата по команде
@router.message(Command('userid'))
async def send_user_info(message: Message):
    user_id = message.from_user.id
    userid = f'Ваш user_id: {user_id}'
    await message.reply(userid)


@router.message(Command('chatid'))
async def send_user_info(message: Message):
    chat_id = message.chat.id
    chatid = f'Ваш chat_id: {chat_id}'
    await message.reply(chatid)


# ответ с ссылкой на сообщение пользователя
#       await message.reply('Чем могу помочь?')

# @router.message(Command('help'))
# async def cmd_start(message:Message):
#      await message.answer('Вы нажали на кнопку помощи')


# Ответный каталог, предложенный пользователю при выборе из главного меню
@router.message(F.text == 'Связь с оператором')
async def catalog(message: Message):
    if oth.user_in_dialog(message.from_user.id):
        await message.answer('Выберите категорию', reply_markup=kb.catalog_in_dialog)
    else:
        await message.answer('Выберите категорию', reply_markup=kb.catalog)


# тут должен подгружать файл с прайсом
@router.message(F.text == 'Скачать прайс')
async def price(message: Message):
    file_path = '../price.pdf'
    document = FSInputFile(file_path)
    await message.answer_document(document)


# Тут должен подгружаться файл с бухгалтерскими услугами
@router.message(F.text == 'Бухгалтерские услуги')
async def price(message: Message):
    file_path = '../buh_uslugi.pdf'
    document = FSInputFile(file_path)
    await message.answer_document(document)


# Тут должен подгружаться файл с юридическими услугами
@router.message(F.text == 'Юридические услуги')
async def price(message: Message):
    file_path = '../ur_uslugi.pdf'
    document = FSInputFile(file_path)
    await message.answer_document(document)

# обрабатываем выбранные категории
@router.callback_query(F.data == 'consultation')
async def consultation(callback: CallbackQuery):
    if oth.user_in_dialog(callback.from_user.id):
        await callback.answer('В вашем диалоге уже присутствует оператор!')
    else:
        await callback.answer('Вы выбрали категорию Консультация')
        await callback.message.answer(ct.consultation, reply_markup=kb.sub_catalog_button, parse_mode='MarkdownV2')


@router.callback_query(F.data == 'requirement')
async def requirement(callback: CallbackQuery):
    await callback.answer('Вы выбрали категорию Требования')
    await callback.message.answer(ct.requirement, reply_markup=kb.sub_catalog_button, parse_mode='MarkdownV2')


@router.callback_query(F.data == 'interrogation')
async def interrogation(callback: CallbackQuery):
    await callback.answer('Вы выбрали категорию Допрос, дача пояснений, комиссии')
    await callback.message.answer(ct.interrogation, reply_markup=kb.sub_catalog_button, parse_mode='MarkdownV2')


@router.callback_query(F.data == 'audits')
async def audits(callback: CallbackQuery):
    await callback.answer('Вы выбрали категорию Налоговые проверки')
    await callback.message.answer(ct.audits, reply_markup=kb.sub_catalog_button, parse_mode='MarkdownV2')


@router.callback_query(F.data == 'declaration')
async def declaration(callback: CallbackQuery):
    await callback.answer('Вы выбрали категорию Декларации')
    await callback.message.answer(ct.declaration, reply_markup=kb.sub_catalog_button, parse_mode='MarkdownV2')


@router.callback_query(F.data == 'lawyer')
async def lawyer(callback: CallbackQuery):
    await callback.answer('Вы выбрали категорию Представление интересов в суде')
    await callback.message.answer(ct.lawyer, reply_markup=kb.sub_catalog_button, parse_mode='MarkdownV2')


'''# подумать почему работает номер только из карточки, а текстом не кушает.
@router.message(Register.phone)
async def register_number(message: Message, state: FSMContext):
    phone = ''
    if message.content_type == types.ContentType.CONTACT:
        phone = message.contact.phone_number
    elif message.content_type == types.ContentType.TEXT:
        phone = message.text.strip()
    if phone.startswith('+') or phone.isdigit():
        await state.update_data(number=phone)
        data = await state.get_data()
        callback_message = f'Заказан обратный звонок\n Имя: {data["name"]}\n Номер: {phone}'
        await message.answer(f'Ваше имя: {data["name"]}\nВаш номер: {phone}', reply_markup=kb.main)
        #await bot_a.send_message(chat_id=os.getenv('GROUPCHATID'), text=callback_message)
        await state.clear()
    else:
        await message.answer(
            'Пожалуйста, введите корректный номер телефона (например, +1234567890) или воспользуйтесь кнопкой "Отправить номер телефона"',
            reply_markup=kb.get_number)
        # ответ в подкатегории'''


@router.callback_query(F.data == 'call_operator')
async def call_for_help(callback: CallbackQuery, state: FSMContext):
    if not oth.is_operator(callback.message):
        await state.update_data(req_type='call_operator')
        await state.set_state(Register.name)
        await callback.message.answer('Как к вам обращаться:')


@router.callback_query(F.data == 'make_call')
async def call_for_help(callback: CallbackQuery, state: FSMContext):
    if not oth.is_operator(callback.message):
        await state.update_data(req_type='make_call')
        await state.set_state(Register.name)
        await callback.message.answer('Как к вам обращаться:')


@router.message(Register.name)
async def request_from_user_name(message: Message, state: FSMContext):
    if not oth.trigger_wording(message.text):
        await state.update_data(name=message.text)
        await state.set_state(Register.pers_data)
        await message.answer('Укажите предпочтительный вид связи:')
    else:
        await state.clear()
        await router.propagate_event(update_type='message', event=message, bot=message.bot)


@router.message(Register.pers_data)
async def request_from_user_city(message: Message, state: FSMContext):
    if not oth.trigger_wording(message.text):
        await state.update_data(pers_data=message.text)
        await state.set_state(Register.question)
        await message.answer('Укажите ваш вопрос:')
    else:
        await state.clear()
        await router.propagate_event(update_type='message', event=message, bot=message.bot)

'''
@router.message(Register.phone)
async def request_from_user_city(message: Message, state: FSMContext):
    if not oth.trigger_wording(message.text):
        phone = ''
        if message.content_type == types.ContentType.CONTACT:
            phone = message.contact.phone_number
        elif message.content_type == types.ContentType.TEXT:
            phone = message.text.strip()
        await state.update_data(phone=phone)
        await state.set_state(Register.mail)
        await message.answer('Введите Вашу электронную почту:')
    else:
        await state.clear()
        await router.propagate_event(update_type='message', event=message, bot=message.bot)'''

'''
@router.message(Register.mail)
async def request_from_user_city(message: Message, state: FSMContext):
    if not oth.trigger_wording(message.text):
        await state.update_data(mail=message.text)
        await state.set_state(Register.question)
        await message.answer('Введите Ваш вопрос:')
    else:
        await state.clear()
        await router.propagate_event(update_type='message', event=message, bot=message.bot)'''


@router.message(Register.question)
async def request_from_user_question(message: Message, state: FSMContext):
    client_id = message.from_user.id
    await state.update_data(client_id=client_id)
    await state.update_data(question=message.text)
    data = await state.get_data()

    groupchat_id = os.getenv('GROUPCHATID')
    client_info = ''
    if data["req_type"] == 'call_operator':
        #client_info = f'Информация о клиенте:\nФИО:{data["name"]}\nРегион налоговой:{data["city"]}\nНомер телефона:{data["phone"]}:\nEmail:{data["mail"]}:\nТема обращения:{data["question"]}\nID клиента:{data["client_id"]}'
        client_info = f'Информация о клиенте:\nЛичные данные:{data["name"]}\nКонтактные данные:{data["pers_data"]}\nТема обращения:{data["question"]}\nID клиента:{data["client_id"]}'
        await bot.send_message(chat_id=groupchat_id, text=client_info, reply_markup=kb.get_client)
    elif data["req_type"] == 'make_call':
        client_info = f'Информация о клиенте:\nЛичные данные:{data["name"]}\nКонтактные данные:{data["pers_data"]}:\nТема обращения:{data["question"]}\nID клиента:{data["client_id"]}'
        await bot.send_message(chat_id=groupchat_id, text=client_info)


    #Записываем id пользователя в routing, если его там еще нет
    if not oth.user_asked_for_help(client_id):
        data = {
            'code': '1',
            'customer_id': f'{client_id}',
            'fio': f'{data["name"]}',
            'email': f'{data["pers_data"]}',
            'request_text': f'{data["question"]}'
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.post(url, data=data, headers=headers, auth=(serv_log, serv_pas))

        file = open('../routing.env', 'r', encoding='utf-8')
        file_is_empty = file.read() == ''
        file.close()
        if file_is_empty:
            file = open('../routing.env', 'a', encoding='utf-8')
            file.write(f'{client_id};{response.text}')
            file.close()
        else:
            file = open('../routing.env', 'a', encoding='utf-8')
            file.write(f'\n{client_id};{response.text}')
            file.close()
    await message.answer('Оператор свяжется с Вами в ближайшее время...', reply_markup=kb.main)
    await state.clear()


#При нажатии на кнопку "принять клиента" в чате операторов
#мы проверяем, оставлял ли клиент заявку и забрал ли ее уже кто-то
#Если оставил, но никто не принял, то занимаем оператором, нажавшим на кнопку
@router.callback_query(F.data == 'get_client')
async def process_get_client_callback(callback_query: CallbackQuery):
    #Получение id клиента из пришедшего сообщения
    callback_text = callback_query.message.text
    pattern = r'ID клиента:(\d+)'
    match = re.search(pattern, callback_text)
    if match:
        client_id = match.group(1)
        if oth.user_asked_for_help(client_id):
            i1 = oth.user_index(client_id)
            #Если пользователю никто не помогает, то подключаем к нему первую свободную группу оператора, нажавшего на кнопку "Принять клиента"
            if not oth.user_in_dialog(client_id):
                user_full_name = callback_query.from_user.full_name

                file = open('../indexing.env', 'r', encoding='utf-8')
                matrix = oth.uncapsule_matrix(file)
                file.close()
                file = open('../routing.env', 'r', encoding='utf-8')
                matrix_client = oth.uncapsule_matrix(file)
                file.close()

                operator_id = callback_query.from_user.id
                i = [matrix.index(row) for row in matrix if str(operator_id) == row[0]]
                if i:
                    i = i[0]
                    j = oth.free_group_index(i)
                    if j != -1:
                        if await oth.bot_in_chat(matrix[i][j], bot):
                            matrix_client[i1].append(str(matrix[i][j]))
                            request_id = oth.get_ID_by_client_id(client_id)

                            data = {
                                'code': '2',
                                'ID': f'{request_id}',
                                'emp_id': f'{operator_id}'
                            }
                            headers = {
                                'Content-Type': 'application/x-www-form-urlencoded'
                            }
                            response = requests.post(url, data=data, headers=headers, auth=(serv_log, serv_pas))
                            file = open('../routing.env', 'w', encoding='utf-8')
                            oth.incapsulate_changed_matrix(file, matrix_client)
                            file.close()

                            operator_chat_id = matrix[i][j]
                            await bot.send_message(chat_id=callback_query.message.chat.id,
                                                   text=f'Клиент принят пользователем: {user_full_name}')
                            await bot.send_message(chat_id=client_id, text=f'***ОПЕРАТОР ПРИСОЕДИНИЛСЯ К БЕСЕДЕ***',
                                                   parse_mode='MarkdownV2', reply_markup=kb.main_in_dialog)
                            await bot.send_message(chat_id=operator_chat_id,
                                                   text=f'***ВЫ ПРИСОЕДИНИЛИСЬ К БЕСЕДЕ С КЛИЕНТОМ***',
                                                   reply_markup=kb.operator_in_dialog, parse_mode='MarkdownV2')
                        else:
                            await bot.send_message(chat_id=callback_query.message.chat.id,
                                                   text=f'{user_full_name}, в вашей случайной свободной группе {matrix[i][j]} отсутствует FNS Expert bot, вы не можете принять в нее клиента (группа будет отозвана из списка инициализированных)! Добавьте в группу FNS Expert bot и воспользуйтесь комндой init снова!')
                            matrix[i].remove(matrix[i][j])
                            file = open('../indexing.env', 'w', encoding='utf-8')
                            oth.incapsulate_changed_matrix(file, matrix)
                            file.close()
                    else:
                        await bot.send_message(chat_id=callback_query.message.chat.id, text=f'{user_full_name}, у вас нет свободных бесед, вы не можете принять еще одного клиента! Попробуйте создать группу, добавить в нее бота и использовать команду "/init"')
                else:
                    await bot.send_message(chat_id=callback_query.message.chat.id, text=f'{user_full_name}, у вас нет ни одной группы, вы не можете принять клиента! Попробуйте создать группу, добавить в нее бота и использовать команду "/init"')
            else:
                client_info = await bot.get_chat(chat_id=client_id)
                operator_info = await bot.get_chat(chat_id=oth.get_second_id_by_first_id(client_id, callback_query))
                await bot.send_message(chat_id=callback_query.message.chat.id, text=f'Клиент {client_info.full_name} уже занят пользователем: {operator_info.full_name}')
        else:
            await bot.send_message(chat_id=callback_query.message.chat.id, text=f'Клиент уже не нуждается в помощи')
    else:
        await bot.send_message(chat_id=callback_query.message.chat.id, text=f'Заявка не содержит идентификатор клиента')


@router.message(F.text == 'Вернуться в главное меню')
async def get_back_to_main(message: Message):
    if not oth.is_operator(message):
        await message.answer('Вы вернулись в главное меню. Выберите категорию или свяжитесь с оператором', reply_markup=kb.main)


#Удаляем строку {client_id;operator_id} из файла routing
@router.message(F.text == 'ЗАКОНЧИТЬ ДАННЫЙ ДИАЛОГ')
async def disconnection(message: Message):
    if oth.is_operator(message):
        user_id = message.chat.id
    else:
        user_id = message.from_user.id
    if oth.user_in_dialog(user_id):
        file = open('../routing.env', 'r', encoding='utf-8')
        matrix = oth.uncapsule_matrix(file)
        file.close()

        i = oth.connection_exists_for_user(user_id)
        client_id = matrix[i][0]
        ident = matrix[i][1]
        operator_id = matrix[i][2]
    
        log = oth.get_log_by_id(client_id, ident, operator_id)
        data = {
            'code': '4',
            'ID': f'{ident}',
            'status': f'{log[1]}',
            'consultation_log': f'{log[0]}'
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.post(url, data=data, headers=headers, auth=(serv_log, serv_pas))

        del matrix[i]
        file = open('../routing.env', 'w', encoding='utf-8')
        oth.incapsulate_changed_matrix(file, matrix)
        file.close()
        if not oth.is_operator(message):
            await bot.send_message(chat_id=client_id, text='***ВЫ ПОКИНУЛИ БЕСЕДУ***', reply_markup=kb.main,
                                   parse_mode='MarkdownV2')
            await bot.send_message(chat_id=operator_id, text='***КЛИЕНТ ПОКИНУЛ БЕСЕДУ***',
                                   reply_markup=ReplyKeyboardRemove(),
                                   parse_mode='MarkdownV2')
        else:
            await bot.send_message(chat_id=client_id, text='***ОПЕРАТОР ПОКИНУЛ БЕСЕДУ***', reply_markup=kb.main,
                                   parse_mode='MarkdownV2')
            await bot.send_message(chat_id=operator_id, text='***ВЫ ПОКИНУЛИ БЕСЕДУ***',
                                   reply_markup=ReplyKeyboardRemove(),
                                   parse_mode='MarkdownV2')
    else:
        if not oth.is_operator(message):
            await message.answer('В данной беседе нет оператора\\!', reply_markup=kb.main, parse_mode='MarkdownV2')
        else:
            await message.answer('В данной группе нет клиента\\!', reply_markup=ReplyKeyboardRemove(),
                                 parse_mode='MarkdownV2')


#Пересылка сообщений, если соединение установлено (через файл routing)
@router.message()
async def sending_message(message: Message):
    file = open('../routing.env', 'r', encoding='utf-8')
    matrix_client = oth.uncapsule_matrix(file)
    file.close()
    if str(os.getenv('GROUPCHATID')) != str(message.chat.id):
        i = oth.user_index(message.chat.id)
    else:
        i = -1

    if i != -1:
        if message.forward_date:
            if oth.is_operator(message):
                from_id = message.chat.id
            else:
                from_id = message.from_user.id
            to_id = oth.get_second_id_by_first_id(from_id, message)
            await bot.forward_message(chat_id=to_id, from_chat_id=from_id, message_id=message.message_id)
            await oth.incapsulate_message(message)
        elif message.reply_to_message:
            if oth.is_operator(message):
                destination = matrix_client[i][0]
            else:
                destination = matrix_client[i][2]
            mes_text = oth.if_empty_text(message)
            rep_mes_text = oth.if_empty_text(message.reply_to_message)
            sending_text1 = f'***Пересланное сообщение:***\n{rep_mes_text}'
            sending_text2 = f'***Ответ на пересланное сообщение:***\n{mes_text}'

            await oth.resending_message_of_type(bot, message.reply_to_message, destination, sending_text1)
            await oth.resending_message_of_type(bot, message, destination, sending_text2)
            await oth.incapsulate_message(message)
        else:
            mes_text = oth.if_empty_text(message)
            if not oth.is_operator(message):
                destination = matrix_client[i][2]
            else:
                destination = matrix_client[i][0]
            await oth.resending_message_of_type(bot, message, destination, mes_text)
            if oth.file_of_certain_type(message):
                await oth.saving_file_on_server(bot, message, url, serv_log, serv_pas)
            await oth.incapsulate_message(message)
