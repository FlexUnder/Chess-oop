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
        max_number = self.params['input_max_number']
        max_letter = self.params['input_max_letter']
        russian_to_latin = {
            'ф': 'a', 'и': 'b', 'с': 'c', 'в': 'd', 'у': 'e', 'а': 'f',
            'п': 'g', 'р': 'h', 'ш': 'i', 'о': 'j', 'л': 'k'
        }

        normalized = raw_input.lower().translate(str.maketrans(russian_to_latin)).strip()

        if normalized in ('danger', 'undo'):
            return normalized

        letters = 'abcdefghijk'
        max_l = letters[max_letter - 1]
        # Паттерн для одной клетки: буква + число (1 или 2 цифры)
        cell = rf'[a-{max_l}]\d{{1,2}}'

        match_two = re.match(rf'^({cell})\s*({cell})$', normalized)
        if match_two:
            return match_two.groups()

        match_one = re.match(rf'^({cell})$', normalized)
        if match_one:
            return (match_one.group(1),)

        return None

    def parse_input(self, normalized_input):
        if normalized_input in ('danger', 'undo'):
            return normalized_input

        # Кастомный парсер из конфига варианта
        if 'parse_input' in self.params:
            return self.params['parse_input'](normalized_input)

        # Стандартный шахматный парсер
        letters_to_coordinates = {
            'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4,
            'f': 5, 'g': 6, 'h': 7, 'i': 8, 'j': 9, 'k': 10
        }

        def to_coords(pos):
            return letters_to_coordinates[pos[0]], 8 - int(pos[1:])

        if len(normalized_input) == 1:
            return (*to_coords(normalized_input[0]),)
        elif len(normalized_input) == 2:
            x_from, y_from = to_coords(normalized_input[0])
            x_to, y_to = to_coords(normalized_input[1])
            return x_from, y_from, x_to, y_to

        return None