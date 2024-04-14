from otree.api import *
from settings import my_show_up_fee, my_num_of_rounds, my_players_per_group, my_groups_draws, my_indi_adjustments

c = cu

doc = 'Author: ZZH'


class C(BaseConstants):
    NAME_IN_URL = 'start_all'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


class Instructions(Page):
    def vars_for_template(player):
        show_up_fee = my_show_up_fee

        return dict(
            show_up_fee=show_up_fee,
        )


page_sequence = [Instructions]
