import socket


def check_internet(
    host="8.8.8.8",
    port=53,
    timeout=5,
):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM,).connect(
            (
                host,
                port,
            )
        )
        # If there is a connection return True
        return True
    except socket.error:
        # If there isn't a connection return False
        return False
