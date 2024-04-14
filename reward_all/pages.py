from ._builtin import Page
from settings import my_show_up_fee, my_payoff_unit


def cal_wisconsin_payoff(num):
    if num < 6:
        payoff = 1
    elif 6 <= num <= 7:
        payoff = 2
    else:
        payoff = 3
    return payoff


def cal_math_puzzles_payoff(num):
    payoff = 2 * num
    return payoff


class Results(Page):
    def vars_for_template(self):
        show_up_fee = my_show_up_fee

        wisc_idx = self.session.config['app_sequence'].index('wisconsin')
        ac_idx = self.session.config['app_sequence'].index('ascending_price')

        if wisc_idx < ac_idx:
            ac_tail = True
        else:
            ac_tail = False

        ascending_payoff = self.player.participant.vars['payoff_ac']
        ascending_payoff = round(ascending_payoff, 0)
        ascending_ecu = ascending_payoff / my_payoff_unit
        ascending_ecu = round(ascending_ecu, 0)

        wisc_correct_num = self.player.participant.wisconsin_num_correct
        wisc_payoff = cal_wisconsin_payoff(wisc_correct_num)
        math_puzzles_correct_num = self.player.participant.math_puzzles_num_correct
        math_puzzles_payoff = cal_math_puzzles_payoff(math_puzzles_correct_num)

        final_payoff = show_up_fee + wisc_payoff + math_puzzles_payoff + ascending_payoff

        self.player.wisc_payoff = wisc_payoff
        self.player.math_puzzles_payoff = math_puzzles_payoff
        self.player.final_payoff = final_payoff

        return dict(
            ac_tail=ac_tail,

            show_up_fee=show_up_fee,

            wisc_correct_num=wisc_correct_num,
            wisc_payoff=wisc_payoff,

            math_puzzles_correct_num=math_puzzles_correct_num,
            math_puzzles_payoff=math_puzzles_payoff,

            ascending_ecu=ascending_ecu,
            ascending_payoff=ascending_payoff,
            final_payoff=final_payoff,
        )


page_sequence = [Results]
