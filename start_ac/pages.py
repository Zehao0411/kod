import random
from otree.api import *
from settings import my_show_up_fee, my_num_of_rounds, my_players_per_group, my_groups_draws, my_indi_adjustments, my_payoff_unit
from .models import C


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


class Instructions(Page):
    def vars_for_template(self):
        second_price_tbr = self.player.session.config['second_price_tbr']
        if second_price_tbr == 'efficient':
            is_efficient = True
        elif second_price_tbr == 'inefficient':
            is_efficient = False
        else:
            is_efficient = None

        show_up_fee = my_show_up_fee
        my_id = self.player.id_in_group

        total_round_num = my_num_of_rounds
        players_per_group = my_players_per_group
        players_num_left_me = players_per_group - 1

        group_draws = my_groups_draws
        min_group_draw = min(my_groups_draws)
        max_group_draw = max(my_groups_draws)
        group_draws_length = len(group_draws)
        example_adjustment = my_indi_adjustments[2]
        example_pv = 30 + example_adjustment

        indi_adjustments = my_indi_adjustments

        return dict(
            is_efficient=is_efficient,
            show_up_fee=show_up_fee,
            my_id=my_id,
            total_round_num=total_round_num,
            players_per_group=players_per_group,
            players_num_left_me=players_num_left_me,

            group_draws=group_draws,
            min_group_draw=min_group_draw,
            max_group_draw=max_group_draw,
            group_draws_length=group_draws_length,
            example_adjustment=example_adjustment,
            example_pv=example_pv,

            indi_adjustments=indi_adjustments,
        )


class InstructionsTraining(Page):
    def before_next_page(self, **kwargs):
        self.player.pv = get_private_value(self.group.group_draw, C.indi_adjustments)


class Wait(WaitPage):
    pass


class BidTraining(Page):
    form_model = 'player'

    def live_method(player, quit_price):
        player.bid = quit_price - 1
        player.group.players_left_num -= 1
        return {0: player.group.players_left_num}

    def vars_for_template(self):
        self.group.start_price = 0
        display_players_num = self.session.config['display_players_num']
        return dict(
            which_round=self.group.round_number,
            pv=self.player.pv,
            start_price=self.group.start_price,
            display_players_num=display_players_num,
        )


class WaitAfterBidTraining(WaitPage):
    def after_all_players_arrive(self):
        all_pv = self.group.get_all_pvs()
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

        self.group.winner = winner
        self.group.players_left_num = 4


class FeedbackTraining(Page):
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
        self.player.participant.vars['payoff_ac'] = 0


page_sequence = [Instructions, InstructionsTraining, Wait, BidTraining, WaitAfterBidTraining, FeedbackTraining]
# page_sequence = [Instructions, Wait]
