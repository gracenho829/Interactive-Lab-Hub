import time
from datetime import date, timedelta
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
from adafruit_rgb_display.rgb import color565

# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
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

backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True
buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()

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
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)
x =0
y = top
title = "Relapse Clock!"
draw.text((x,y), title, font = font, fill="#FFFFFF")
disp.image(image, rotation)
userDate = input('How many days do you wish to stay drug-free?: ')
disp.fill(color565(10, 120, 17))  
time.sleep(1)
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
while True:
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    y = top
    draw.text((x,y), userDate, font = font, fill="#FFFFFF")
    y += font.getsize(userDate)[1] *2
    currentTime = time.strftime("%m/%d/%Y")
    d0 = date.today()
    d1 = d0 + timedelta(days=int(userDate))
    deadlineTime = d1.strftime("%m/%d/%Y")
    draw.text((x, y), "Current   " + currentTime, font=font, fill="#FFFFFF")
    y += font.getsize(userDate)[1]*2
    draw.text((x, y), "Deadline   " + deadlineTime, font=font, fill="#FFFFFF")
    y += font.getsize(userDate)[1]

    # Display image.
    disp.image(image, rotation)
    time.sleep(1)
