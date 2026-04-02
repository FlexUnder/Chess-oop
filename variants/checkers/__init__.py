from . import setup
from . import rules
from . import render
from . import config


def after_init(board, rules_instance):
    setup.link_rules(board, rules_instance)
