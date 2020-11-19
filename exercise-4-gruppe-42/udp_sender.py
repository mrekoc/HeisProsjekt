import socket
import json

class udp:

    UDPIP = "255.255.255.255"
    UDPPORT_SEND = 20009
    UDPPORT_RCV = 30000
    sendAdress = "10.100.23.223"

    def sendTo(self):
        while True:
            message = input("Enter your message to server:")
            #self.message = message
            message_ = {
            "queue info": {
            "queue" : "E3",
            "position" : "E5",
            "message" : message
            }
        }
            message = json.dumps(message_)
            #for pings in range(int(1024/len(message))):
            #    message += message  #"Hei, gaar bra???"
            sendSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sendSock.bind(('', self.UDPPORT_SEND))
            sendSock.settimeout(1.0) 
            sendSock.sendto( bytes(message, "ascii") , (self.sendAdress, self.UDPPORT_SEND))
            #sendSock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        


    def receiveFrom(self):
        
        receiveSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #receiveSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        receiveSock.bind(('', self.UDPPORT_SEND))
        i = 0
        while i<10:
            i += 1
            print("READY TO RECV")
            message, address = receiveSock.recvfrom(1024)
            message = message.decode("ascii")
            print(message) 
            message = message.encode('ascii') 
            #receiveSock.sendto(message, address)
             




def main():
    udp1 = udp()
    #udp1.sendTo("Hei, det er konge!!!!!")
    #udp1.receiveFrom()
    while True:
        #message = input("Enter your message to server:")
        udp1.sendTo()
        #udp1.receiveFrom()


if __name__ == "__main__":
    main()
