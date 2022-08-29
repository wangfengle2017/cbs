import time
import json

from comm.can_task import can_task
from comm.mqtt_task import mqtt_task

response = False

def can_data_handler(data):
    global response 
    
    print(data)
    response = True

def can_test():
    global response

    ct = can_task()
    ct.set_data_handler(can_data_handler)
    ct.start()
     
    # send message to CAN bus
    msg = {}
    msg["can-id"] = 0x4200
    msg["dlc"] = 5
    msg["data"] = bytearray("hello","ascii")
    msg["timestamp"] = time.time()  # current timestamp
    ct.send_data(msg)

    while(True):

        if response==False:
            time.sleep(1)
            continue

        break
      
    time.sleep(2)
    ct.stop()
 
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    # client.subscribe("$SYS/#") 
    # client.subscribe("cbs/to-device")
    
def on_message(client, userdata, msg):
    
    global response 
     
    print(msg.topic+" "+str(msg.payload)) 
    print(type(msg.payload))

    response = True
    
def mqtt_test(): 
    mt = mqtt_task(client_id="gateway-mqtt-client")  
    mt.set_connect_handler(on_connect)
    mt.set_message_handler(on_message)
    mt.start()
    mt.subscribe("cbs/to-device/#")
    
    while(True):

        if response==True:
            # data="Hello, this is Device"
            msg = {}
            msg["can-id"] = 0x4211
            msg["dlc"] = 5
            msg["data"] = bytearray("world","ascii")
            msg["timestamp"] = time.time()  # current timestamp 
            mt.publish(title="cbs/from-device", data=str(msg))
            time.sleep(5)
            break
        else:    
            time.sleep(1)
            continue

    mt.stop() 


if __name__ == '__main__':
    pass