import socket
import config
from ctypes import *
from ctypes.util import find_library
from threading import Thread
import fsm
import order
import time

elevator_driver = cdll.LoadLibrary("driver/driver.so")

class Network:

    online_elevators = [0]*config.N_ELEVATORS

    def __init__(self, ID): 

        try:
            
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            
        except:
            pass 

        self.ID = ID
        self.sock.settimeout(1.5)

        Network.online_elevators[ID] = 1
            

    def UDP_broadcast(self, json_packet, IP_address, port, elevator):

        try:
            for i in range(10):
                self.sock.sendto(json_packet, (IP_address,port))
            Network.online_elevators[config.ELEV_ID] = 1

        except socket.timeout:
            Network.online_elevators[config.ELEV_ID] = 0


    def UDP_listen(self, port):

        try:
            self.sock.bind(("", port))

        except:
            pass

        try:
            json_packet, address = self.sock.recvfrom(1024)
            json_packet = json_packet.decode(encoding="ascii")
            return json_packet, address

        except socket.timeout:
            return port

        
    def msg_receive_handler(self, elevator):
        
        while True:
            
            for i in range(config.N_ELEVATORS):
                if(i != config.ELEV_ID):
                    msg = self.UDP_listen(config.BASE_ELEVATOR_PORT+i)
                    if(isinstance(msg, int) == 0):
                        Network.online_elevators[i] = 1
                        if(msg[0] != "alive"):
                            try: 
                                position_matrix = elevator.queue.order_json_decode_position_matrix(msg[0])
                                for j in range (config.N_FLOORS + 1):
                                    elevator.m_position_matrix[j][i] = position_matrix[j][i]

                            except:
                                pass

                            config.order_matrix_lock.acquire()

                            try: 
                                order_matrix = elevator.queue.order_json_decode_order_matrix(msg[0])
                                
                                for k in range(config.N_ELEVATORS):
                                    for j in range (config.N_FLOORS):
                                        elevator.queue.m_order_matrix[j][k] = order_matrix[j][k]
                            
                            except:
                                pass

                            config.order_matrix_lock.release()
                            
                    else:
                        Network.online_elevators[msg-config.BASE_ELEVATOR_PORT] = 0

    def msg_send_handler(self, elevator):

        timer_start = time.time()
        other_elev = ( config.ELEV_ID + 1 ) % 2
        while True:
            
            if(Network.online_elevators[other_elev] == 1 and elevator.m_position_matrix[0][other_elev] == 1 and elevator.queue.order_exists(other_elev) == 1):
                config.order_matrix_lock.acquire()
                self.UDP_broadcast(bytes(elevator.queue.order_json_encode_order_matrix(), "ascii"), "", config.BASE_ELEVATOR_PORT+config.ELEV_ID, elevator)
                config.order_matrix_lock.release()

            if(time.time()-timer_start >= 3):
                self.UDP_broadcast(bytes("alive", "ascii"), "", config.BASE_ELEVATOR_PORT+config.ELEV_ID, elevator)
                timer_start = time.time()

            if(elevator.order_is_received == 1 or elevator.m_next_state == config.DOOR_OPEN):
                config.order_matrix_lock.acquire()
                self.UDP_broadcast(bytes(elevator.queue.order_json_encode_order_matrix(), "ascii"), "", config.BASE_ELEVATOR_PORT+config.ELEV_ID, elevator)
                config.order_matrix_lock.release()
                
            if(elevator.fsm_get_current_floor() != -1): 
                self.UDP_broadcast(bytes(elevator.queue.order_json_encode_position_matrix(elevator.m_position_matrix), "ascii"), "", config.BASE_ELEVATOR_PORT+config.ELEV_ID, elevator)
