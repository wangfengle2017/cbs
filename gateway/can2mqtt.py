# can-to-mqtt gateway

# from queue import SimpleQueue
 
import time


from comm.can_task import can_task
from comm.mqtt_task import mqtt_task
 
from testcode.test import can_test
from testcode.test import mqtt_test
 
class gateway:
    def __init__(self): 
        self._can = can_task()
        self._mqtt = mqtt_task()

        self._can.set_data_handler(self._mqtt.publish) 
        self._mqtt.set_message_handler(self._can.send_data)

        self._can.start() 
        self._mqtt.start()



def main():
    # instanciate can object
    # instanciate mqtt-client object
    # instanciate  gateway object with can and mqtt-client
    pass


if __name__ == '__main__':
 
    print("gateway start ...")
     
    # test can bus
    # can_test()
    
    # test mqtt
    # mqtt_test()

    # test message forward
    
      
    ct = can_task()

    mt = mqtt_task(client_id="gateway-mqtt-client")

    def can_data_handler(data):
        global mt
        print("CAN-Data-Handler: Publish - " + str(data))
        mt.publish(title="cbs/from-device", data=str(data))
     
    def mqtt_on_connect(client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
    
    def mqtt_on_message(client, userdata, msg):
        global ct
        print("MQTT-Client received: " + msg.topic+" "+str(msg.payload)) 
        print(type(msg.payload))

        # convert msg to dict
        data = eval(msg.payload.decode("utf-8"))
        ct.send_data(data)
    
    ct.set_data_handler(can_data_handler)
    ct.start()

    mt.set_connect_handler(mqtt_on_connect) 
    mt.set_message_handler(mqtt_on_message)
    mt.start()
    mt.subscribe("cbs/to-device/#")
 
    print("gateway to stop in 20 secs")  
    time.sleep(20)

    ct.stop()
    mt.stop() 
    print("end")
  