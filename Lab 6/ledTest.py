from __future__ import print_function
import qwiic_led_stick
import time
import sys
import board
import busio
import adafruit_mpr121
import paho.mqtt.client as mqtt
import uuid


client = mqtt.Client(str(uuid.uuid1()))
client.tls_set()
client.username_pw_set('idd', 'device@theFarm')

client.connect(
    'farlab.infosci.cornell.edu',
    port=8883)

topic = 'IDD/doorshock'

i2c = busio.I2C(board.SCL, board.SDA)

mpr121 = adafruit_mpr121.MPR121(i2c)

def cycle_rainbow(LED_stick, delay):
    # Red to yellow
    for g in range(0, 255):
        LED_stick.set_all_LED_color(255, g, 0)
        time.sleep(delay)
    
    # Yellow to green
    for r in range(255, 0, -1):
        LED_stick.set_all_LED_color(r, 255, 0)
        time.sleep(delay)
    
    # Green to cyan
    for b in range(0, 255):
        LED_stick.set_all_LED_color(0, 255, b)
        time.sleep(delay)
    
    # Cyan to blue
    for g in range(255, 0, -1):
        LED_stick.set_all_LED_color(0, g, 255)
        time.sleep(delay)
    
    # Blue to magenta
    for r in range(0, 255):
        LED_stick.set_all_LED_color(r, 0, 255)
        time.sleep(delay)
    
    # Magenta to red
    for b in range(255, 0, -1):
        LED_stick.set_all_LED_color(255, 0, b)
        time.sleep(delay)

def detect_capacitor():
    if mpr121[10].value:
        val = "Someone touched the door knob."
        print(val)
        client.publish(topic, val)

def run_example():

    print("\nSparkFun Qwiic LED Stick Example 7")
    my_stick = qwiic_led_stick.QwiicLEDStick()
    my_stick.set_all_LED_brightness(16)

    if my_stick.begin() == False:
        print("\nThe Qwiic LED Stick isn't connected to the system. Please check your connection", \
            file=sys.stderr)
        return
    print("\nLED Stick ready!")

    while True:
        cycle_rainbow(my_stick, 0.01)
        detect_capacitor()
        time.sleep(0.25)

if __name__ == '__main__':
    try:
        run_example()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example 7")
        sys.exit(0)