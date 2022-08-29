# cbs

## Prepare
Before demo, to start can-remote and mqtt broker

(1) can-remote

$ python -m can_remote --interface=virtual --channel=0 --bitrate=500000

defaut site: http://localhost:54701/
 
(2) mqtt-broker

start in verbose mode, defaut port 1884

$ cd \Program Files\mosquitto
$ mosquitto -v 

## Start Demo
BMS 
  - simualtion of BMS

Gateway 
  - CAN-to-MQTT gateway

IOT 
  -IOT platform simualtion

