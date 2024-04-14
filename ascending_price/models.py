import random
from otree.api import *
from settings import my_groups_draws, my_players_per_group, my_indi_adjustments, my_num_of_rounds

c = cu

doc = 'Ascending price auction. Author: Zehao Zhang'


def get_group_draw(group_draws):
    group_draw = random.choice(group_draws)
    return group_draw


class C(BaseConstants):
    NAME_IN_URL = 'ascending_price'

    PLAYERS_PER_GROUP = my_players_per_group
    NUM_ROUNDS = my_num_of_rounds

    group_draws = my_groups_draws
    indi_adjustments = my_indi_adjustments


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    # group_draw = models.IntegerField(initial=get_group_draw(C.group_draws))
    start_price = models.IntegerField(initial=-99)
    players_left_num = models.IntegerField(initial=C.PLAYERS_PER_GROUP)
    winner = models.IntegerField(initial=-99)

    highest_bid_this_round = models.IntegerField()
    second_highest_bid_this_round = models.IntegerField()

    def get_all_pvs(self):
        all_pvs = [None, None, None, None]
        for player_id in range(C.PLAYERS_PER_GROUP):
            current_player = self.get_player_by_id(player_id + 1)
            current_pv = current_player.pv
            all_pvs[player_id] = current_pv
        return all_pvs

    def get_all_bids(self):
        all_bids = [None, None, None, None]
        for player_id in range(C.PLAYERS_PER_GROUP):
            current_player = self.get_player_by_id(player_id + 1)
            current_bid = current_player.bid
            all_bids[player_id] = current_bid
        return all_bids


class Player(BasePlayer):
    pv = models.IntegerField()
    bid = models.IntegerField()

    payoff_this_round = models.IntegerField()
    is_winner = models.BooleanField(initial=False)
    group_draw_this_round = models.IntegerField()
