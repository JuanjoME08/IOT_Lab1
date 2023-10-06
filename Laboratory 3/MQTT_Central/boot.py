
import bluetooth
import random
import struct
import time
import sys
from machine import deepsleep
from machine import Pin
from machine import reset
from simpleBLE import BLECentral 
from time import sleep_ms
import network
from mqtt import MQTTClient 
import json
from micropython import const


def do_connect():
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('iPhone', 'juanjo0812')
        #sta_if.connect('Redmi Note 12', 'andres123')
        #sta_if.connect('Redmi Note 9', 'holabb123')
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())

do_connect()


# This example finds and connects to a BLE temperature sensor (e.g. the one in ble_temperature.py).



# Bluetooth object
ble = bluetooth.BLE()

# Environmental service
service="683aa995-81a3-4be4-8456-6bebe973101c" 

# Temperature characteristic
characteristic="74a2a6e4-3ce3-4b5f-929a-a95f216d2525"

# BLE Central object
central = BLECentral(ble,service,characteristic)

done_flag=False
BUTTON=0
button_pin = Pin(BUTTON, Pin.IN)

USERNAME = const('BzcaBSYDCgcvHDIiMgM4ISs')
CLIENTID = const('BzcaBSYDCgcvHDIiMgM4ISs')
PASS = const('Jo3RpjkZVicN+2x3bZi8ajRq')
SERVER=const('mqtt3.thingspeak.com')
CHANNEL=const('2283267')


client = MQTTClient(client_id=CLIENTID, server=SERVER,user=CLIENTID,password=PASS)
client.connect()

def showData(data):
    global done_flag
    print(data)
    msg='field1='+str(data)
    print(msg)
    client.publish(topic="channels/"+CHANNEL+"/publish", msg=msg)   
    client.check_msg();
    done_flag=True
    sleep_ms(500)
    if button_pin.value()==1:
        deepsleep(15000)
        
def on_scan(addr_type, addr, name):
    global not_found
    if addr_type is not None:
        print("Found sensor:", addr_type, addr, name)
        central.connect()
    else:
        print("No sensor found.")

central.scan(callback=on_scan)

# Wait for connection...
attempts=0
while True:
    time.sleep_ms(100)
    if central.is_connected():
        break;
    else:
        attempts=attempts+1
        if attempts==100:
            reset()
            
    
print("Connected")

central.on_notify(callback= lambda data :print('Notified'))

# Explicitly issue reads, using "print" as the callback.


central.read(callback=lambda data: showData(data[0]/3600000))
while not done_flag:
    pass
# Alternative to the above, just show the most recently notified value.
# while central.is_connected():
#     print(central.value())
#     time.sleep_ms(2000)




