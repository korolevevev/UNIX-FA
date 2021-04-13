import socket

sock = socket.socket()
print("Создали новый сокет")
sock.bind(('', 9090))
print("Мы готовы принимать соединение!")
sock.listen(0)
conn, addr = sock.accept()
print(addr)

msg = ''

while True:
	data = conn.recv(1024)
	if not data:
		break
	msg += data.decode()
	conn.send(data)

print(msg)

conn.close()