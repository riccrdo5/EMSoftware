from time import sleep
from gpiozero import LED

led_mapping = {
    'Surgical Face Mask': 17,
    'Disposable Nitrile Gloves': 18,
    '3.4 fl oz Bottle Sanitizer': 22
}