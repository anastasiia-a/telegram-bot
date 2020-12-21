import datetime

import pymysql
import schedule
import time

from pymysql.cursors import DictCursor
from classes import TelegramBot, Menu, MainMenu, Game, Booking, Information, Newsletter
from random import shuffle
from telebot import *
from multiprocessing.context import Process


telegram_bot = TelegramBot()
menu_bot = Menu()
main_menu_bot = MainMenu()
booking_bot = Booking()
information_bot = Information()
newsletter = Newsletter()

game_bot = Game()
qNum = 0
correct_answer = ''
question = ''
score = 0
isGame = False
isBooking = False


bot = telegram_bot.bot
booking_date, date_time, free_tables, questions = (0, 0, [], 0)


@bot.message_handler(commands=['start'])
def handle_start_help(message):
    main_menu_bot.start(message.chat.id, bot, telegram_bot.connection)


@bot.message_handler(content_types=['text'])
def mess(message):
    global booking_date
    global free_tables
    global date_time
    global questions
    global qNum
    global score
    global correct_answer
    global question
    global isGame
    global isBooking


    if message.text == 'Информация':
        isGame, isBooking = False, False
        information_bot.get_information(message.chat.id)

    elif message.text == 'Начать':
        if not isGame:
           connection = pymysql.connect(
                host='localhost',
                user='root',
                password='',
                db='bot',
                charset='utf8mb4',
                cursorclass=DictCursor
           )
           with connection.cursor() as cursor:
               query = f"SELECT * FROM game WHERE chat_id = {message.chat.id};"
               cursor.execute(query)
               result = cursor.fetchone()
               connection.commit()
               if not result:
                   isGame = True
                   qNum = 0
                   score = 0
                   questions = game_bot.get_questions()
                   now = datetime.datetime.now()
                   with connection.cursor() as cursor:
                       add_user = f"INSERT INTO game (game.chat_id, game.last_game) VALUES ({int(message.chat.id)}, %s);"
                       connection.begin
                       cursor.execute(add_user, str(now))
                       connection.commit()
                       connection.close()

                   correct_answer, question = do_question(questions[qNum])
                   print_question(message.chat.id, question)

               else:
                   markup_game = types.ReplyKeyboardMarkup(row_width=1)
                   main_menu = types.KeyboardButton('Назад')
                   markup_game.add(main_menu)
                   bot.send_message(message.chat.id,
                                         'Ты пока не можешь сыграть еще раз, попробуй поиграть еще раз в'
                                         ' следующем календарном месяце\n\n',
                                         reply_markup=markup_game)


        else:
            bot.send_message(message.chat.id, 'Вы уже начали игру\n',
                             reply_markup=game_bot.markup)

    elif message.text in ['1', '2', '3', '4', 'пропустить']:
        if isGame:
            qNum = qNum + 1
            if qNum < 10:
                score = score + game_bot.start_game(message, correct_answer, question, qNum)
                correct_answer, question = do_question(questions[qNum])
                print_question(message.chat.id, question)
            else:
                game_bot.check_result(message.chat.id, score)
                questions.clear()
                isGame = False
        else:
             newsletter.check_subscription(message.chat.id)

    elif message.text == 'Рассылка':
       isGame, isBooking = False, False
       newsletter.check_subscription(message.chat.id)

    elif message.text == 'Подписаться на рассылку':
       newsletter.change_subscription(message.chat.id)

    elif message.text == 'Отписаться от рассылки':
        newsletter.change_subscription(message.chat.id)

    elif message.text == 'Меню':
        isGame, isBooking = False, False
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
        isGame, isBooking = False, False
        booking_bot.show_map(message.chat.id)
        booking_bot.show_dates(message.chat.id)

    elif message.text in ['Назад', 'Главное меню']:
        isGame, isBooking = False, False
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
        isBooking = True

    elif message.text in list(map(str, free_tables)):
        booking_bot.do_reservation(date_time, message,
                                   main_menu_bot.markup, message.chat.id)

    elif message.text == 'Игра':
        isBooking = False
        isGame = False
        game_bot.check_user(message.chat.id)

    elif isGame:
        bot.send_message(message.chat.id,
                          "Упс! Ты ввел(а) некорректный ответ. "
                          "Попробуй еще раз либо отправь “пропустить” и "
                          "перейдешь к следующему вопросу”")
    elif isBooking:
        bot.send_message(message.chat.id,
                         'Вы ввели некорректный номер либо этот '
                         'столик уже занят, выберите другой.\n')

    else:
        bot.send_message(message.chat.id, 'Нажмите кнопку!\n')

def do_question(some_question):
    cor_answer = some_question["answers"][0]
    shuffle(some_question["answers"])
    return cor_answer, some_question

def print_question(chat_id, some_question):
    bot.send_message(chat_id, f'\n{some_question["question"]}\n')
    numbering = "12345"
    i = 0
    for answer in some_question["answers"]:
        bot.send_message(chat_id, numbering[i] + ". " + answer, "\n")
        i += 1
        pass

# для проверки работы рассылки сообщения отправляются каждую минуту
#schedule.every().minute.at(":17").do(newsletter.send_newsletter)

# можно, к примеру, отправлять рассылку каждый понедельник в 12:00
schedule.every().monday.at("12:00").do(newsletter.send_newsletter)


class ScheduleMessage:
    @staticmethod
    def try_send_schedule():
        while True:
            schedule.run_pending()
            time.sleep(1)

    @staticmethod
    def start_process():
        p1 = Process(target=ScheduleMessage.try_send_schedule, args=())
        p1.start()


schedule_message = ScheduleMessage()


if __name__ == '__main__':
    ScheduleMessage.start_process()
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
        time.sleep(15)
