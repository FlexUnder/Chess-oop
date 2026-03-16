from . import setup
from . import rules
from . import render


def after_init(board, rules_instance):
    """
    Вызывается из Game.__init__() после создания board и rules.
    Связывает доску с rules чтобы apply_move знал о взятиях.
    """
    setup.link_rules(board, rules_instance)
