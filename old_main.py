import copy
import os
import platform
import random
import re
import time


def print_board(board, player):
    print(f"\nХод: {'белых' if player == 'white' else 'черных'}")

    for i in range(8):
        row_num = 8 - i
        print(f"{row_num:2}", end=" ")
        for j in range(8):
            piece = board[i][j]
            print(f"{piece.symbol if piece else '○'}", end=" ")
        print()

    print("   a b c d e f g h")


def normalize_input(cmd):
    russian_to_latin = {
        'а': 'a', 'б': 'b', 'в': 'c', 'г': 'd', 'д': 'e', 'е': 'f', 'ж': 'g', 'з': 'h',
        'А': 'a', 'Б': 'b', 'В': 'c', 'Г': 'd', 'Д': 'e', 'Е': 'f', 'Ж': 'g', 'З': 'h'
    }

    normalized = cmd.translate(str.maketrans(russian_to_latin))
    match = re.match(r'([a-h][1-8])\s*([a-h][1-8])', normalized)
    if match:
        return match.groups()
    return None


def pos_to_coords(pos):
    if len(pos) != 2:
        return None

    col, row = pos[0].lower(), pos[1]
    if not ('a' <= col <= 'h') or not ('1' <= row <= '8'):
        return None

    x = 8 - int(row)  # 1->7, 8->0
    y = ord(col) - ord('a')
    return x, y


def coords_to_pos(x, y):
    col = chr(ord('a') + y)
    row = str(8 - x)
    return col + row


def find_king(board, color):
    for i in range(8):
        for j in range(8):
            piece = board[i][j]
            if isinstance(piece, King) and piece.color == color:
                return i, j
    return None


def local_game():
    board = setup_board()
    player = 'white'
    game_over = False

    print("Форматы: e2 e4, e2e4")
    print("quit - выход, help - справка")

    while not game_over:
        print_board(board, player)
        if is_checkmate(board, player):
            winner = "белые" if player == 'black' else "черные"
            print(f"\nШАХ И МАТ! Победили {winner}!")
            break
        if is_stalemate(board, player):
            print("\nПАТ! Ничья!")
            break

        while True:
            cmd = input(f"\n{player.upper()} ход > ").strip()

            if cmd == 'quit':
                print("Игра завершена")
                return

            if cmd == 'help':
                print("Формат: e2 e4 (с пробелом) или e2e4 (без)")
                print("Поддержка русских: а2 а4, а2а4")
                continue

            parsed = normalize_input(cmd)
            if not parsed:
                print("Неверный формат! Примеры: e2 e4, e2e4, а2 а4")
                continue

            from_pos_str, to_pos_str = parsed
            from_pos = pos_to_coords(from_pos_str)
            to_pos = pos_to_coords(to_pos_str)

            if not from_pos or not to_pos:
                print("Неверные координаты (a-h, 1-8)")
                continue

            fx, fy = from_pos
            piece = board[fx][fy]

            if not piece:
                print(f"На {from_pos_str} нет фигуры")
                continue

            if piece.color != player:
                print("Ходите своей фигурой!")
                continue

            valid_moves = get_valid_moves(board, from_pos, player)

            if to_pos not in valid_moves:
                print(f"Недопустимый ход с {from_pos_str}")
                if valid_moves:
                    moves_str = " ".join(coords_to_pos(*m) for m in valid_moves)
                    print(f"Возможные: {moves_str}")
                continue


            tx, ty = to_pos
            board[tx][ty] = piece
            board[fx][fy] = None

            player = 'black' if player == 'white' else 'white'
            print(f"Ход {from_pos_str}-{to_pos_str} выполнен!")
            break

def online_game():
    print('  Выбирете тип подключения (q чтобы выйти): ')
    print('\t1. Создать сервер')
    print('\t2. Подключиться (по ip)')
    is_server = False
    while True:
        choice = input('\t ~> ')
        if choice == '1':
            connection = netcode.start_server()
            is_server = True
            break
        if choice == '2':
            ip_server = input('Введите ip сервера: ')
            connection, success = netcode.connect_to_server(ip_server)
            if success:
                break
            else:
                print('\n  Выберете тип подключения: ')
                print('\t1. Создать сервер')
                print('\t2. Подключиться (по ip)')
                continue
        if choice == 'q':
            print('Завершение программы')
            exit()
        print('Некорректный ввод, введите 1/2')

    if is_server:
        player_color = random.choice(['white', 'black'])
        netcode.send_data(connection, player_color)
    else:
        time.sleep(1)
        player_color = 'white' if netcode.listen_data(connection) == 'black' else 'black'
        print('Соединение установленно')


    board = setup_board()
    turn = 'white'

    print("Форматы: e2 e4, e2e4")
    print("quit - выход, help - справка")

    while True:
        clear_console()
        print(f'Вы играете за {'белых' if player_color == 'white' else 'черных'}\n')
        print_board(board, turn)
        if is_checkmate(board, turn):
            winner = "белые" if turn == 'black' else "черные"
            print(f"\nШАХ И МАТ! Победили {winner}!")
            break
        if is_stalemate(board, turn):
            print("\nПАТ! Ничья!")
            break

        while True:
            if player_color == turn:
                cmd = input(f"\n{turn.upper()} ход > ").strip()

                if cmd == 'quit':
                    print("Игра завершена")
                    return

                if cmd == 'help':
                    print("Формат: e2 e4 (с пробелом) или e2e4 (без)")
                    continue

                parsed = normalize_input(cmd)
                if not parsed:
                    print("Неверный формат! Примеры: e2 e4, e2e4, а2 а4")
                    continue

                from_pos_str, to_pos_str = parsed
                from_pos = pos_to_coords(from_pos_str)
                to_pos = pos_to_coords(to_pos_str)

                if not from_pos or not to_pos:
                    print("Неверные координаты (a-h, 1-8)")
                    continue

                fx, fy = from_pos
                piece = board[fx][fy]

                if not piece:
                    print(f"На {from_pos_str} нет фигуры")
                    continue

                if piece.color != turn:
                    print("Ходите своей фигурой!")
                    continue

                valid_moves = get_valid_moves(board, from_pos, turn)

                if to_pos not in valid_moves:
                    print(f"Недопустимый ход с {from_pos_str}")
                    if valid_moves:
                        moves_str = " ".join(coords_to_pos(*m) for m in valid_moves)
                        print(f"Возможные: {moves_str}")
                    continue

                tx, ty = to_pos
                board[tx][ty] = piece
                board[fx][fy] = None

                print(f"Ход {from_pos_str}-{to_pos_str} выполнен!")
                netcode.send_data(connection, f'{tx} {ty} {fx} {fy}')
                break
            else:
                print('\n Ход противника...')
                ops_move = netcode.listen_data(connection)
                print(f'|{ops_move}|')
                tx, ty, fx, fy = map(int, ops_move.split())
                piece = board[fx][fy]
                board[tx][ty] = piece
                board[fx][fy] = None
                break
        turn = 'black' if turn == 'white' else 'white'


def main_menu():
    while True:
        clear_console()
        print(''.join(open('assets/logo.txt').readlines()))
        print('\n')
        print('\t' * 6 + 'Выберите режим')
        print('\t' * 6 + ' 1. Онлайн')
        print('\t' * 6 + ' 2. Локально\n')
        game_mode = input('\t' * 6 + '  > ')
        if game_mode == '1':
            online_game()
        elif game_mode == '2':
            local_game()
        elif game_mode == 'q':
            print('\t\t\t\t\tВыход...')
            exit()
        else:
            print('Не знаю такого, повторите ввод. Нажмите Enter чтобы продолжить')
            input()
            continue


def clear_console():
    system = platform.system().lower()
    if system == "windows":
        os.system('cls')
    else:
        os.system('clear')


if __name__ == "__main__":
    main_menu()
