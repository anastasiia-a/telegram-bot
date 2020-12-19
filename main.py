import datetime

from classes import TelegramBot, Menu, MainMenu, Game, Booking, Information, Newsletter


telegram_bot = TelegramBot()
menu_bot = Menu()
main_menu_bot = MainMenu()
booking_bot = Booking()
information_bot = Information()
newsletter = Newsletter()
game_bot = Game()

bot = telegram_bot.bot
booking_date, date_time, free_tables = (0, 0, [])


@bot.message_handler(commands=['start'])
def handle_start_help(message):
    main_menu_bot.start(message.chat.id, bot, telegram_bot.connection)


@bot.message_handler(content_types=['text'])
def mess(message):
    global booking_date
    global free_tables
    global date_time

    if message.text == 'Информация':
        information_bot.get_information(message.chat.id)

    elif message.text == 'Рассылка':
        newsletter.check_subscription(message.chat.id)

    elif message.text == 'Подписаться на рассылку':
        newsletter.change_subscription(message.chat.id)

    elif message.text == 'Начать':
        game_bot.start_game(message)

    elif message.text == 'Отписаться от рассылки':
        newsletter.change_subscription(message.chat.id)

    elif message.text == 'Меню':
        menu_bot.get_menu(message.chat.id)

    elif message.text == 'Основные блюда':
        with open('static/menu_1.pdf', 'rb') as file:
            bot.send_document(message.chat.id, file)

    elif message.text == 'Закуски':
        with open('static/menu_2.pdf', 'rb') as file:
            bot.send_document(message.chat.id, file)

    elif message.text == 'Напитки':
        with open('static/menu_3.pdf', 'rb') as file:
            bot.send_document(message.chat.id, file)

    elif message.text == "Бронирование":
        booking_bot.show_map(message.chat.id)
        booking_bot.show_dates(message.chat.id)

    elif message.text in ['Назад', 'Главное меню']:
        bot.send_message(message.chat.id, 'Выберите новое действие\n',
                         reply_markup=main_menu_bot.markup)

    elif message.text in [str(telegram_bot.d_today),
                        str(telegram_bot.d_tomorrow),
                        str(telegram_bot.d_day_after_tom)]:

        booking_date = message.text
        booking_bot.show_times(message.chat.id)

    elif message.text in ['18:00', '19:00', '20:00', '21:00', '22:00', '23:00']:
        date_time = datetime.datetime(int(booking_date[:4]),
                                      int(booking_date[5:7]),
                                      int(booking_date[8:]),
                                      int(message.text[:2]))

        free_tables = booking_bot.show_free_tables(date_time, message.chat.id)

    elif message.text in list(map(str, free_tables)):
        booking_bot.do_reservation(date_time, message,
                                   main_menu_bot.markup, message.chat.id)

    elif message.text == 'Игра':
        bot.send_message(message.chat.id,
                              'Привет! Хочешь получить скидку в нашем заведении или бесплатный напиток из меню? У тебя есть все шансы! '
                              'Ответь правильно, как минимум, на 8 вопросов из 10 и получи уникальный промокод, с которым ты сможешь сразу же '
                              'прийти к нам и забрать свой выигрыш или же покушать/выпить с приятной скидкой. Для того, чтобы проверить свои '
                              'знания нажми кнопку “начать”\n\n')
        game_bot.start_game(message)

    else:
        try:
            int(message.text)
            bot.send_message(message.chat.id,
                             'Вы ввели некорректный номер либо этот '
                             'столик уже занят, выберите другой.\n')
        except ValueError:
            bot.send_message(message.chat.id, 'Нажмите кнопку!\n')


if __name__ == '__main__':
    bot.polling(none_stop=True)