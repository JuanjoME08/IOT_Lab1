from machine import Pin, ADC, deepsleep, lightsleep
from utime import ticks_ms, sleep_ms
import time
import math

pin_voltage = Pin(32)

adc = ADC(pin_voltage)
adc.atten(ADC.ATTN_11DB)


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
            print('The average voltage is:', offset)
            break
    
    return samples, offset


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


while True:
    
    average()
    
    samples, offset = average()

    current_rms = calculate_rms(samples,offset)

    voltage_rms = 129
    
    apparent_power = current_rms * voltage_rms

    print("Current RMS:", current_rms, "A")
    print("Voltage RMS:", voltage_rms, "V")
    print("Apparent Power:", apparent_power, "VA")
    
