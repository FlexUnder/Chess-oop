import socket
import ipaddress
import ifaddr


def get_all_local_ips():
    hamachi_ips, radmin_ips = find_hamachi_ips(), find_radmin_ips()
    ips = {'local': get_default_local_ip(), 'hamachi': hamachi_ips, 'radmin': radmin_ips}
    return ips


def get_default_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    local_ip = s.getsockname()[0]
    s.close()
    return local_ip


def find_hamachi_ips():
    hamachi_net = ipaddress.ip_network("25.0.0.0/8")
    result = []
    for adapter in ifaddr.get_adapters():
        name = (adapter.nice_name or "").lower()
        name_hint = any(tok in name for tok in ("hamachi", "logmein", "ham"))
        for ipinfo in adapter.ips:
            addr = ipinfo.ip
            if isinstance(addr, tuple):
                addr = addr[0]
            try:
                ip_obj = ipaddress.ip_address(addr)
            except ValueError:
                continue
            if ip_obj.version == 4 and ip_obj in hamachi_net:
                result.append(str(ip_obj))
            elif ip_obj.version == 4 and name_hint:
                result.append(str(ip_obj))
    return list(dict.fromkeys(result))


def find_radmin_ips():
    radmin_net = ipaddress.ip_network("26.0.0.0/8")
    result = []
    for adapter in ifaddr.get_adapters():
        name = (adapter.nice_name or "").lower()
        name_hint = any(tok in name for tok in ("radmin", "vpn"))
        for ipinfo in adapter.ips:
            addr = ipinfo.ip
            if isinstance(addr, tuple):
                addr = addr[0]
            try:
                ip_obj = ipaddress.ip_address(addr)
            except ValueError:
                continue
            if ip_obj.version == 4 and ip_obj in radmin_net:
                result.append(str(ip_obj))
            elif ip_obj.version == 4 and name_hint:
                result.append(str(ip_obj))
    return list(dict.fromkeys(result))
