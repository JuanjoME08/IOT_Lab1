from machine import Pin, ADC, deepsleep, lightsleep
from utime import ticks_ms, sleep_ms
import time

pin = Pin(32)
btn = Pin(0,  Pin.IN)

adc = ADC(pin)
adc.atten(ADC.ATTN_11DB)
voltage = 0
    
while True:
    status_btn = btn()
    
    voltage_read = adc.read()
    voltage = (3.3 * voltage_read) / 4095
    print(voltage)
    time.sleep_ms(1000)
    #time.sleep(1)
    
    if status_btn ==0 :
        print("Entrando en modo sleep")
        #deepsleep(1000)  #<-- Modo Profundo
        lightsleep(5000)	#<-- Modo Sueno Ligero
