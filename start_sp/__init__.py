from otree.api import *
from settings import my_show_up_fee, my_num_of_rounds, my_players_per_group, my_groups_draws, my_indi_adjustments

c = cu

doc = 'Author: ZZH'


class C(BaseConstants):
    NAME_IN_URL = 'start_sp'
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
        second_price_tbr = player.session.config['second_price_tbr']
        if second_price_tbr == 'efficient':
            is_efficient = True
        elif second_price_tbr == 'inefficient':
            is_efficient = False
        else:
            is_efficient = None

        show_up_fee = my_show_up_fee
        my_id = player.id_in_group

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


class Wait(WaitPage):
    pass


page_sequence = [Instructions, Wait]
