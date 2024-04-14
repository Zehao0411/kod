import random
from ._builtin import Page, WaitPage
from .models import C
from settings import my_groups_draws


def get_private_value(group_draw, indi_adjustments):
    pv = group_draw + random.choice(indi_adjustments)
    return pv


def get_winner(all_bids, tbr):
    max_value = all_bids[0] if all_bids else None
    max_indices = []

    for index, value in enumerate(all_bids):
        if value > max_value:
            max_value = value
            max_indices = [index]  # reset max_indices
        elif value == max_value:
            max_indices.append(index)
        else:
            pass

    tie = len(max_indices) > 1
    if tie and tbr == 'efficient':
        winner = random.choice(max_indices) + 1
    elif tie and tbr == 'inefficient':
        winner = -1
    else:
        winner = max_indices[0] + 1
    return winner


def get_highest_bid(all_bids):
    bids = all_bids.copy()
    highest_bid = max(bids)
    return highest_bid


def get_second_highest_bid(all_bids):
    bids = all_bids.copy()
    highest_bid_idx = bids.index(max(bids))
    bids.pop(highest_bid_idx)
    second_highest_bid = max(bids)
    return second_highest_bid


def get_my_payoff(my_id, winner, my_pv, second_price):
    if my_id == winner:
        my_payoff = my_pv - second_price
    else:
        my_payoff = 0
    return my_payoff


class Start(Page):

    def vars_for_template(self):
        which_round = self.group.round_number
        return dict(
            which_round=which_round,
        )

    def before_next_page(self, **kwargs):
        group_draw = my_groups_draws[self.group.round_number - 1]
        self.player.group_draw_this_round = group_draw
        self.player.pv = get_private_value(group_draw, C.indi_adjustments)


class Bid(Page):
    form_model = 'player'
    form_fields = ['bid']

    def vars_for_template(self):

        return dict(
            which_round=self.group.round_number,
            pv=self.player.pv,
        )

    def before_next_page(self, **kwargs):
        self.player.participant.vars['payoff_sp'] = 0


class WaitAfterBid(WaitPage):
    def after_all_players_arrive(self):
        all_pv = self.group.get_all_pvs()
        all_bids = self.group.get_all_bids()
        second_price_tbr = self.session.config['second_price_tbr']

        winner = get_winner(all_bids, second_price_tbr)
        highest_bid = get_highest_bid(all_bids)
        second_highest_bid = get_second_highest_bid(all_bids)

        for current_player in self.group.get_players():
            current_player.highest_bid_this_round = highest_bid
            current_id = current_player.id_in_group

            payoff_this_round = get_my_payoff(current_id, winner, all_pv[current_id-1], second_highest_bid)
            current_player.payoff_this_round = payoff_this_round
            current_player.participant.vars['payoff_sp'] += payoff_this_round
        self.group.winner = winner


class Feedback(Page):
    def vars_for_template(self):
        return dict(
            pv=self.player.pv,
            bid=self.player.bid,
            winner=self.group.winner,
            highest_bid_this_round=self.player.highest_bid_this_round,
            payoff_this_round=self.player.payoff_this_round,
            which_round=self.group.round_number,
        )

    def before_next_page(self, **kwargs):
        pass


page_sequence = [Start, Bid, WaitAfterBid, Feedback]
