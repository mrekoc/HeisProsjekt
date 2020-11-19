import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('', 33546))
sock.listen(5)

while True:
    clientSock, address = sock.accept()
    print(f"Connection from {address} has been established!")
    clientSock.send(bytes("Welcome to the server!", "utf-8"))
    clientSock.close()