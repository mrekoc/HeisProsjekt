
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('', 15657))

#msg = s.recv(1024)
#msg = msg.decode("utf-8")
#print(msg)
msg = []
while True:
	cmd1 = int(input("Command:"))
	msg.append(cmd1)
	cmd2 = int(input("Floor:"))
	msg.append(cmd2)
	cmd3 = int(input("Command3:"))
	msg.append(cmd3)
	cmd4 = int(input("Command4:"))
	msg.append(cmd4)
	msg = bytes(msg)
	s.sendto(msg, ('', 15657))
	msg = []

	#msg = s.recv(1024)
	#msg = msg.decode("utf-8")
	#print(msg)