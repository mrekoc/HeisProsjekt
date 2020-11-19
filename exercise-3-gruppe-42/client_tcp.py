
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('10.100.23.147', 33546))

msg = s.recv(1024)
msg = msg.decode("utf-8")
print(msg)

for i in range(10):
	msg = "I am boring \0"
	s.sendto(bytes(msg, "utf-8"), ('10.100.23.147', 33546))

	msg = s.recv(1024)
	msg = msg.decode("utf-8")
	print(msg)