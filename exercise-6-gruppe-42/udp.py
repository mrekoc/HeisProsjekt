import socket
from multiprocessing import Process, SimpleQueue
from threading import Thread


UDP_IP = "localhost"
UDP_PORT = 55681

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((UDP_IP, UDP_PORT))
    sock.settimeout(3)
except:
    pass

def udp_listen():
    message, adress = sock.recvfrom(1024)
    message = message.decode("ascii")
    message = int(message)
    return message

def udp_send(message):
    message = bytes(message, "utf-8")
    sock.sendto(message, (UDP_IP,UDP_PORT))

