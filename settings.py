import random
from os import environ

SESSION_CONFIG_DEFAULTS = dict(real_world_currency_per_point=1, participation_fee=0)

SESSION_CONFIGS = [
    dict(
        name='efficient_display', num_demo_participants=None,
        app_sequence=[
            'start_all',
            'wisconsin', 'math_puzzles',
            'start_ac', 'ascending_price',
            'reward_all',
        ],
        second_price_tbr='efficient', ascending_price_tbr='efficient', display_players_num=True,
    ),
    dict(
        name='inefficient_display', num_demo_participants=None,
        app_sequence=[
            'start_all',
            'wisconsin', 'math_puzzles',
            'start_ac', 'ascending_price',
            'reward_all',
        ],
        second_price_tbr='inefficient', ascending_price_tbr='inefficient', display_players_num=True,
    ),
    dict(
        name='efficient_no_display', num_demo_participants=None,
        app_sequence=[
            'start_all',
            'wisconsin', 'math_puzzles',
            'start_ac', 'ascending_price',
            'reward_all',
        ],
        second_price_tbr='efficient', ascending_price_tbr='efficient', display_players_num=False,
    ),
    dict(
        name='inefficient_no_display', num_demo_participants=None,
        app_sequence=[
            'start_all',
            'wisconsin', 'math_puzzles',
            'start_ac', 'ascending_price',
            'reward_all',
        ],
        second_price_tbr='inefficient', ascending_price_tbr='inefficient', display_players_num=False,
    ),
    dict(
        name='efficient_display_head', num_demo_participants=None,
        app_sequence=[
            'start_all',
            'start_ac', 'ascending_price',
            'wisconsin', 'math_puzzles',
            'reward_all',
        ],
        second_price_tbr='efficient', ascending_price_tbr='efficient', display_players_num=True,
    ),
    dict(
        name='inefficient_display_head', num_demo_participants=None,
        app_sequence=[
            'start_all',
            'start_ac', 'ascending_price',
            'wisconsin', 'math_puzzles',
            'reward_all',
        ],
        second_price_tbr='inefficient', ascending_price_tbr='inefficient', display_players_num=True,
    ),
    dict(
        name='test', num_demo_participants=None, app_sequence=[
            'start_ac', 'ascending_price',
        ],
        second_price_tbr='inefficient', ascending_price_tbr='inefficient', display_players_num=False,
    ),
]

LANGUAGE_CODE = 'zh-hans'
REAL_WORLD_CURRENCY_CODE = 'CNY'
USE_POINTS = False
DEMO_PAGE_INTRO_HTML = ''
PARTICIPANT_FIELDS = [
    'wisconsin_num_correct', 'wisconsin_payoff',
    'math_puzzles_num_correct',
]
SESSION_FIELDS = ['wisconsin',]
ROOMS = [
    {
        'name': 'ED',
        'display_name': '404A_efficient_display',
        'participant_label_file': '_rooms/CCBEF404A.txt',
    },
    {
        'name': 'ID',
        'display_name': '404A_inefficient_display',
        'participant_label_file': '_rooms/CCBEF404A.txt',
    },
    {
        'name': 'END',
        'display_name': '404A_efficient_no_display',
        'participant_label_file': '_rooms/CCBEF404A.txt',
    },
    {
        'name': 'IND',
        'display_name': '404A_inefficient_no_display',
        'participant_label_file': '_rooms/CCBEF404A.txt',
    },
    {
        'name': 'EDH',
        'display_name': '404A_efficient_display_head',
        'participant_label_file': '_rooms/CCBEF404A.txt',
    },
    {
        'name': 'IDH',
        'display_name': '404A_inefficient_display_head',
        'participant_label_file': '_rooms/CCBEF404A.txt',
    },
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')
SECRET_KEY = 'blahblah'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']


# customized settings
my_players_per_group = 4
my_num_of_rounds = 10
# my_groups_draws = list(range(5, 51))
# my_groups_draws = [19, 17, 19, 6, 34, 27, 9, 35, 21, 20]
my_groups_draws = [random.randint(5, 35) for _ in range(10)]
my_indi_adjustments = [0, 1, 2, 3, 4]
my_show_up_fee = 50
my_payoff_unit = 5
my_timeout_seconds = 8
