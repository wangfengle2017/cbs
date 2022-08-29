from threading import Thread
import time
import can

#
# Wrapper to python-can and python=-can-remote
#

class can_adapter():
    def __init__(self, channel="ws://localhost:54701/"):
        # initialize CAN bus
        self._channel = channel
        self._connected = False
        self._extended = False
        self._bus = None 
         
    def connect(self):
        if self._bus is None:
            self._bus = can.Bus(channel=self._channel, bustype='remote', bitrate=500000)
       
    def is_connected(self):
        return True if self._bus else False
              
    def recv(self, timeout=None):
        if self._bus :
            msg = self._bus.recv(timeout=timeout)            
            if msg:
                # print(msg)
                # convert can message object to data 
                data = {}        
                data["can-id"] = msg.arbitration_id
                data["dlc"] =msg.dlc
                data["data"] = msg.data
                data["timestamp"] = msg.timestamp
                return data 
        return None 
     
    def send(self, data):
        if self._bus :
            #  compose can message from data
            arbitration_id= data["can-id"]
            timestamp = data["timestamp"]
            dlc = data["dlc"]
            msg = can.Message(arbitration_id=arbitration_id, dlc=dlc, timestamp=timestamp, data=list(data["data"]), is_extended_id=self._extended) 
            self._bus.send(msg)

    def shutdown(self):
        self._bus.shutdown()
        self._connected = False
        self._bus = None

#
# task of CAN  
# 
class can_task(Thread):
    def __init__(self, handler=None):
        self._data_handler = handler
        self._stopped = True
        self._can = can_adapter()
        self._timeout = 1
        super().__init__()
                  
    def set_data_handler(self, handler=None):
        self._data_handler = handler
         
    def start(self):
        self._stopped = False
        self._can.connect()
        super().start()
          
    def stop(self):
        if not self._stopped:
            self._stopped = True
    
    def is_connected(self):
        return self._can.is_connected()

    def send_data(self, data):
        # compose message from content
        # send message to CAN bus
        self._can.send(data)
   
    def run(self):
        while(True):
            # read CAN bus
            data = self._can.recv(timeout=self._timeout)

            if data:
                # to handle data
                self._data_handler(data)

            if self._stopped:
                self._can.shutdown()
                time.sleep(1)
                # print("can task terminate")
                break
