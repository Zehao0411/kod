import random
from otree.api import *

c = cu

doc = 'Author: Zehao Zhang'


class C(BaseConstants):
    NAME_IN_URL = 'math_puzzles'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    task1 = models.IntegerField(
        label='你认为下一个整数是？',
        min=0,
        max=999,
    )

    task2 = models.IntegerField(
        label='你认为下一个整数是？',
        min=0,
        max=999,
    )

    task3 = models.IntegerField(
        label='你认为下一个整数是？',
        min=0,
        max=999,
    )


