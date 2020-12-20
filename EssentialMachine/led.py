from time import sleep
from gpiozero import LED

led_mapping = {
    'Surgical Face Mask': 17,
    'Disposable Nitrile Gloves': 18,
    '3.4 fl oz Bottle Sanitizer': 22
}


def blinkLed(prod_list):
    # need a prod to led port
    for prod in prod_list:
        if prod.get('Product(s)') in led_mapping:
            led = LED(led_mapping[prod.get('Product(s)')])
            for i in range(int(prod.get('Quantity'))):
                # print("blinking " + prod.get('Product Name'))
                led.on()
                sleep(0.5)
                led.off()
                sleep(0.5)