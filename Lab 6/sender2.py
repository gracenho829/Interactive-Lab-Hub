import time
import board
import busio
import adafruit_mpr121
from adafruit_seesaw import seesaw, rotaryio, digitalio

import paho.mqtt.client as mqtt
import uuid

# preparations for using the rotary encoder
#
#
#
seesaw = seesaw.Seesaw(board.I2C(), addr=0x36)

seesaw_product = (seesaw.get_version() >> 16) & 0xFFFF
print("Found product {}".format(seesaw_product))
if seesaw_product != 4991:
    print("Wrong firmware loaded?  Expected 4991")

seesaw.pin_mode(24, seesaw.INPUT_PULLUP)
button = digitalio.DigitalIO(seesaw, 24)
button_held = False

encoder = rotaryio.IncrementalEncoder(seesaw)
last_position = None

# setting up the client
#
#
#

client = mqtt.Client(str(uuid.uuid1()))
client.tls_set()
client.username_pw_set('idd', 'device@theFarm')

client.connect(
    'farlab.infosci.cornell.edu',
    port=8883)

topic = 'IDD/your/topic/here'

i2c = busio.I2C(board.SCL, board.SDA)

mpr121 = adafruit_mpr121.MPR121(i2c)

while True:
	position = -encoder.position
	val = "Encoder Position" + str(position)
	print(val)
	client.publish(topic,val)
	time.sleep(0.25)