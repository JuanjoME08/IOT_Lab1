from machine import Pin, ADC, deepsleep
from utime import ticks_ms, sleep_ms
import time

pin = Pin(32)

adc = ADC(pin)
adc.atten(ADC.ATTN_11DB)
voltage = 0
    
while True:
    voltage_read = adc.read()
    voltage = (3.3 * voltage_read) / 4095
    print(voltage)
    time.sleep_ms(1000)
    #time.sleep(1)

        
