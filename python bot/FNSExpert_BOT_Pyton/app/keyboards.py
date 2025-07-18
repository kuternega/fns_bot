# будем создавать менюшки

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,InlineKeyboardMarkup, InlineKeyboardButton

# это меню-предложение под блоком "написать сообщение", на которое кликает пользователь, отправляя запрос
'''main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Каталог услуг')],
                                   [KeyboardButton(text='Скачать прайс')],
                                   [KeyboardButton(text='Контакты'),
                                   KeyboardButton(text='Заказать звонок')]],
                                     resize_keyboard=True,
                                    input_field_placeholder='Выберите пункт меню...'
                                   )'''
main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Юридические услуги')],
                                   [KeyboardButton(text='Бухгалтерские услуги')],
                                   [KeyboardButton(text='Скачать прайс')],
                                   [KeyboardButton(text='Связь с оператором')]],
                                    resize_keyboard=True,
                                    input_field_placeholder='Выберите пункт меню...'
                                   )
catalog = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Заказать звонок', callback_data='make_call')],
                                              [InlineKeyboardButton(text='Соединить с оператором', callback_data='call_operator')]])
start = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='/start')]],
                                     resize_keyboard=True)

'''# это меню-ответ пользователю на его запрос
catalog=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Консультация', callback_data='consultation')],
                                              [InlineKeyboardButton(text='Налоговые проверки', callback_data='audits')],
                                              [InlineKeyboardButton(text='Требования', callback_data='requirement')],
                                              [InlineKeyboardButton(text='Допрос, дача пояснений, комиссии', callback_data='interrogation')],
                                              [InlineKeyboardButton(text='Представление интересов в суде', callback_data='lawyer')],
                                              [InlineKeyboardButton(text='Декларации', callback_data='declaration')],
                                              ])'''

# кнопка для прикрепления номера тлф в форме обратной связи
get_number = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Отправить номер телефона', request_contact=True)]], resize_keyboard=True)

# кнопка для отправки прайса и предложение связаться с оператором
sub_catalog_button = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Связаться с оператором')],
                                            [KeyboardButton(text='Вернуться в главное меню')]],
                                                resize_keyboard=True)

# кнопка для сообщения-запроса в чате операторов
get_client = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Принять клиента", callback_data="get_client")]])

# это меню-ответ пользователю на его запрос
catalog_in_dialog = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Налоговые проверки', callback_data='audits')],
                                                          [InlineKeyboardButton(text='Требования', callback_data='requirement')],
                                                          [InlineKeyboardButton(text='Допрос, дача пояснений, комиссии', callback_data='interrogation')],
                                                          [InlineKeyboardButton(text='Представление интересов в суде', callback_data='lawyer')],
                                                          [InlineKeyboardButton(text='Декларации', callback_data='declaration')],
                                                          ])

main_in_dialog = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Каталог услуг')],
                                               [KeyboardButton(text='Скачать прайс')],
                                               [KeyboardButton(text='Контакты'),
                                               KeyboardButton(text='Заказать звонок')],
                                               [KeyboardButton(text='ЗАКОНЧИТЬ ДАННЫЙ ДИАЛОГ')]],
                                                resize_keyboard=True,
                                                input_field_placeholder='Выберите пункт меню...'
                                               )

operator_in_dialog = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='ЗАКОНЧИТЬ ДАННЫЙ ДИАЛОГ')]],
                                                resize_keyboard=True,
                                                input_field_placeholder='Вы можете закончить диалог')

