# ElevatorProject

### Running several elevators with the simulator
- run simulator in one terminal and main.py in another.
- change ELEV_ID in config.py (starting ID is 0)
- change the last number of the port in simulator.con 
- change the port number in elevator_hardware.c (port has to be the same as above)
- run the compile command below
- now run a second simulator in a new terminal and main.py in another

**Command to compile elevator driver for running c code in python, must be run in the folder "driver":**\
gcc --std=gnu11 -shared -fPIC timer.c elevator_hardware.c -o driver.so /usr/local/lib/libcomedi.so

**if its not working, try:**
gcc --std=gnu11 -shared -fPIC timer.c elevator_hardware.c -o driver.so /usr/lib/libcomedi.so


### Test network issues:
**New command:**\
sudo iptables -A INPUT -p udp --dport 20000 -m statistic --mode random --probability 0.2 -j DROP\
sudo iptables -A INPUT -p udp --dport 20001 -m statistic --mode random --probability 0.2 -j DROP

**Old command:**\
sudo iptables -A INPUT -p tcp --dport 15657 -j ACCEPT\
sudo iptables -A INPUT -p tcp --sport 15657 -j ACCEPT\
sudo iptables -A INPUT -p tcp --dport 15658 -j ACCEPT\
sudo iptables -A INPUT -p tcp --sport 15658 -j ACCEPT

**Test disconnect:**\
sudo iptables -A INPUT -j DROP

**Test packet loss:**\
sudo iptables -A INPUT -m statistic --mode random --probability 0.2 -j DROP

**Flush after you're finished:**\
sudo iptables -F


## Libraries
we have used some handed out code:
- In the "driver" folder we have used the elevator_hardware files.
- In the "ProjectResources-master" folder we have used the handed out cost function code.



