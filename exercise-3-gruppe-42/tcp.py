import socket
from threading import Thread

class tcp: 
    
    TCPPORT_FIXED_SIZE = 34933
    TCPPPORT_ZERO_TERMINATOR = 33546
    sendAdress = "10.100.23.147"
    LOCAL_PORT = 20009

    def client(self):

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.sendAdress, 33546))
        message = sock.recv(1024)
        print(message)

        messageSend = bytes("hei\0", "utf-8")
        sock.send(messageSend)
        print(sock.recv(1024))

        sock.close()


    
    def server(self):

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.connect((self.sendAdress, 33546))
            sock.send(bytes("Connect to: 10.100.23.223:20009\0", "utf-8"))
            #sock.bind(('', self.LOCAL_PORT))
            print("hellooooo")
        except:
            print("oh noes")
            

        #sock.send(connectMessage)

        listenSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #listenSock.bind(('',self.LOCAL_PORT))
        listenSock.listen(5)
        

        conn, addr = listenSock.accept()
        
        data = conn.recv(1024)
        print(data, addr)

        sock.close()
        listenSock.close()
""" 
        recieveThread = Thread(target = listenSock.recv(1024))
        sendThread = Thread(target = listenSock.send())
        
        recieveThread.start()
        sendThread.start()

        recieveThread.join()
        sendThread.join()


 """






def main():
    tcp1 = tcp()
    tcp1.server()
    tcp1.client()

if __name__ == "__main__":
    main()