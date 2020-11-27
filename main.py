import config
import telebot
from telebot import *

bot = telebot.TeleBot(config.token)

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


if __name__ == '__main__':
     bot.polling(none_stop=True)
