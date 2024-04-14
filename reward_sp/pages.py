from ._builtin import Page


class Reward(Page):
    def vars_for_template(self):
        final_payoff_this_part = self.player.participant.vars['payoff_sp']

        return dict(
            final_payoff_this_part=final_payoff_this_part,
        )


page_sequence = [Reward]
