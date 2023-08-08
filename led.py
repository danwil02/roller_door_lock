
from machine import Pin
from PiicoDev_TMP117 import sleep_ms

pin = Pin("LED", Pin.OUT)
def flash_led(count=1):
    global pin
    for i in range(0, count):
        pin.on()
        sleep_ms(200)
        pin.off()
        sleep_ms(50)
    sleep_ms(100)

def flash_long():
    global pin
    pin.on()
    sleep_ms(1000)
    pin.off()
    sleep_ms(50)

def flash_err():
    global pin
    for i in range(0, 10):
        pin.on()
        sleep_ms(150)
        pin.off()
        sleep_ms(50)
    sleep_ms(100)
