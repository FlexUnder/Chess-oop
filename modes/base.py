import re

from base import WHITE


class GameMode:
    def __init__(self, board, rules, render):
        self.board = board
        self.rules = rules
        self.render = render
        self.current_player = WHITE

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

    def parse_input(self, normalized_input):
        letters_to_coordinates = {
            'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7
        }
        position_from, position_to = normalized_input
        x_from, y_from = letters_to_coordinates[position_from[0]], int(position_from[1]) - 1
        x_to, y_to = letters_to_coordinates[position_to[0]], int(position_to[1]) - 1
        return x_from, y_from, x_to, y_to