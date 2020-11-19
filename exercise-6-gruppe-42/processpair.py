import os
import udp
import socket
from time import sleep


count = 0
is_master = 0

while True:
    try:
        count = udp.udp_listen()
    except socket.timeout:
        os.system('gnome-terminal -- python3 /home/petter/Documents/exercise-6-gruppe-42/processpair.py')
        is_master = 1

    while is_master:

        for i in range(10):
            udp.udp_send(str(count))
        count += 1
        print(count)
        sleep(1)
