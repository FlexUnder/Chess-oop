import re

from base import WHITE


class GameMode:
    def __init__(self, board, rules, render):
        self.board = board
        self.rules = rules
        self.render = render
        self.turn = WHITE

    def run(self):
        raise NotImplementedError

    def normalize_input(self, raw_input):
        russian_to_latin = {
            'а': 'a', 'б': 'b', 'в': 'c', 'г': 'd', 'д': 'e', 'е': 'f', 'ж': 'g', 'з': 'h',
            'А': 'a', 'Б': 'b', 'В': 'c', 'Г': 'd', 'Д': 'e', 'Е': 'f', 'Ж': 'g', 'З': 'h'
        }

        normalized = raw_input.translate(str.maketrans(russian_to_latin)).lower().strip()

        if raw_input == 'danger' or raw_input == 'undo':
            return raw_input

        match_two = re.match(r'^([a-h][1-8])\s*([a-h][1-8])$', normalized)
        if match_two:
            return match_two.groups()

        match_one = re.match(r'^([a-h][1-8])$', normalized)
        if match_one:
            return (match_one.group(1),)

        return None

    def parse_input(self, normalized_input):
        def to_coords(pos):
            return letters_to_coordinates[pos[0]], 8 - int(pos[1])

        letters_to_coordinates = {
            'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7
        }

        if normalized_input == 'danger' or normalized_input == 'undo':
            return normalized_input

        if len(normalized_input) == 1:
            return (*to_coords(normalized_input[0]),)

        elif len(normalized_input) == 2:
            x_from, y_from = to_coords(normalized_input[0])
            x_to, y_to = to_coords(normalized_input[1])
            return x_from, y_from, x_to, y_to
        return None