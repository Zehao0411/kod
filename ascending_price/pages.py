import random
from ._builtin import Page, WaitPage
from .models import C
from settings import my_groups_draws, my_payoff_unit, my_timeout_seconds


def get_group_draw(group_draws):
    group_draw = random.choice(group_draws)
    return group_draw


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
    timeout_seconds = my_timeout_seconds

    def vars_for_template(self):
        which_round = self.group.round_number
        return dict(
            which_round=which_round,
        )

    def before_next_page(self, **kwargs):
        group_draw = my_groups_draws[self.group.round_number - 1]
        self.player.group_draw_this_round = group_draw
        self.player.pv = get_private_value(group_draw, C.indi_adjustments)
        self.group.start_price = 0


class Bid(Page):
    form_model = 'player'

    def live_method(player, quit_price):
        player.bid = quit_price - 1
        player.group.players_left_num -= 1
        return {0: player.group.players_left_num}

    def vars_for_template(self):
        display_players_num = self.session.config['display_players_num']
        return dict(
            which_round=self.group.round_number,
            pv=self.player.pv,
            start_price=self.group.start_price,
            display_players_num=display_players_num,
        )

    def before_next_page(self, **kwargs):
        pass


class WaitAfterBid(WaitPage):
    def after_all_players_arrive(self):
        all_pv = self.group.get_all_pvs()
        # print(f'I am player {self.player.id_in_group}. The 2nd time: {self.player.pv}')
        all_bids = self.group.get_all_bids()
        ascending_price_tbr = self.session.config['ascending_price_tbr']

        winner = get_winner(all_bids, ascending_price_tbr)
        highest_bid = get_highest_bid(all_bids)
        second_highest_bid = get_second_highest_bid(all_bids)

        for current_player in self.group.get_players():
            current_player.group.highest_bid_this_round = highest_bid
            current_player.group.second_highest_bid_this_round = second_highest_bid
            current_id = current_player.id_in_group

            payoff_this_round = get_my_payoff(current_id, winner, all_pv[current_id-1], second_highest_bid) * my_payoff_unit
            current_player.payoff = payoff_this_round
            current_player.participant.vars['payoff_ac'] += payoff_this_round

        self.group.winner = winner
        self.group.players_left_num = 4


class Feedback(Page):
    def vars_for_template(self):
        if self.player.id_in_group == self.group.winner:
            self.player.is_winner = True

        ecu_this_round = self.player.payoff / my_payoff_unit
        ecu_this_round = round(ecu_this_round, 0)
        payoff_this_round = round(self.player.payoff, 0)

        return dict(
            pv=self.player.pv,
            bid=self.player.bid,
            winner=self.group.winner,
            highest_bid_this_round=self.group.highest_bid_this_round,
            winning_price_this_round=self.group.second_highest_bid_this_round,
            ecu_this_round=ecu_this_round,
            payoff_this_round=payoff_this_round,
            my_id=self.player.id_in_group,
            which_round=self.group.round_number,
        )

    def before_next_page(self, **kwargs):
        pass


class WaitAfterFeedback(WaitPage):
    pass


page_sequence = [Start, Bid, WaitAfterBid, Feedback, WaitAfterFeedback]
