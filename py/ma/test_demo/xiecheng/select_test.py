# request -> urlib -> socket
import socket

from urllib.parse import urlparse


def get_url(url):
    # request html via socket
    url = urlparse(url)
    host = url.netloc
    path = url.path
    if path == "":
        path = "/"

    # create connection of socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.setblocking(False)
    try:
        client.connect((host, 80))
    except BlockingIOError as e:
        pass

    while True:
        try:
            client.send("GET {} HTTP/1.1\r\nHost:{}\r\nConnection:close\r\n\r\n".format(path, host).encode("utf8"))
            break
        except OSError as e:
            pass

    data = b""
    while True:
        try:
            d = client.recv(1024)
        except BlockingIOError as e:
            continue

        if d:
            data += d
        else:
            break

    data = data.decode("utf8")
    # html_data = data.split("\r\n\r\n")[1]
    print(data)
    client.close()


if __name__ == '__main__':
    get_url("http://www.baidu.com")