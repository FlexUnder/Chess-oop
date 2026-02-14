import re


class GameMode:
    def __init__(self, board, rules, render):
        self.board = board
        self.rules = rules
        self.render = render

    def run(self):
        raise NotImplementedError

    def normalize_input(self, raw_input):
        russian_to_latin = {
            'а': 'a', 'б': 'b', 'в': 'c', 'г': 'd', 'д': 'e', 'е': 'f', 'ж': 'g', 'з': 'h',
            'А': 'a', 'Б': 'b', 'В': 'c', 'Г': 'd', 'Д': 'e', 'Е': 'f', 'Ж': 'g', 'З': 'h'
        }

        normalized = raw_input.translate(str.maketrans(russian_to_latin))
        match = re.match(r'([a-h][1-8])\s*([a-h][1-8])', normalized)
        if match:
            return match.groups()
        return None