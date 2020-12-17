import datetime

from classes import TelegramBot, Menu, MainMenu, Game, Booking, Information


telegram_bot = TelegramBot()
menu_bot = Menu()
main_menu_bot = MainMenu()
booking_bot = Booking()
information_bot = Information()

bot = telegram_bot.bot
booking_date, date_time, free_tables = (0, 0, [])


@bot.message_handler(commands=['start'])
def handle_start_help(message):
    main_menu_bot.start(message.chat.id)


@bot.message_handler(content_types=['text'])
def mess(message):
    global booking_date
    global free_tables
    global date_time
    '''
    Информация
    '''
    if message.text == 'Информация':
        information_bot.get_information(message.chat.id)

    '''
    Рассылка
    '''
    if message.text == 'Рассылка':
        pass

    '''
    Меню
    '''
    if message.text == 'Меню':
        menu_bot.get_menu(message.chat.id)

    if message.text == 'Основные блюда':
        with open('static/menu_1.pdf', 'rb') as file:
            bot.send_document(message.chat.id, file)

    if message.text == 'Закуски':
        with open('static/menu_2.pdf', 'rb') as file:
            bot.send_document(message.chat.id, file)

    if message.text == 'Напитки':
        with open('static/menu_3.pdf', 'rb') as file:
            bot.send_document(message.chat.id, file)

    '''
    Бронирование
    '''
    if message.text == "Бронирование":
        booking_bot.show_map(message.chat.id)
        booking_bot.show_dates(message.chat.id)

    if message.text in ['Назад', 'Главное меню']:
        bot.send_message(message.chat.id, 'Выберите новое действие\n',
                         reply_markup=main_menu_bot.markup)

    if message.text in [str(telegram_bot.d_today),
                        str(telegram_bot.d_tomorrow),
                        str(telegram_bot.d_day_after_tom)]:

        booking_date = message.text
        booking_bot.show_times(message.chat.id)

    if message.text in ['18:00', '19:00', '20:00', '21:00', '22:00', '23:00']:
        time = message.text
        year = int(booking_date[:4])
        mounth = int(booking_date[5:7])
        day = int(booking_date[8:])
        date_time = datetime.datetime(year, mounth, day, int(time[:2]))

        free_tables = booking_bot.show_free_tables(date_time, message.chat.id)

    if message.text in list(map(str, free_tables)):
        booking_bot.do_reservation(date_time, message,
                                   main_menu_bot.markup, message.chat.id)

    '''
    Игра
    '''
    if message.text == 'Игра':
        pass


if __name__ == '__main__':
    bot.polling(none_stop=True)
