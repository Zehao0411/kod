import random
from otree.api import *

c = cu

doc = 'Author: Zehao Zhang'


class C(BaseConstants):
    NAME_IN_URL = 'reward_sp'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass



