from machine import Pin, ADC, deepsleep, lightsleep
from utime import ticks_ms, sleep_ms
import struct
import time
import math
import bluetooth
from simpleBLE import BLEPeripheral

#Pines del sensor y ADC
pin_voltage = Pin(32)
adc = ADC(pin_voltage)
adc.atten(ADC.ATTN_11DB)

# Bluetooth object
ble = bluetooth.BLE() 

# Environmental service
service="683aa995-81a3-4be4-8456-6bebe973101c" 

# Temperature characteristic
characteristic="74a2a6e4-3ce3-4b5f-929a-a95f216d2525"

# BLE peripheral object
temp = BLEPeripheral(ble,"sensor",service,characteristic) 

#Funcion de promedio
def average():
    
    samples = 0
    voltage = 0
    offset = 0
    time = ticks_ms()
    
    while True:
        voltage_read=adc.read()
        voltage=voltage+3.3*voltage_read/4095
        samples +=1
        
        if ticks_ms() - time >= 200:
            offset = voltage/samples
            #print('The average voltage is:', offset)
            break
    
    return samples, offset

#Funcion de los calculos en valor eficaz RMS

def calculate_rms(samples,offset):
    sensitivity = 0.185
    sum_squares = 0
    for i in range(samples):
        voltage_read = adc.read()
        voltage = 3.3 * voltage_read / 4095
        sum_squares += (voltage - offset) ** 2

    mean_square = sum_squares / samples
    rms_voltage = math.sqrt(mean_square)
    rms_current = rms_voltage / sensitivity  # Aquí multiplicamos por el inverso de la sensibilidad
    return rms_current

def power_inst():
    average()
    samples, offset = average()
    current_rms = calculate_rms(samples,offset)
    
    voltage = 129
    power = current_rms * voltage
    return power

i = 0
sum_power = 0.0

while True:
    sum_power += power_inst()
    # Write every second, notify every 10 seconds.
    i = (i + 1) % 10
    temp.set_values([float(sum_power)], notify=i== 0, indicate=False)
    print("Apparent Power:", sum_power, "kWh")
    time.sleep(1)
    