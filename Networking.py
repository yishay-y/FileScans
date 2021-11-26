import socket

def check_connection(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((str(ip), int(port)))
    sock.close()

    if result == 0:
        return True
    return False
