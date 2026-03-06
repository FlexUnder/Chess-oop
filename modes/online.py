import random

from network import server, client, protocol
from base import WHITE, BLACK
from base import SERVER, CLIENT
from ui import console
from modes import base


class Mode(base.GameMode):
    def __init__(self, board, rules, render, network_config):
        super().__init__(board, rules, render)
        self.network_type, self.connection_ip = network_config[0], network_config[1]
        self.turn = WHITE
        self.local_player_color = 'Not defined'
        self.connection = None
        self._init_connection()

    def _init_connection(self):
        if self.network_type == SERVER:
            self.socket, self.default_ip, self.hamachi_ip, self.radmin_ip = server.start()
        else:
            self.connection = client.connect_to_server(self.connection_ip)

    def run(self):
        if self.network_type == SERVER:
            self.output_ips()
            self.connection = server.accept_connections(self.socket)
            self.local_player_color = random.choice([WHITE, BLACK])
            protocol.send_data(self.connection, self.local_player_color)
        else:
            opponent_color = protocol.listen_data(self.connection)
            self.local_player_color = BLACK if opponent_color == WHITE else WHITE

        while True:
            console.clear_console()
            console.print_logo()
            self.render.print_board(self.board)

            if self.turn == self.local_player_color:
                raw_input = console.get_player_input(self.turn)
                normalized = self.normalize_input(raw_input)
                if not normalized:
                    self.handle_input_error('Неверный формат! Примеры: e2 e4, e2e4, а2 а4')
                    continue
                x_from, y_from, x_to, y_to = self.parse_input(normalized)
                legal_moves = self.rules.get_legal_moves(self.board, x_from, y_from, self.turn)
                if (x_to, y_to) not in legal_moves:
                    self.handle_input_error('Невозможный ход!')
                    continue

                self.board.apply_move(x_from, y_from, x_to, y_to)

                print(f'{x_from} {y_from} {x_to} {y_to}')
                protocol.send_data(self.connection, f'{x_from} {y_from} {x_to} {y_to}')
            else:
                console.print_center('Ход оппонента')
                opponent_move = map(int, protocol.listen_data(self.connection).split())
                print(opponent_move)
                x_from, y_from, x_to, y_to = opponent_move
                self.board.apply_move(x_from, y_from, x_to, y_to)
            self.switch_turn()

            finish_message = self.rules.get_game_finish_message(self.board, self.turn)
            if finish_message:
                print(finish_message)
                break

                # if self.rules.is_stalemate(self.board, self.current_player):
                #     print("Пат!")
                #     break

    def handle_input_error(self, message):
        print('\n' * 3 + '\t' * 4 + message)
        input('\n' + '\t' * 4 + 'Нажмите Enter чтобы продолжить...')

    def output_ips(self):
        console.clear_console()
        console.print_logo()
        console.print_center('\n\n\n\n\n\niP для подключения:')
        console.print_center(f'\nDefault: {self.default_ip}', 1)
        if self.hamachi_ip is not None:
            console.print_center(f'Hamachi: {self.hamachi_ip}', 1)
        if self.radmin_ip is not None:
            console.print_center(f'Radmin: {self.radmin_ip}', 1)

    def switch_turn(self):
        self.turn = BLACK if self.turn == WHITE else WHITE


