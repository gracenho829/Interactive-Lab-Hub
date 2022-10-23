from __future__ import print_function
import time
import digitalio as dio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
from adafruit_seesaw import seesaw, rotaryio, digitalio
import qwiic_joystick
import sys


# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = dio.DigitalInOut(board.CE0)
dc_pin = dio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the ST7789 display:
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)

seesaw = seesaw.Seesaw(board.I2C(), addr=0x36)
# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 90

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0


# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
bigFont = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36)
# Turn on the backlight
backlight = dio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True


seesaw_product = (seesaw.get_version() >> 16) & 0xFFFF
print("Found product {}".format(seesaw_product))
if seesaw_product != 4991:
    print("Wrong firmware loaded?  Expected 4991")

seesaw.pin_mode(24, seesaw.INPUT_PULLUP)
button = digitalio.DigitalIO(seesaw, 24)
button_held = False

encoder = rotaryio.IncrementalEncoder(seesaw)
last_position = None
current_code = ""
total = 0
myJoystick = qwiic_joystick.QwiicJoystick()
myJoystick.begin()

while True:
    # Draw a black filled box to clear the image.
    position = -encoder.position
    if total == 6: 
        draw.rectangle((0, 0, width, height), outline=0, fill=0)
        y = top
        draw.text((x, y), "Grace gifted you a\n", font=font, fill="#FFFFFF")
        y += font.getsize(last_position)[1]
        draw.text((x, y), "Starbucks \nAmericano", font=bigFont, fill="#FFFFFF")
        disp.image(image, rotation)
        time.sleep(3)
        break

    if str(position) != last_position:
        last_position = str(position)
        print("Position: " + last_position)

    if not button.value and not button_held:
        button_held = True
        print("Button pressed")
        current_code += last_position + " "
        last_position = "Next Code"
        total += 1
        draw.rectangle((0, 0, width, height), outline=0, fill=0)
        y = top
        draw.text((x, y), last_position, font=font, fill="#FFFFFF")
        disp.image(image, rotation)
        time.sleep(1)

    if button.value and button_held:
        button_held = False
        print("Button released")

    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    y = top
    draw.text((x, y), last_position, font=font, fill="#FFFFFF")
    y += font.getsize(last_position)[1]
    draw.text((x, y), "Current Code : \n" + current_code, font=font, fill="#FFFFFF")
    disp.image(image, rotation)
    time.sleep(0.1)


