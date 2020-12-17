from random import sample
from random import shuffle
from telebot import *

import csv
import argparse


class MainMenu:
    def start(self):
        pass


class Information:
    def get_information(self):
        pass


class Newsletter:
    def check_subscription(self):
        pass

    def change_subscription(self):
        pass


class Menu:
    def get_menu(self):
        pass


class Booking:
    def show_map(self):
        pass

    def show_dates(self):
        pass

    def show_times(self):
        pass

    def show_free_tables(self):
        pass

    def do_reservation(self):
        pass


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

        questions = []
        with open('static/quiz.csv') as csv_file:
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
        return questions

    def check_result(self):
        pass