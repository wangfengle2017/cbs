# BMS Simulation
 
import time

from threading import Thread
from comm.can_task import can_task

class bms(Thread):
    def __init__(self):
        pass

if __name__ == '__main__':

    received = False

    def data_handler(data):
        print("BMS received: " + str(data))
        global received
        received = True
    
    ct = can_task()
    ct.set_data_handler(data_handler) 
    ct.start()

    print("bms start ... ")

    while(True):
    
        # receive message from CAN bus
        if received == True:
            # send message to CAN bus
            msg = {}
            msg["can-id"] = 0x4211
            msg["dlc"] = 5
            msg["data"] = bytearray("world","ascii")
            msg["timestamp"] = time.time()  # current timestamp 
            ct.send_data(msg)
            print("BMS response: "+str(msg))
        else: 
            time.sleep(1)
            continue
        
        break
    
    time.sleep(3) 
    ct.stop()
    time.sleep(2)
    print("end")
    
