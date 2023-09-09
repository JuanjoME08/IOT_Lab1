from machine import Pin, ADC, deepsleep, lightsleep
from utime import ticks_ms, sleep_ms
import time

pin = Pin(32)
btn = Pin(0,  Pin.IN)

if btn.value() == 1 :
    print("Entrando en modo sleep")
    deepsleep(1000)  #<-- Modo Profundo