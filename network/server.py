import socket

from network import utils


def start():
    ip = utils.get_all_local_ips()
    local_ip, hamachi_ip, radmin_ip = ip['local'], ip['hamachi'], ip['radmin']
    _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    _socket.bind(('0.0.0.0', 7878))
    _socket.listen(5)
    return _socket, local_ip, hamachi_ip, radmin_ip


def accept_connections(_socket):
    connection, address = _socket.accept()
    ip, _ = address
    try:
        print('Подсоединен:', socket.gethostbyaddr(ip)[0].split('.')[0]) # socket.getfqdn(ip).split('.')[0] вызывает ошибку
    except socket.herror:
        print('Подсоединен:', ip)
    return connection