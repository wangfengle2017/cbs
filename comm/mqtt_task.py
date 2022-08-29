from threading import Thread
import paho.mqtt.client as mqtt

#
# task of mqtt client         
#
# The callback for when the client receives a CONNACK response from the server.
def default_on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
  
# The callback for when a PUBLISH message is received from the server.
def default_on_message(client, userdata, msg):
     print(msg.topic+" "+str(msg.payload))
 
class mqtt_task(Thread):
    
    def __init__(self, client_id="mqtt-client"):
        self._client_id = client_id
        self._client =  mqtt.Client(client_id=client_id)
        self._client.on_connect = default_on_connect 
        self._client.on_message = default_on_message
        self._stopped =True
        super().__init__()

    def set_connect_handler(self, handler=default_on_connect):
        # print("set connect handler")
        self._client.on_connect = handler 
         
    def set_message_handler(self, handler=default_on_message):
        # print("set message handler")
        self._client.on_message = handler

    def start(self):
        # connect to mqtt broker
        self._stopped = False
        # The broker is 'localhost:1883' and keepalive is 180 sec
        self._client.connect("localhost", 1883, 180)
        # start thread
        super().start() 
  
    def stop(self):
        if self._stopped == False:
            self._client.disconnect()
            self._stopped = True
    
    # subcriber topics 
    def subscribe(self, topic):
        self._client.subscribe(topic)
     
    def publish(self, title, data):
        # publish data
        # print("publish: "+ title + " " + data)
        self._client.publish(title, data)
         
    def run(self):
        print(self._client_id + " start ...")
        self._client.loop_forever()
        print(self._client_id + " is stoped")
