import socket
from threading import Thread, Lock

class tcp:

    lock = Lock()

    def serverFunction(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('10.100.23.147', 33546))
        sock.listen(5)

        while True:
            self.lock.acquire()
            clientSock, address = sock.accept()
            print(f"Server: Connection from {address} has been established!")
            clientSock.send(bytes("Server: Welcome to the server!", "utf-8"))
            clientSock.close()
            self.lock.release()

    def clientFunction(self):

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('10.100.23.147', 33546))
        
        for ping in range(10):
            self.lock.acquire()
            msg = s.recv(1024)
            msg = msg.decode("utf-8")
            print("Client:", msg)
            self.lock.release()


def main():
    
    tcp1 = tcp()

    serverThread = Thread(target = tcp1.serverFunction)
    clientThread = Thread(target = tcp1.clientFunction)

    serverThread.start()
    clientThread.start()

    serverThread.join()
    clientThread.join()
    

if __name__ == "__main__":
    main()
