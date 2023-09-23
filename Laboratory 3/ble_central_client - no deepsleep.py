# This example finds and connects to a BLE temperature sensor (e.g. the one in ble_temperature.py).
import bluetooth
import random
import struct
import time
import sys
from machine import deepsleep, Pin
from simpleBLE import BLECentral 

# Bluetooth object
ble = bluetooth.BLE()

# Environmental service
service="683aa995-81a3-4be4-8456-6bebe973101c" 

# Temperature characteristic
characteristic="74a2a6e4-3ce3-4b5f-929a-a95f216d2525"

# BLE Central object
central = BLECentral(ble,service,characteristic)

not_found = False


def on_scan(addr_type, addr, name):
    if addr_type is not None:
        print("Found sensor:", addr_type, addr, name)
        central.connect()
    else:
        global not_found
        not_found = True
        print("No sensor found.")

central.scan(callback=on_scan)

# Wait for connection...
while not central.is_connected():
    time.sleep_ms(100)
    if not_found:
        sys.exit()

print("Connected")

central.on_notify(callback= lambda data :print('Notified') )

# Explicitly issue reads, using "print" as the callback.
while central.is_connected():
    central.read(callback=lambda data: print('Accumulate:', abs(data[0]/3600000), "kWh"))
    time.sleep(1)

print("Disconnected")
