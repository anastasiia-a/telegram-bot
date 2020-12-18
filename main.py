import datetime
import schedule
import time
from multiprocessing.context import Process

from classes import TelegramBot, Menu, MainMenu, Game, Booking, Information, Newsletter


telegram_bot = TelegramBot()
menu_bot = Menu()
main_menu_bot = MainMenu()
booking_bot = Booking()
information_bot = Information()
newsletter = Newsletter()

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
        pass

    else:
        try:
            int(message.text)
            bot.send_message(message.chat.id,
                             'Вы ввели некорректный номер либо этот '
                             'столик уже занят, выберите другой.\n')
        except ValueError:
            bot.send_message(message.chat.id, 'Нажмите кнопку!\n')


'''отправка рассылки через schedule /не работает/'''
# schedule.every().minute.at(":17").do(newsletter.send_newsletter)
#
#
# class ScheduleMessage:
#     @staticmethod
#     def try_send_schedule():
#         while True:
#             schedule.run_pending()
#             time.sleep(1)
#
#     @staticmethod
#     def start_process():
#         p1 = Process(target=ScheduleMessage.try_send_schedule(), args=())
#         p1.start()
#
#
# schedule_message = ScheduleMessage()

'''отправка рассылки через сравнение даты в функции /тоже не работает :(((/'''
# p1 = Process(target=newsletter.send_newsletter, args=())
# p1.start()


if __name__ == '__main__':
    bot.polling(none_stop=True)
    # while True:
    #     try:
    #         bot.polling(none_stop=True)
    #     except Exception as e:
    #         print(e)
    #         # повторяем через 15 секунд в случае недоступности сервера Telegram
    #         time.sleep(15)

