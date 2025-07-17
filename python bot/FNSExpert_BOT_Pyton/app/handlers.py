import os, requests, re
from dotenv import load_dotenv
from aiogram import F, Router, Bot, Dispatcher, types
from aiogram.types import ContentType, Message, CallbackQuery, URLInputFile
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import app.keyboards as kb
import app.content_text as ct
import app.other as oth
# Данный код работает с ботом A
load_dotenv()
token_a = os.getenv('TOKEN_A')
token_b = os.getenv('TOKEN_B')
bot_a = Bot(token=token_a)
bot_b = Bot(token=token_b)
dp = Dispatcher()
router = Router()
serv_log = os.getenv('serv_log')
serv_pas = os.getenv('serv_pas')
url = os.getenv('url')

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


class Register(StatesGroup):
    name = State()
    number = State()


class RequestFromUser(StatesGroup):
    name = State()
    question = State()
    letter = State()
    city = State()


# простой ответ
@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f'{ct.Hello_text}, {message.from_user.first_name}\\! {ct.Hello_text1}', reply_markup=kb.main, parse_mode='MarkdownV2')

# ответ с ссылкой на сообщение пользователя
#       await message.reply('Чем могу помочь?')

# @router.message(Command('help'))
# async def cmd_start(message:Message):
#      await message.answer('Вы нажали на кнопку помощи')


@router.message(RequestFromUser.name)
async def request_from_user_name(message: Message, state: FSMContext):
    if not oth.trigger_wording(message.text):
        await state.update_data(name=message.text)
        await state.set_state(RequestFromUser.city)
        await message.answer('Введите Ваш регион:')
    else:
        await state.clear()
        await router.propagate_event(update_type='message', event=message, bot=message.bot)


@router.message(RequestFromUser.city)
async def request_from_user_city(message: Message, state: FSMContext):
    if not oth.trigger_wording(message.text):
        await state.update_data(city=message.text)
        await state.set_state(RequestFromUser.question)
        await message.answer('Введите Ваш вопрос:')
    else:
        await state.clear()
        await router.propagate_event(update_type='message', event=message, bot=message.bot)

# Ответный каталог, предложенный пользователю при выборе из главного меню
@router.message(F.text == 'Каталог услуг')
async def catalog(message: Message):
    if oth.user_has_help(message.from_user.id):
        await message.answer('Выберите категорию', reply_markup=kb.catalog_in_dialog)
    else:
        await message.answer('Выберите категорию', reply_markup=kb.catalog)


# тут должен подгружать файл с прайсом
@router.message(F.text == 'Скачать прайс')
async def price(message: Message):
    file_path = 'https://dwweb.ru/__a-data/__all_for_scripts/__rar/pro_dw_koments_1_3.rar'
    await message.answer_document(URLInputFile(file_path))


# обрабатываем выбранные категории
@router.callback_query(F.data == 'consultation')
async def consultation(callback: CallbackQuery):
    if oth.user_has_help(callback.from_user.id):
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


@router.message(F.text == 'Заказать звонок')
async def get_call(message: Message, state: FSMContext):
    await state.set_state(Register.name)
    await message.answer('Введите Ваше имя')


@router.message(Register.name)
async def register_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Register.number)
    await message.answer('Введите Ваш номер телефона', reply_markup=kb.get_number, parse_mode='MarkdownV2')


# подумать почему работает номер только из карточки, а текстом не кушает.
@router.message(Register.number)
async def register_number(message: Message, state: FSMContext):
    phone = ''
    if message.content_type == ContentType.CONTACT:
        phone = message.contact.phone_number
    elif message.content_type == ContentType.TEXT:
        phone = message.text.strip()
    if phone.startswith('+') or phone.isdigit():
        await state.update_data(number=phone)
        data = await state.get_data()
        callback_message = f'Заказан обратный звонок\n Имя: {data["name"]}\n Номер: {phone}'
        await message.answer(f'Ваше имя: {data["name"]}\nВаш номер: {phone}', reply_markup=kb.main)
        await bot_a.send_message(chat_id=os.getenv('GROUPCHATID'), text=callback_message)
        await state.clear()
    else:
        await message.answer('Пожалуйста, введите корректный номер телефона (например, +1234567890) или воспользуйтесь кнопкой "Отправить номер телефона"',reply_markup=kb.get_number )
# ответ в подкатегории


# обработка ответа "связаться с оператором"
@router.message(F.text == 'Связаться с оператором')
async def call_operator(message: Message, state: FSMContext):
    await state.set_state(RequestFromUser.name)
    await message.answer('Введите Ваше ФИО:')


@router.message(RequestFromUser.question)
async def request_from_user_question(message: Message, state: FSMContext):
    client_id = message.from_user.id
    await state.update_data(client_id=client_id)
    await state.update_data(question=message.text)
    data = await state.get_data()

    client_info = f'Информация о клиенте:\nФИО:{data["name"]}\nРегион налоговой:{data["city"]}\nТема обращения:{data["question"]}\nID клиента:{data["client_id"]}'
    groupchat_id = os.getenv('GROUPCHATID')
    await bot_a.send_message(chat_id=groupchat_id, text=client_info, reply_markup=kb.get_client)

    #print('Status Code:', response.status_code)
    #print('Response Text:', response.text)

    #Записываем id пользователя в routing, если его там еще нет
    if not oth.user_asked_for_help(client_id):
        data = {
            'code': '1',
            'customer_id': f'{client_id}',
            'fio': f'{data["name"]}',
            'tax_region': f'{data["city"]}',
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
            if not oth.user_has_help(client_id):
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
                        await bot_a.send_message(chat_id=callback_query.message.chat.id, text=f'Клиент принят пользователем: {user_full_name}')
                        await bot_a.send_message(chat_id=client_id, text=f'***ОПЕРАТОР ПРИСОЕДИНИЛСЯ К БЕСЕДЕ***', parse_mode='MarkdownV2', reply_markup=kb.main_in_dialog)
                        await bot_b.send_message(chat_id=operator_chat_id, text=f'***ВЫ ПРИСОЕДИНИЛИСЬ К БЕСЕДЕ С КЛИЕНТОМ***', parse_mode='MarkdownV2')
                    else:
                        await bot_a.send_message(chat_id=callback_query.message.chat.id, text=f'{user_full_name}, у вас нет свободных бесед, вы не можете принять еще одного клиента! Попробуйте создать группу, добавить в нее бота и использовать команду "/init"')
                else:
                    await bot_a.send_message(chat_id=callback_query.message.chat.id, text=f'{user_full_name}, у вас нет ни одной группы, вы не можете принять клиента! Попробуйте создать группу, добавить в нее бота и использовать команду "/init"')
            else:
                client_info = await bot_a.get_chat(chat_id=client_id)
                operator_info = await bot_a.get_chat(chat_id=oth.get_operator_id_by_client_id(client_id))
                await bot_a.send_message(chat_id=callback_query.message.chat.id, text=f'Клиент {client_info.full_name} уже занят пользователем: {operator_info.full_name}')
        else:
            await bot_a.send_message(chat_id=callback_query.message.chat.id, text=f'Клиент уже не нуждается в помощи')
    else:
        await bot_a.send_message(chat_id=callback_query.message.chat.id, text=f'Заявка не содержит идентификатор клиента')


@router.message(F.text == 'Вернуться в главное меню')
async def get_back_to_main(message: Message):
    await message.answer('Вы вернулись в главное меню. Выберите категорию или свяжитесь с оператором', reply_markup=kb.main)


#Удаляем строку {client_id;operator_id} из файла routing
@router.message(F.text == 'ЗАКОНЧИТЬ ДАННЫЙ ДИАЛОГ')
async def disconnection(message: Message):
    if oth.user_has_help(message.chat.id):
        file = open('../routing.env', 'r', encoding='utf-8')
        matrix = oth.uncapsule_matrix(file)
        file.close()

        i = oth.connection_exists_for_user(message.chat.id)
        client_id = matrix[i][0]
        operator_id = matrix[i][2]

        log = oth.get_log_by_id(client_id, operator_id)
        data = {
            'code': '4',
            'ID': f'{matrix[i][1]}',
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

        await bot_a.send_message(chat_id=client_id, text='***ВЫ ПОКИНУЛИ БЕСЕДУ***', reply_markup=kb.main, parse_mode='MarkdownV2')
        await bot_b.send_message(chat_id=operator_id, text='***КЛИЕНТ ПОКИНУЛ БЕСЕДУ***', parse_mode='MarkdownV2')
    else:
        await message.answer('В данной группе нет оператора\\!', reply_markup=kb.main, parse_mode='MarkdownV2')
#1142441775;10;-1002172137144

#Пересылка сообщений, если соединение установлено (через файл routing)
@router.message()
async def sending_message(message: Message):
    file = open('../routing.env', 'r', encoding='utf-8')
    matrix_client = oth.uncapsule_matrix(file)
    file.close()
    i = oth.user_index(message.chat.id)

    if i != -1:
        if message.forward_date:
            from_sender = await oth.check_sender(bot_a, message)
            mes_text = oth.if_empty_text(message)
            sending_text = f'***От {from_sender}:***\n{mes_text}'
            await oth.resending_message_of_type(bot_a, bot_b, message, matrix_client[i][2], sending_text)
            await oth.incapsulate_message(message)
        elif message.reply_to_message:
            mes_text = oth.if_empty_text(message)
            rep_mes_text = oth.if_empty_text(message.reply_to_message)
            sending_text1 = f'***Пересланное сообщение:***\n{rep_mes_text}'
            sending_text2 = f'***Ответ на пересланное сообщение:***\n{mes_text}'
            await oth.resending_message_of_type(bot_a, bot_b, message.reply_to_message, matrix_client[i][2], sending_text1)
            await oth.resending_message_of_type(bot_a, bot_b, message, matrix_client[i][2], sending_text2)
            await oth.incapsulate_message(message)
        else:
            mes_text = oth.if_empty_text(message)
            await oth.resending_message_of_type(bot_a, bot_b, message, matrix_client[i][2], mes_text)
            if oth.file_of_certain_type(message):
                await oth.saving_file_on_server(bot_a, message, url, serv_log, serv_pas)
            await oth.incapsulate_message(message)
    else:
        await message.answer('В вашем чате нет операторов')
