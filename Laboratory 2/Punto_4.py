from machine import Pin, ADC, deepsleep
from utime import ticks_ms
from time import sleep_ms


pin = Pin(32)

adc=ADC(pin)
adc.atten(ADC.ATTN_11DB)

def average():
    
    NumDates = 0
    voltage = 0
    average = 0
    tiempo = ticks_ms()
    
    while True:
        voltage_read=adc.read()
        voltage=voltage+(3.3*voltage_read)/4095
        NumDates +=1
        #time.sleep(1)
        #time.sleep_ms(1000)
        if ticks_ms() - tiempo >= 200:
            average = voltage/NumDates
            print('The average voltage is:', average)
            sleep_ms(500)
            print('And samples is:', NumDates)
            break
    
    return NumDates

while True:
    average()
    
    