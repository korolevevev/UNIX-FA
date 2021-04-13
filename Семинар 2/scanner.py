import socket
from threading import Thread

N = 2**16 - 1

for port in range(1,100):
    sock = socket.socket()
    print("Создали сокет")
    try:
        print(port)
        sock.connect(('127.0.0.1', port))
        print("Подключили сокет к порту")
        print("Порт", i, "открыт!")
    except:
        continue
    finally:
        sock.close()
        print("Сокет закрыт, всем спасибо! С Вами работал Илья Королев, группа ПИ19-2.")