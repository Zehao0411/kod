from ._builtin import Page


class Instructions(Page):
    form_model = 'player'


class Task1(Page):
    form_model = 'player'
    form_fields = ['task1']

    def before_next_page(self, **kwargs):
        self.player.participant.math_puzzles_num_correct = 0
        if self.player.task1 == 34:
            self.player.participant.math_puzzles_num_correct += 1


class Task2(Page):
    form_model = 'player'
    form_fields = ['task2']

    def before_next_page(self, **kwargs):
        if self.player.task2 == 319:
            self.player.participant.math_puzzles_num_correct += 1


class Task3(Page):
    form_model = 'player'
    form_fields = ['task3']

    def before_next_page(self, **kwargs):
        if self.player.task3 == 62:
            self.player.participant.math_puzzles_num_correct += 1


class Results(Page):
    pass


page_sequence = [Instructions, Task1, Task2, Task3, Results]

