import socket

from network import utils


def start_server():
    local_ip, hamachi_ip, is_hamachi_found = utils.get_all_local_ips(True)
    _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    _socket.bind(('0.0.0.0', 7878))
    _socket.listen(5)
    print("Сервер запущен")
    print('Ваш ip: ' + local_ip + is_hamachi_found * f'\nВаш Hamachi ip: {hamachi_ip}')
    connection, address = _socket.accept()
    ip, _ = address
    try:
        print('Подсоединен:', socket.gethostbyaddr(ip)[0].split('.')[0]) # socket.getfqdn(ip).split('.')[0] вызывает ошибку
    except socket.herror:
        print('Подсоединен:', ip)
    return connection