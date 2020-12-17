import pymysql
from pymysql.cursors import DictCursor
import telebot
from telebot import *

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

    def start(self, chat_id):
        with self.connection.cursor() as cursor:
            user = f"SELECT chat_id FROM chat WHERE chat_id = {chat_id}"
            cursor.execute(user)
            if not ([row for row in cursor]):
                add_user = f"INSERT INTO chat (chat_id) VALUE ({chat_id})"
                cursor.execute(add_user)
                self.connection.commit()
            self.bot.send_message(chat_id, 'Добро пожаловать!\n', reply_markup=self.markup)


class Information(TelegramBot):
    def get_information(self, chat_id):
        self.bot.send_message(chat_id, 'Время работы:\nПн-Пт: 08:00 - 01:00\nСб-Вс: 09:00 - 02:00\n'
                                          'Адрес: ул. Политехническая, 29\n'
                                          'Телефон: 8-800-555-35-35\n'
                                          'Сайт: www.loveyousomatcha.ru')
        self.bot.send_location(chat_id, latitude=60.00729003, longitude=30.37286282)


class Newsletter:
    def check_subscription(self):
        pass

    def change_subscription(self):
        pass


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
            else:
                add_booking = f"INSERT INTO reserve (reserve.table, reserve.date) VALUES ({int(message.text)}, %s)"
                cursor.execute(add_booking, str(date_time))
                self.connection.commit()
                self.bot.send_message(chat_id, 'Бронь успешно завершена.\n', reply_markup=markup)


class Game:
    '''
    проверка, может ли пользователь в текущее время начать игру
    (мб еще не прошел месяц с последней попытки)
    '''
    def check_user(self):
        pass

    def start_game(self):
        pass

    def get_questions(self):
        pass

    def check_result(self):
        pass
