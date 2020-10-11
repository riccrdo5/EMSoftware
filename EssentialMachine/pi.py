from gpiozero import LED
from time import sleep

led = LED(17)

def blink(led,count):
 for i in range(count):
  led.on()
  sleep(1)
  led.off()
  sleep(1)

blink(led, 2)
