from ctypes import *
from ctypes.util import find_library
import json
import config
import subprocess

elevator_driver = cdll.LoadLibrary("driver/driver.so")



class MyEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__

class Order:

    def __init__(self, floor, order_type, order_set):
        self.floor = floor
        self.order_type = order_type
        self.order_set = order_set
        self.ELEV_ID = config.ELEV_ID
    

class OrderMatrix():
    m_order_matrix = []
    
    for i in range(config.N_FLOORS):
        m_order_matrix.append([])
        for j in range(config.N_ELEVATORS):
            order = Order(i,-1, 0)
            m_order_matrix[i].append(order)

    def order_change_type(self, order, id):
        if(OrderMatrix.m_order_matrix[order.floor][id].order_set == 1 and OrderMatrix.m_order_matrix[order.floor][id].order_type != order.order_type):
            if(OrderMatrix.m_order_matrix[order.floor][id].order_type == config.BUTTON_COMMAND):
                if(order.order_type == config.BUTTON_CALL_DOWN):
                    order.order_type = config.BUTTON_IN_DOWN
                elif(order.order_type == config.BUTTON_CALL_UP):
                    order.order_type = config.BUTTON_IN_UP

            elif(OrderMatrix.m_order_matrix[order.floor][id].order_type == config.BUTTON_CALL_DOWN):
                if(order.order_type == config.BUTTON_COMMAND):
                    order.order_type = config.BUTTON_IN_DOWN
                elif(order.order_type == config.BUTTON_CALL_UP):
                    order.order_type = config.BUTTON_UP_DOWN

            elif(OrderMatrix.m_order_matrix[order.floor][id].order_type == config.BUTTON_CALL_UP):
                if(order.order_type == config.BUTTON_COMMAND):
                    order.order_type = config.BUTTON_IN_UP
                elif(order.order_type == config.BUTTON_CALL_DOWN):
                    order.order_type = config.BUTTON_UP_DOWN

            elif(OrderMatrix.m_order_matrix[order.floor][id].order_type == config.BUTTON_IN_DOWN):
                if(order.order_type == config.BUTTON_CALL_UP):
                    order.order_type = config.BUTTON_MULTI
            
            elif(OrderMatrix.m_order_matrix[order.floor][id].order_type == config.BUTTON_IN_UP):
                if(order.order_type == config.BUTTON_CALL_DOWN):
                    order.order_type = config.BUTTON_MULTI
                
            elif(OrderMatrix.m_order_matrix[order.floor][id].order_type == config.BUTTON_UP_DOWN):
                if(order.order_type == config.BUTTON_COMMAND):
                    order.order_type = config.BUTTON_MULTI
        return order

    def order_add(self, order, pos_matrix):
        if(order.order_type == config.BUTTON_COMMAND):
            order = self.order_change_type(order,config.ELEV_ID)
            order.order_set = 1
            config.order_matrix_lock.acquire()
            OrderMatrix.m_order_matrix[order.floor][config.ELEV_ID] = order
            config.order_matrix_lock.release()
        else:
            elev_id = self.order_designate_elevator(pos_matrix, order)
            order = self.order_change_type(order,elev_id)
            order.order_set = 1
            config.order_matrix_lock.acquire()
            OrderMatrix.m_order_matrix[order.floor][elev_id] = order
            config.order_matrix_lock.release()

    def order_poll_buttons(self, pos_matrix, online_elevators, order_is_received):
        if(order_is_received == 0):
            order = Order(-1,-1, -1)
            for i in range(config.N_FLOORS):
                if(elevator_driver.elevator_hardware_get_button_signal(config.BUTTON_COMMAND, i)):
                    order_is_received = 1
                    order.floor = i
                    order.order_type = config.BUTTON_COMMAND
                    self.order_add(order, pos_matrix)
                    return order_is_received

                if(elevator_driver.elevator_hardware_get_button_signal(config.BUTTON_CALL_DOWN, i)):
                    if(sum(online_elevators) <= 1 or online_elevators[config.ELEV_ID] == 0):
                        return    
                    order_is_received = 1
                    order.floor = i
                    order.order_type = config.BUTTON_CALL_DOWN
                    self.order_add(order, pos_matrix)
                    return order_is_received
                if(elevator_driver.elevator_hardware_get_button_signal(config.BUTTON_CALL_UP, i)):
                    if(sum(online_elevators) <= 1 or online_elevators[config.ELEV_ID] == 0):
                        return    
                    order_is_received = 1
                    order.floor = i
                    order.order_type = config.BUTTON_CALL_UP
                    self.order_add(order, pos_matrix)
                    return order_is_received
        return order_is_received
    
    def order_designate_elevator(self, pos_matrix, order):
        cab_req_elev_0 = [False, False, False, False]
        cab_req_elev_1 = [False, False, False, False]
        hall_req = [[False,False],[False,False],[False,False],[False,False]]
        position_elev_0 = 0
        position_elev_1 = 0
        direction_elev_0 = "stop"
        direction_elev_1 = "stop"
        behaviour_elev_0 = "idle"
        behaviour_elev_1 = "idle"

        for i in range(config.N_FLOORS):
            if(OrderMatrix.m_order_matrix[i][0].order_set == 1):
                behaviour_elev_0 = "moving"
            if(OrderMatrix.m_order_matrix[i][1].order_set == 1):
                behaviour_elev_1 = "moving"


        if(order.order_type == config.BUTTON_CALL_UP):
            hall_req[order.floor][0] = True
        
        elif(order.order_type == config.BUTTON_CALL_DOWN):
            hall_req[order.floor][1] = True

        for i in range(config.N_FLOORS):
            if(pos_matrix[i][0] == 1):
                position_elev_0 = i
            if(pos_matrix[i][1] == 1):
                position_elev_1 = i

            if(OrderMatrix.m_order_matrix[i][0].order_set == 1 and (OrderMatrix.m_order_matrix[i][0].order_type == config.BUTTON_COMMAND or OrderMatrix.m_order_matrix[i][0].order_type == config.BUTTON_MULTI)):
                cab_req_elev_0[i] = True
            if(OrderMatrix.m_order_matrix[i][1].order_set == 1 and (OrderMatrix.m_order_matrix[i][1].order_type == config.BUTTON_COMMAND or OrderMatrix.m_order_matrix[i][1].order_type == config.BUTTON_MULTI)):
                cab_req_elev_1[i] = True


        if(pos_matrix[config.N_FLOORS][0] == -1):
            direction_elev_0 = "down"
        elif(pos_matrix[config.N_FLOORS][0] == 1):
            direction_elev_0 = "up"
        else:
            direction_elev_0 = "stop"
        
        if(pos_matrix[config.N_FLOORS][1] == -1):
            direction_elev_1 = "down"
        elif(pos_matrix[config.N_FLOORS][1] == 1):
            direction_elev_1 = "stop"
        else:
            direction_elev_1 = "stop"

        input = {
            "hallRequests" : hall_req,
            "states" : {
                "zero" : {
                    "behaviour" : behaviour_elev_0,
                    "floor" : position_elev_0,
                    "direction" : direction_elev_0,
                    "cabRequests" : cab_req_elev_0
                },
                "one" : {
                    "behaviour": behaviour_elev_1,
                    "floor" : position_elev_1,
                    "direction" : direction_elev_1,
                    "cabRequests" : cab_req_elev_1  
                }
            }
        }

        json_packet = json.dumps(input)
        json_packet = bytes(json_packet, "ascii")
        process = subprocess.run(["./ProjectResources-master/cost_fns/hall_request_assigner/hall_request_assigner", "--input", json_packet], check=True, stdout=subprocess.PIPE, universal_newlines=True)
        output = process.stdout
        output = json.loads(output)
        
        for i in range(config.N_FLOORS):
            for j in range(2):
                if(output["zero"][i][j] == True):
                    return 0
                if(output["one"][i][j] == True):
                    return 1


    def order_clear_floor(self, floor):
        OrderMatrix.m_order_matrix[floor][config.ELEV_ID].order_set = 0
        
    def order_clear_all(self):
        for i in range(config.N_FLOORS):
            for k in range(config.N_ELEVATORS):
                for j in range(config.N_BUTTONS):
                    OrderMatrix.m_order_matrix[i][k].order_set = 0
                    elevator_driver.elevator_hardware_set_button_lamp(j,i,0)
        
    def order_is_set(self, floor):
        for i in range(config.N_ELEVATORS):
            if(OrderMatrix.m_order_matrix[floor][i].order_set == 1):
                return 1
        return 0


    def order_exists(self, id):
        for i in range(config.N_FLOORS):
            if(OrderMatrix.m_order_matrix[i][id].order_set == 1):
                return 1
        return 0
    
    def order_json_encode_order_matrix(self):
        json_packet = json.dumps(OrderMatrix.m_order_matrix, cls=MyEncoder)
        return json_packet

    def order_json_decode_order_matrix(self, json_packet):
        json_packet = json.JSONDecoder().decode(json_packet)
        order_matrix = []
        for i in range(config.N_FLOORS):
            order_matrix.append([])
            for j in range(config.N_ELEVATORS):
                floor = json_packet[i][j]["floor"]
                order_type = json_packet[i][j]["order_type"]
                order_set = json_packet[i][j]["order_set"]
                order = Order(floor,order_type, order_set)
                order_matrix[i].append(order)
        return order_matrix
    
    def order_json_encode_position_matrix(self, pos_matrix):
        return json.dumps(pos_matrix)

    def order_json_decode_position_matrix(self, json_pos_matrix):
        json_packet = json.JSONDecoder().decode(json_pos_matrix)
        m_position_matrix = []
        for i in range(config.N_FLOORS + 1):
            m_position_matrix.append([])
            for j in range(config.N_ELEVATORS):
                m_position_matrix[i].append(json_packet[i][j])

        return m_position_matrix
            

    def order_get_top(self, floor):
        order = OrderMatrix.m_order_matrix[config.N_FLOORS-1][config.ELEV_ID]

        for i in range(floor, config.N_FLOORS):
            for j in range(config.N_BUTTONS):
                if(OrderMatrix.m_order_matrix[i][config.ELEV_ID].order_set == 1):
                    order = OrderMatrix.m_order_matrix[i][config.ELEV_ID]
        return order
    
    def order_get_bottom(self, floor):
        order = OrderMatrix.m_order_matrix[0][config.ELEV_ID]

        for i in range(floor,-1,-1):
            for j in range(config.N_BUTTONS):
                if(OrderMatrix.m_order_matrix[i][config.ELEV_ID].order_set == 1):
                    order = OrderMatrix.m_order_matrix[i][config.ELEV_ID]
        return order

    def order_stop_at_floor(self, direction, current_floor):
        
        if(direction == config.DIRN_DOWN):
            if(OrderMatrix.m_order_matrix[current_floor][config.ELEV_ID].order_set == 1 and (OrderMatrix.m_order_matrix[current_floor][config.ELEV_ID].order_type == config.BUTTON_CALL_DOWN or OrderMatrix.m_order_matrix[current_floor][config.ELEV_ID].order_type == config.BUTTON_MULTI)):
                return 1
            elif(OrderMatrix.m_order_matrix[current_floor][config.ELEV_ID].order_set == 1 and OrderMatrix.m_order_matrix[current_floor][config.ELEV_ID].order_type == config.BUTTON_IN_DOWN):
                return 1
            elif(OrderMatrix.m_order_matrix[current_floor][config.ELEV_ID].order_set == 1 and OrderMatrix.m_order_matrix[current_floor][config.ELEV_ID].order_type == config.BUTTON_UP_DOWN):
                return 1    
            elif(OrderMatrix.m_order_matrix[current_floor][config.ELEV_ID].order_set == 1 and OrderMatrix.m_order_matrix[current_floor][config.ELEV_ID].order_type == config.BUTTON_COMMAND):
                return 1
            elif(self.order_get_bottom(current_floor).floor == current_floor and self.order_get_bottom(current_floor).order_set == 1):
                return 1
            elif( current_floor == 0):
                return 1
        
        elif(direction == config.DIRN_UP):
            
            if(OrderMatrix.m_order_matrix[current_floor][config.ELEV_ID].order_set == 1 and (OrderMatrix.m_order_matrix[current_floor][config.ELEV_ID].order_type == config.BUTTON_CALL_UP or OrderMatrix.m_order_matrix[current_floor][config.ELEV_ID].order_type == config.BUTTON_MULTI)):
                return 1
            elif(OrderMatrix.m_order_matrix[current_floor][config.ELEV_ID].order_set == 1 and OrderMatrix.m_order_matrix[current_floor][config.ELEV_ID].order_type == config.BUTTON_IN_UP):
                return 1
            elif(OrderMatrix.m_order_matrix[current_floor][config.ELEV_ID].order_set == 1 and OrderMatrix.m_order_matrix[current_floor][config.ELEV_ID].order_type == config.BUTTON_UP_DOWN):
                return 1
            elif(OrderMatrix.m_order_matrix[current_floor][config.ELEV_ID].order_set == 1 and OrderMatrix.m_order_matrix[current_floor][config.ELEV_ID].order_type == config.BUTTON_COMMAND):
                return 1
            elif(self.order_get_top(current_floor).floor == current_floor and self.order_get_top(current_floor).order_set == 1):
                return 1
            elif(current_floor == config.N_FLOORS-1):
                return 1
        
        return 0

    def order_continue(self, direction, current_floor):
        if(direction == config.DIRN_DOWN):
            if(self.order_get_bottom(current_floor).order_set == 1 and self.order_get_bottom(current_floor).floor < current_floor):
                return 1
        
        elif(direction == config.DIRN_UP):
            if(self.order_get_top(current_floor).order_set == 1 and self.order_get_top(current_floor).floor > current_floor):
                return 1

    def order_reassign_order(self, id):
        other_elev = ( id + 1 ) % 2
        for i in range(config.N_FLOORS):
            if(OrderMatrix.m_order_matrix[i][id].order_set == 1 and OrderMatrix.m_order_matrix[i][id].order_type != config.BUTTON_COMMAND):

                if(OrderMatrix.m_order_matrix[i][id].order_type == config.BUTTON_IN_DOWN):
                    if(OrderMatrix.m_order_matrix[i][other_elev].order_set == 1):
                        OrderMatrix.m_order_matrix[i][other_elev].order_type = config.BUTTON_IN_DOWN
                    else: 
                        OrderMatrix.m_order_matrix[i][other_elev].order_type = config.BUTTON_CALL_DOWN

                    OrderMatrix.m_order_matrix[i][id].order_type = config.BUTTON_COMMAND
                
                elif(OrderMatrix.m_order_matrix[i][id].order_type == config.BUTTON_IN_UP):
                    if(OrderMatrix.m_order_matrix[i][other_elev].order_set == 1):
                        OrderMatrix.m_order_matrix[i][other_elev].order_type = config.BUTTON_IN_UP
                    else: 
                        OrderMatrix.m_order_matrix[i][other_elev].order_type = config.BUTTON_CALL_UP
                    OrderMatrix.m_order_matrix[i][id].order_type = config.BUTTON_COMMAND

                elif(OrderMatrix.m_order_matrix[i][id].order_type == config.BUTTON_MULTI):
                    if(OrderMatrix.m_order_matrix[i][other_elev].order_set == 1):
                        OrderMatrix.m_order_matrix[i][other_elev].order_type = config.BUTTON_MULTI
                    else: 
                        OrderMatrix.m_order_matrix[i][other_elev].order_type = config.BUTTON_UP_DOWN
                    OrderMatrix.m_order_matrix[i][id].order_type = config.BUTTON_COMMAND
                
                elif(OrderMatrix.m_order_matrix[i][id].order_type == config.BUTTON_CALL_DOWN):
                    if(OrderMatrix.m_order_matrix[i][other_elev].order_set == 1):
                        OrderMatrix.m_order_matrix[i][other_elev].order_type = config.BUTTON_IN_DOWN
                    else:
                        OrderMatrix.m_order_matrix[i][other_elev].order_type = OrderMatrix.m_order_matrix[i][id].order_type
                    OrderMatrix.m_order_matrix[i][id].order_set = 0

                elif(OrderMatrix.m_order_matrix[i][id].order_type == config.BUTTON_CALL_UP):
                    if(OrderMatrix.m_order_matrix[i][other_elev].order_set == 1):
                        OrderMatrix.m_order_matrix[i][other_elev].order_type = config.BUTTON_IN_UP
                    else:
                        OrderMatrix.m_order_matrix[i][other_elev].order_type = OrderMatrix.m_order_matrix[i][id].order_type
                    OrderMatrix.m_order_matrix[i][id].order_set = 0
                
                elif(OrderMatrix.m_order_matrix[i][id].order_type == config.BUTTON_UP_DOWN):
                    if(OrderMatrix.m_order_matrix[i][other_elev].order_set == 1):
                        OrderMatrix.m_order_matrix[i][other_elev].order_type = config.BUTTON_MULTI
                    else: 
                        OrderMatrix.m_order_matrix[i][other_elev].order_type = config.BUTTON_UP_DOWN
                    OrderMatrix.m_order_matrix[i][id].order_set = 0

                OrderMatrix.m_order_matrix[i][other_elev].order_set = 1

    def order_light_control(self):
        for j in range (config.N_FLOORS):
                other_elev = ( config.ELEV_ID + 1 ) % 2
                if(OrderMatrix.m_order_matrix[j][config.ELEV_ID].order_set == 1):

                    if(OrderMatrix.m_order_matrix[j][config.ELEV_ID].order_type == config.BUTTON_IN_DOWN):
                        elevator_driver.elevator_hardware_set_button_lamp(config.BUTTON_CALL_DOWN,j,1)
                        elevator_driver.elevator_hardware_set_button_lamp(config.BUTTON_COMMAND,j,1)
                        if(OrderMatrix.m_order_matrix[j][other_elev].order_set != 1):
                            elevator_driver.elevator_hardware_set_button_lamp(config.BUTTON_CALL_UP,j,0)
                    
                    elif(OrderMatrix.m_order_matrix[j][config.ELEV_ID].order_type == config.BUTTON_IN_UP):
                        elevator_driver.elevator_hardware_set_button_lamp(config.BUTTON_CALL_UP,j,1)
                        elevator_driver.elevator_hardware_set_button_lamp(config.BUTTON_COMMAND,j,1)
                        if(OrderMatrix.m_order_matrix[j][other_elev].order_set != 1):
                            elevator_driver.elevator_hardware_set_button_lamp(config.BUTTON_CALL_DOWN,j,0)
                    
                    elif(OrderMatrix.m_order_matrix[j][config.ELEV_ID].order_type == config.BUTTON_UP_DOWN):
                        elevator_driver.elevator_hardware_set_button_lamp(config.BUTTON_CALL_DOWN,j,1)
                        elevator_driver.elevator_hardware_set_button_lamp(config.BUTTON_CALL_UP,j,1)
                        if(OrderMatrix.m_order_matrix[j][other_elev].order_set != 1):
                            elevator_driver.elevator_hardware_set_button_lamp(config.BUTTON_COMMAND,j,0)
                    
                    elif(OrderMatrix.m_order_matrix[j][config.ELEV_ID].order_type == config.BUTTON_MULTI):
                        elevator_driver.elevator_hardware_set_button_lamp(config.BUTTON_COMMAND,j,1)
                        elevator_driver.elevator_hardware_set_button_lamp(config.BUTTON_CALL_DOWN,j,1)
                        elevator_driver.elevator_hardware_set_button_lamp(config.BUTTON_CALL_UP,j,1)

                    elif(OrderMatrix.m_order_matrix[j][config.ELEV_ID].order_type == config.BUTTON_CALL_UP):
                        if(OrderMatrix.m_order_matrix[j][other_elev].order_set != 1):
                            elevator_driver.elevator_hardware_set_button_lamp(config.BUTTON_COMMAND,j,0)
                            elevator_driver.elevator_hardware_set_button_lamp(config.BUTTON_CALL_DOWN,j,0)
                        elevator_driver.elevator_hardware_set_button_lamp(config.BUTTON_CALL_UP,j,1)
                    
                    elif(OrderMatrix.m_order_matrix[j][config.ELEV_ID].order_type == config.BUTTON_CALL_DOWN):
                        
                        elevator_driver.elevator_hardware_set_button_lamp(config.BUTTON_CALL_DOWN,j,1)
                        if(OrderMatrix.m_order_matrix[j][other_elev].order_set != 1):
                            elevator_driver.elevator_hardware_set_button_lamp(config.BUTTON_CALL_UP,j,0)
                            elevator_driver.elevator_hardware_set_button_lamp(config.BUTTON_COMMAND,j,0)
                    
                    elif(OrderMatrix.m_order_matrix[j][config.ELEV_ID].order_type == config.BUTTON_COMMAND):
                        elevator_driver.elevator_hardware_set_button_lamp(config.BUTTON_COMMAND,j,1)
                        if(OrderMatrix.m_order_matrix[j][other_elev].order_set != 1):
                            elevator_driver.elevator_hardware_set_button_lamp(config.BUTTON_CALL_DOWN,j,0)
                            elevator_driver.elevator_hardware_set_button_lamp(config.BUTTON_CALL_UP,j,0)
                    

                if(OrderMatrix.m_order_matrix[j][other_elev].order_set == 1):
                    if(OrderMatrix.m_order_matrix[j][other_elev].order_type == config.BUTTON_IN_DOWN):
                        elevator_driver.elevator_hardware_set_button_lamp(config.BUTTON_CALL_DOWN,j,1)
                        if(OrderMatrix.m_order_matrix[j][config.ELEV_ID].order_set != 1):
                            elevator_driver.elevator_hardware_set_button_lamp(config.BUTTON_CALL_UP,j,0)
                    
                    elif(OrderMatrix.m_order_matrix[j][other_elev].order_type == config.BUTTON_IN_UP):
                        if(OrderMatrix.m_order_matrix[j][config.ELEV_ID].order_set != 1):
                            elevator_driver.elevator_hardware_set_button_lamp(config.BUTTON_CALL_DOWN,j,0)
                        elevator_driver.elevator_hardware_set_button_lamp(config.BUTTON_CALL_UP,j,1)
                    
                    elif(OrderMatrix.m_order_matrix[j][other_elev].order_type == config.BUTTON_UP_DOWN):
                        elevator_driver.elevator_hardware_set_button_lamp(config.BUTTON_CALL_DOWN,j,1)
                        elevator_driver.elevator_hardware_set_button_lamp(config.BUTTON_CALL_UP,j,1)
                    
                    elif(OrderMatrix.m_order_matrix[j][other_elev].order_type == config.BUTTON_MULTI):
                        elevator_driver.elevator_hardware_set_button_lamp(config.BUTTON_CALL_DOWN,j,1)
                        elevator_driver.elevator_hardware_set_button_lamp(config.BUTTON_CALL_UP,j,1)
                    
                    elif(OrderMatrix.m_order_matrix[j][other_elev].order_type == config.BUTTON_CALL_UP):
                        if(OrderMatrix.m_order_matrix[j][config.ELEV_ID].order_set != 1):
                            elevator_driver.elevator_hardware_set_button_lamp(config.BUTTON_CALL_DOWN,j,0)
                        elevator_driver.elevator_hardware_set_button_lamp(config.BUTTON_CALL_UP,j,1)
                    
                    elif(OrderMatrix.m_order_matrix[j][other_elev].order_type == config.BUTTON_CALL_DOWN):
                        elevator_driver.elevator_hardware_set_button_lamp(config.BUTTON_CALL_DOWN,j,1)
                        if(OrderMatrix.m_order_matrix[j][config.ELEV_ID].order_set != 1):
                            elevator_driver.elevator_hardware_set_button_lamp(config.BUTTON_CALL_UP,j,0)

                    elif(OrderMatrix.m_order_matrix[j][other_elev].order_type == config.BUTTON_COMMAND):
                        if(OrderMatrix.m_order_matrix[j][config.ELEV_ID].order_set != 1):
                            elevator_driver.elevator_hardware_set_button_lamp(config.BUTTON_CALL_DOWN,j,0)
                            elevator_driver.elevator_hardware_set_button_lamp(config.BUTTON_CALL_UP,j,0)

                if(OrderMatrix.m_order_matrix[j][other_elev].order_set == 0 and OrderMatrix.m_order_matrix[j][config.ELEV_ID].order_set == 0):
                    for i in range(3):
                        elevator_driver.elevator_hardware_set_button_lamp(i,j,0)
                
                elif(OrderMatrix.m_order_matrix[j][config.ELEV_ID].order_set == 0):
                    elevator_driver.elevator_hardware_set_button_lamp(2,j,0)
                
