import pymysql
from pymysql.cursors import DictCursor
import telebot
from telebot import *

from random import choice
from string import ascii_uppercase
from random import shuffle

import csv

import config
import datetime


class TelegramBot:
    def __init__(self):
        self.connection = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            db='bot',
            charset='utf8mb4',
            cursorclass=DictCursor
        )

        self.bot = telebot.TeleBot(config.token)
        self.d_today = datetime.date.today()
        self.d_tomorrow = self.d_today + datetime.timedelta(days=1)
        self.d_day_after_tom = self.d_today + datetime.timedelta(days=2)


class MainMenu(TelegramBot):
    def __init__(self):
        self.markup = types.ReplyKeyboardMarkup(row_width=2)
        info_btn = types.KeyboardButton('Информация')
        mail_btn = types.KeyboardButton('Рассылка')
        menu_btn = types.KeyboardButton('Меню')
        book_btn = types.KeyboardButton('Бронирование')
        game_btn = types.KeyboardButton('Игра')
        self.markup.add(info_btn, mail_btn, menu_btn, book_btn, game_btn)

    def start(self, chat_id, bot, connection):
        with connection.cursor() as cursor:
            user = f"SELECT chat_id FROM chat WHERE chat_id = {chat_id}"
            cursor.execute(user)
            if not ([row for row in cursor]):
                add_user = f"INSERT INTO chat (chat_id) VALUE ({chat_id})"
                cursor.execute(add_user)
                connection.commit()
            bot.send_message(chat_id, 'Добро пожаловать!\n', reply_markup=self.markup)


class Information(TelegramBot):
    def get_information(self, chat_id):
        self.bot.send_message(chat_id, 'Время работы:\nПн-Пт: 08:00 - 01:00\nСб-Вс: 09:00 - 02:00\n'
                                        'Адрес: ул. Политехническая, 29\n'
                                        'Телефон: 8-800-555-35-35\n'
                                        'Сайт: www.loveyousomatcha.ru')
        self.bot.send_location(chat_id, latitude=60.00729003, longitude=30.37286282)


class Newsletter(TelegramBot):
    def check_subscription(self, chat_id):
        with self.connection.cursor() as cursor:
            query = f"SELECT subscribe FROM chat WHERE chat_id = {chat_id}"
            cursor.execute(query)
            subscription = cursor.fetchone()
            if subscription['subscribe'] == 'no':
                markup_newsletter = types.ReplyKeyboardMarkup(row_width=1)
                main_menu = types.KeyboardButton('Назад')
                subscription = types.KeyboardButton('Подписаться на рассылку')
                markup_newsletter.add(subscription, main_menu)
                self.bot.send_message(chat_id, 'Подписавшись на рассылку, Вы будете получать актуальные новости об '
                                               'акциях и других предложениях нашего заведения\n',
                                      reply_markup=markup_newsletter)
            else:
                markup_newsletter = types.ReplyKeyboardMarkup(row_width=1)
                main_menu = types.KeyboardButton('Назад')
                subscription = types.KeyboardButton('Отписаться от рассылки')
                markup_newsletter.add(subscription, main_menu)
                self.bot.send_message(chat_id, 'Отписавшись от рассылки, Вы перестанете получать актуальные '
                                               'новости об акциях и других предложениях нашего заведения\n',
                                      reply_markup=markup_newsletter)

    def change_subscription(self, chat_id):
        with self.connection.cursor() as cursor:
            query = f"SELECT subscribe FROM chat WHERE chat_id = {chat_id}"
            cursor.execute(query)
            subscription = cursor.fetchone()
            if subscription['subscribe'] == 'no':
                change_subs = f"UPDATE chat SET subscribe = 'yes' WHERE chat_id = {chat_id}"
                cursor.execute(change_subs)
                self.connection.commit()
                markup_newsletter = types.ReplyKeyboardMarkup(row_width=1)
                main_menu = types.KeyboardButton('Назад')
                subscription = types.KeyboardButton('Отписаться от рассылки')
                markup_newsletter.add(subscription, main_menu)
                self.bot.send_message(chat_id, 'Вы успешно подписаны на рассылку новостей и акций нашего заведения. '
                                               'Если хотите ее отменить, нажмите на кнопку "Отменить рассылку”\n',
                                      reply_markup=markup_newsletter)
            elif subscription['subscribe'] == 'yes':
                change_subs = f"UPDATE chat SET subscribe = 'no' WHERE chat_id = {chat_id}"
                cursor.execute(change_subs)
                self.connection.commit()
                markup_newsletter = types.ReplyKeyboardMarkup(row_width=1)
                main_menu = types.KeyboardButton('Назад')
                subscription = types.KeyboardButton('Подписаться на рассылку')
                markup_newsletter.add(subscription, main_menu)
                self.bot.send_message(chat_id, 'Подписка на новости и акции нашего заведения отменена. '
                                               'Если вы хотите вернуть подписку, нажмите на кнопку '
                                               '"Подписаться на рассылку"\n',
                                      reply_markup=markup_newsletter)

    def send_newsletter(self):
        pass
        with self.connection.cursor() as cursor:
            news = ['В нашем заведении действует скидка 30% на все сладкое меню\n'
                    'каждый будний день c 20:00 до закрытия!\n',

                    'Акция!\n'
                    'При заказе 2 одинаковых позиций из нашего меню\n'
                    '3 получите совершенно бесплатно!\n',

                    'Каждый понедельник дарим скидку на завтраки до 12:00 10%\n',

                    'Не забывай раз в месяц испытывать удачу в игре-викторине\n'
                    'И бороться за приятный бонус в нашем заведении))\n',
                    ]
            newsletter = choice(news)
            query = f"SELECT chat_id FROM chat WHERE subscribe = 'yes'"
            cursor.execute(query)
            users = cursor.fetchall()
            for user in users:
                try:
                    self.bot.send_message(user['chat_id'], newsletter)
                except:
                    print('Не удалось отправить сообщению пользователю :', user)


class Menu(TelegramBot):
    def get_menu(self, chat_id):
        markup_menu = types.ReplyKeyboardMarkup(row_width=1)
        main_menu = types.KeyboardButton('Назад')
        main_dishes = types.KeyboardButton('Основные блюда')
        dishes = types.KeyboardButton('Закуски')
        drinks = types.KeyboardButton('Напитки')
        markup_menu.add(main_dishes, dishes, drinks, main_menu)
        self.bot.send_message(chat_id, 'Выберите категорию\n', reply_markup=markup_menu)


class Booking(TelegramBot):
    def show_map(self, chat_id):
        img = open('static/plancafe.JPG', 'rb')
        self.bot.send_message(chat_id, 'Карта нашего заведения\n')
        self.bot.send_photo(chat_id, img)

    def show_dates(self, chat_id):
        markup_date = types.ReplyKeyboardMarkup(row_width=1)
        today = types.KeyboardButton(str(self.d_today))
        tomorrow = types.KeyboardButton(str(self.d_tomorrow))
        day_after_tomorrow = types.KeyboardButton(str(self.d_day_after_tom))
        main_menu = types.KeyboardButton('Главное меню')
        markup_date.add(today, tomorrow, day_after_tomorrow, main_menu)
        self.bot.send_message(chat_id, 'Выберите день\n', reply_markup=markup_date)

    def show_times(self, chat_id):
        markup = types.ReplyKeyboardMarkup(row_width=2)
        time_18 = types.KeyboardButton('18:00')
        time_19 = types.KeyboardButton('19:00')
        time_20 = types.KeyboardButton('20:00')
        time_21 = types.KeyboardButton('21:00')
        time_22 = types.KeyboardButton('22:00')
        time_23 = types.KeyboardButton('23:00')
        main_menu = types.KeyboardButton('Главное меню')
        markup.add(time_18, time_19, time_20, time_21, time_22, time_23, main_menu)
        self.bot.send_message(chat_id, 'Выберите время\n', reply_markup=markup)

    def show_free_tables(self, date_time, chat_id):
        tables = [n for n in range(1, 30)]
        with self.connection.cursor() as cursor:
            sql = "SELECT reserve.table FROM reserve WHERE reserve.date=%s; "
            cursor.execute(sql, str(date_time))

            not_free = []
            for row in cursor:
                not_free.append(row['table'])
        free_tables = [n for n in tables if n not in not_free]

        if free_tables:
            self.bot.send_message(chat_id, 'Выберите свободный стол\n')
            self.bot.send_message(chat_id, str(free_tables)[1:-1])
        else:
            self.bot.send_message(chat_id, 'К сожалению, мест нет\n')

        return free_tables

    def do_reservation(self, date_time, message, markup, chat_id):

        with self.connection.cursor() as cursor:
            sql = "SELECT reserve.table FROM reserve WHERE reserve.date=%s; "
            cursor.execute(sql, str(date_time))

            not_free = []
            for row in cursor:
                not_free.append(row['table'])
            if message.text in list(map(str, not_free)):
                self.bot.send_message(chat_id, 'К сожалению, ваш столик уже кто-то забронировал, выберите другой.\n')
                tables = [table for table in range(1, 30) if table not in not_free]
                self.bot.send_message(chat_id, str(tables)[1:-1])
            else:
                add_booking = f"INSERT INTO reserve (reserve.table, reserve.date) VALUES ({int(message.text)}, %s)"
                cursor.execute(add_booking, str(date_time))
                self.connection.commit()
                self.bot.send_message(chat_id, 'Бронь успешно завершена.\n', reply_markup=markup)


class Menu(TelegramBot):
    def get_menu(self, chat_id):
        markup_menu = types.ReplyKeyboardMarkup(row_width=1)
        main_menu = types.KeyboardButton('Назад')
        main_dishes = types.KeyboardButton('Основные блюда')
        dishes = types.KeyboardButton('Закуски')
        drinks = types.KeyboardButton('Напитки')
        markup_menu.add(main_dishes, dishes, drinks, main_menu)
        self.bot.send_message(chat_id, 'Выберите категорию\n', reply_markup=markup_menu)


class Booking(TelegramBot):
    def show_map(self, chat_id):
        img = open('static/plancafe.JPG', 'rb')
        self.bot.send_message(chat_id, 'Карта нашего заведения\n')
        self.bot.send_photo(chat_id, img)

    def show_dates(self, chat_id):
        markup_date = types.ReplyKeyboardMarkup(row_width=1)
        today = types.KeyboardButton(str(self.d_today))
        tomorrow = types.KeyboardButton(str(self.d_tomorrow))
        day_after_tomorrow = types.KeyboardButton(str(self.d_day_after_tom))
        main_menu = types.KeyboardButton('Главное меню')
        markup_date.add(today, tomorrow, day_after_tomorrow, main_menu)
        self.bot.send_message(chat_id, 'Выберите день\n', reply_markup=markup_date)

    def show_times(self, chat_id):
        markup = types.ReplyKeyboardMarkup(row_width=2)
        time_18 = types.KeyboardButton('18:00')
        time_19 = types.KeyboardButton('19:00')
        time_20 = types.KeyboardButton('20:00')
        time_21 = types.KeyboardButton('21:00')
        time_22 = types.KeyboardButton('22:00')
        time_23 = types.KeyboardButton('23:00')
        main_menu = types.KeyboardButton('Главное меню')
        markup.add(time_18, time_19, time_20, time_21, time_22, time_23, main_menu)
        self.bot.send_message(chat_id, 'Выберите время\n', reply_markup=markup)

    def show_free_tables(self, date_time, chat_id):
        tables = [n for n in range(1, 30)]
        with self.connection.cursor() as cursor:
            sql = "SELECT reserve.table FROM reserve WHERE reserve.date=%s; "
            cursor.execute(sql, str(date_time))

            not_free = []
            for row in cursor:
                not_free.append(row['table'])
        free_tables = [n for n in tables if n not in not_free]

        if free_tables:
            self.bot.send_message(chat_id, 'Выберите свободный стол\n')
            self.bot.send_message(chat_id, str(free_tables)[1:-1])
        else:
            self.bot.send_message(chat_id, 'К сожалению, мест нет\n')

        return free_tables

    def do_reservation(self, date_time, message, markup, chat_id):

        with self.connection.cursor() as cursor:
            sql = "SELECT reserve.table FROM reserve WHERE reserve.date=%s; "
            cursor.execute(sql, str(date_time))

            not_free = []
            for row in cursor:
                not_free.append(row['table'])
            if message.text in list(map(str, not_free)):
                self.bot.send_message(chat_id, 'К сожалению, ваш столик уже кто-то забронировал, выберите другой.\n')
                tables = [table for table in range(1, 30) if table not in not_free]
                self.bot.send_message(chat_id, str(tables)[1:-1])
            else:
                add_booking = f"INSERT INTO reserve (reserve.table, reserve.date) VALUES ({int(message.text)}, %s)"
                cursor.execute(add_booking, str(date_time))
                self.connection.commit()
                self.bot.send_message(chat_id, 'Бронь успешно завершена.\n', reply_markup=markup)


class Game(TelegramBot):
    def check_user(self, chat_id):
        markup_game = types.ReplyKeyboardMarkup(row_width=1)
        main_menu = types.KeyboardButton('Назад')
        subscription = types.KeyboardButton('Начать')
        markup_game.add(subscription, main_menu)
        self.bot.send_message(chat_id, 'Привет! Хочешь получить скидку в нашем заведении или бесплатный напиток из меню? У тебя есть все шансы! '
                              'Ответь правильно, как минимум, на 8 вопросов из 10 и получи уникальный промокод, с которым ты сможешь сразу же '
                              'прийти к нам и забрать свой выигрыш или же покушать/выпить с приятной скидкой. Для того, чтобы проверить свои '
                              'знания нажми кнопку “начать”\n\n',
                              reply_markup=markup_game)

    def start_game(self, message, correctAnsw,  question, qNum):

        numbering = "1234"
        score = 0
        correct = 0
        i = 0

        for answer in question["answers"]:
            if answer == correctAnsw:
                correct = i
            i += 1
        while True:
            answer = message.text
            if (len(answer) == 1) and answer in numbering[0:i]:
                break
            if (answer == 'пропустить'):
                break
        if answer == numbering[correct]:
            score = 1
        return score

    def get_questions(self):
        questions = []
        with open('static/quiz.csv', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                else:
                    ans = []
                    num = 0
                    for item in row:
                        if num > 0:
                            ans.append(item)
                        num += 1

                    q = {'question': row[0], 'answers': ans}
                    questions.append(q)
                    line_count += 1

        shuffle(questions)
        return questions[0:10]

    def check_result(self, chat_id, score):
        prizes = ['Coca-cola 0.5л',
                  'Скидку 10%',
                  'Скидку 5%',
                  'Латте 0.3л',
                  'Чизкейк 300гр',
                  'Сырные палочки 3шт']
        if score < 8:
            self.bot.send_message(chat_id, 'К сожалению, твой результат ' + f'{score}' + ' из 10. '
                                           'Попробуй еще раз, но уже в следующем месяце')
        else:
            self.bot.send_message(chat_id, 'Ты выиграл ' + choice(prizes) + '. Промокод: ' +
                                  ''.join(choice(ascii_uppercase) for i in range(12)) + '. Покажи это сообщение своему официанту.')
