import fsm
import network
from ctypes import *
from ctypes.util import find_library
import config
import order
from threading import Thread, Lock
import time

elevator_driver = cdll.LoadLibrary("driver/driver.so")

def main():

    netw = network.Network(config.ELEV_ID)
    elev = fsm.Fsm()
    elevator_driver.elevator_hardware_init()
    elev.fsm_init()
    
    running_thread = Thread(target= elev.fsm_run, args=(netw.online_elevators,))
    network_receiver_thread = Thread(target= netw.msg_receive_handler, args=(elev,))
    network_sender_thread = Thread(target= netw.msg_send_handler, args=(elev,))
    
    running_thread.start()
    network_receiver_thread.start()
    network_sender_thread.start()

main()