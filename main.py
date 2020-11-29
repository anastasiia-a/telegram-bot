import datetime
from telebot import *

import config


bot = TeleBot(config.token)

markup = types.ReplyKeyboardMarkup(row_width=2)
info_btn = types.KeyboardButton('Информация')
mail_btn = types.KeyboardButton('Рассылка')
menu_btn = types.KeyboardButton('Меню')
book_btn = types.KeyboardButton('Бронирование')
game_btn = types.KeyboardButton('Игра')
markup.add(info_btn, mail_btn, menu_btn, book_btn, game_btn)


@bot.message_handler(commands=['start'])
def handle_start_help(message):
    bot.send_message(message.chat.id, 'Добро пожаловать!', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def mess(message):
    if message.text == 'Информация':
        bot.send_message(message.chat.id, 'Время работы:\nПн-Пт: 08:00 - 22:00\nСб-Вс: 09:00 - 22:00\n'
                                          'Адрес: ул. Политехническая, 29\n'
                                          'Телефон: 8-800-555-35-35\n'
                                          'Сайт: www.matchacafe.ru')
        bot.send_location(message.chat.id, latitude=60.00729003, longitude=30.37286282)

    if message.text == "Бронирование":
        img = open('static/plancafe.png', 'rb')

        bot.send_message(message.chat.id, 'Карта нашего заведения\n')
        bot.send_photo(message.chat.id, img)
        markup2 = types.ReplyKeyboardMarkup(row_width=1)
        today = types.KeyboardButton('Сегодня')
        tom = types.KeyboardButton('Завтра')
        day_after_tom = types.KeyboardButton('Послезавтра')
        main_menu = types.KeyboardButton('Главное меню')
        markup2.add(today, tom, day_after_tom, main_menu)
        bot.send_message(message.chat.id, 'Выберите день\n', reply_markup=markup2)

    if message.text == 'Главное меню':
        bot.send_message(message.chat.id, 'Выберите новое действие\n', reply_markup=markup)

    if message.text in ['Сегодня', 'Завтра', 'Послезавтра']:
        markup3 = types.ReplyKeyboardMarkup(row_width=2)
        time_18 = types.KeyboardButton('18:00')
        time_19 = types.KeyboardButton('19:00')
        time_20 = types.KeyboardButton('20:00')
        time_21 = types.KeyboardButton('21:00')
        time_22 = types.KeyboardButton('22:00')
        time_23 = types.KeyboardButton('23:00')
        main_menu = types.KeyboardButton('Главное меню')
        markup3.add(time_18, time_19, time_20, time_21, time_22, time_23, main_menu)
        bot.send_message(message.chat.id, 'Выберите время\n', reply_markup=markup3)


if __name__ == '__main__':
     bot.polling(none_stop=True)
