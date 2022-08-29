# IoT platform

from glob import glob
import time
import json

from threading import Thread
from comm.mqtt_task import mqtt_task


class iot(Thread):
    def __init__(self):
        pass


if __name__ == '__main__':

    received = False

    def on_connect(client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        # client.subscribe("$SYS/#") 
        # client.subscribe("cbs/from-device/#")

    def on_message(client, userdata, msg):
        
        global received 
         
        print("IoT received: "+msg.topic+" "+str(msg.payload)) 
        received = True
        
  
    print("IoT start ...")
 
    mt = mqtt_task(client_id="IoT-mqtt-client") 
    mt.set_connect_handler(on_connect)
    mt.set_message_handler(on_message) 
    mt.start()
    mt.subscribe("cbs/from-device/#")
    
    # publish 
    # mt.publish(title="cbs/to-device", data="Hello, this is IoT")

    msg = {}
    msg["can-id"] = 0x4200
    msg["dlc"] = 5
    msg["data"] = bytearray("hello","ascii")
    msg["timestamp"] = time.time()  # current timestamp
 
    print("IoT Published: cbs/to-device "+str(msg))
    mt.publish(title="cbs/to-device", data=str(msg))     
 
    time.sleep(10)
    
    ''' 
    while(True):
    
        if received==True:
            time.sleep(5)
            break 
        else:    
            time.sleep(1)
            continue
    '''

    mt.stop()     
    time.sleep(5)
    print("end")
    
