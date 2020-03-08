#!/usr/bin/python3
# 文件名：server.py

# 导入 socket、sys 模块
import socket
import sys
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", 8000))

server.listen()


def handle_sock(sock, addr):
    data = sock.recv(1024)
    print(data.decode("utf8"))
    re_data = input()
    sock.send(re_data.encode("utf8"))


# get data from client
# get 1K every time
while True:
    sock, addr = server.accept()

    client_thread = threading.Thread(target=handle_sock, args=(sock, addr))
    client_thread.start()

    # re_data = input()
    # data = sock.recv(1024)
    # print(data.decode("utf8"))

    # server.close()
    # sock.close()
