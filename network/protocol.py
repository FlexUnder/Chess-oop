def send_data(connection, data):
    try:
        connection.sendall(data.encode('utf-8'))
    except ConnectionResetError:
        print('Соединение разорвано. Нажмите Enter')
        connection.close()
        input()
    except ConnectionAbortedError:
        print('Соединение разорвано. Нажмите Enter')
        connection.close()
        input()


def listen_data(connection):
    try:
        data = connection.recv(1024)
        return data.decode("utf-8")
    except ConnectionResetError:
        print('Ваш противник вышел!. Нажмите Enter')
        connection.close()
        input()
    except ConnectionAbortedError:
        print('Ваш противник вышел!. Нажмите Enter')
        connection.close()
        input()
