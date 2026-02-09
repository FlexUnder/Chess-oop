import socket


def connect_to_server(server_ip):
    print('Соединение...')
    server = (server_ip, 7878)
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        connection.connect(server)
        print('\nСервер найден! Подключен к:', socket.gethostbyaddr(server_ip)[0].split('.')[0]) # socket.getfqdn(ip).split('.')[0] вызывает ошибку
    except socket.herror:
        print('\nСервер найден! Подключен к:', server_ip)
    except socket.gaierror:
        print('Некорректный ip адрес')
        return None, False
    except TimeoutError:
        print('Cервер не найден. Убедитесь в правильности написания адреса. Если подключаетесь по Hamachi, то убедитесь в том что Hamachi включен')
        return None, False
    except ConnectionRefusedError:
        print('Компьютер найден, но соединение было отвергнуто. Проверьте запущен ли сервер, проверьте настройки firewall')
        return None, False
    return connection, True