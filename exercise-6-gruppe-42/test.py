import os
import udp
from multiprocessing import Process
import socket
from time import sleep


def test_listen():
    count = 0
    print("halla fra listen")
    #p1 = Process(target=udp.udp_listen)
    #p1.start()
    #p2.start()
    # p1.join(timeout=5)
    # p1.terminate()
    # print(p1.is_alive())

    while True:
        #p1.join(timeout=5)
        print(udp.udp_listen())
        #count = p1.exitcode
        #print("listen", count)

def test():
    sleep(1)
    os.system('gnome-terminal -- python3 /home/petter/Documents/exercise-6-gruppe-42/petter/test.py')
    #os.system('gnome-terminal -x date')
    sleep(1)


test_listen()