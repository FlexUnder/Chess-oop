from base import WHITE


def get_player_input(color):
    if color == WHITE:
        player_input = input('\t' * 5 + ' Ход белых > ')
    else:
        player_input = input('\t' * 5 + ' Ход черных > ')
    return player_input
