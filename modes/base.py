import re

from base import WHITE


class GameMode:
    def __init__(self, board, rules, render, config):
        self.board = board
        self.rules = rules
        self.render = render
        self.turn = WHITE
        self.params = config.params

    def run(self):
        raise NotImplementedError

    def normalize_input(self, raw_input):
        max_number, max_letter = self.params['input_max_number'], self.params['input_max_letter']
        russian_to_latin = {
            'ф': 'a', 'и': 'b', 'с': 'c', 'в': 'd', 'у': 'e', 'а': 'f', 'п': 'g', 'р': 'h', 'ш': 'i', 'о': 'j', 'л': 'k'
        }

        normalized = raw_input.lower().translate(str.maketrans(russian_to_latin)).strip()

        if raw_input == 'danger' or raw_input == 'undo':
            return raw_input

        pattern = rf'^([a-{list(russian_to_latin.values())[max_letter - 1]}][1-{max_number}])\s*([a-{list(russian_to_latin.values())[max_letter - 1]}][1-{max_number}])$'
        match_two = re.match(pattern, normalized)
        if match_two:
            return match_two.groups()

        match_one = re.match(rf'^([a-{list(russian_to_latin.values())[max_letter - 1]}][1-{max_number}])$', normalized)
        if match_one:
            return (match_one.group(1),)

        return None

    def parse_input(self, normalized_input):

        def to_coords(pos):
            return letters_to_coordinates[pos[0]], 8 - int(pos[1])

        letters_to_coordinates = {
            'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8, 'j': 9, 'k': 10
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