from base import WHITE


def get_player_input(color):
    if color == WHITE:
        player_input = input('\t' * 4 + ' Ход белых > ')
    else:
        player_input = input('\t' * 4 + ' Ход черных > ')
    return player_input


def print_center(text, offset=0, padding_left=4):
    print('\t' * (padding_left + offset) + text)
