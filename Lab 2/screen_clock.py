import time
from datetime import date, timedelta
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
from adafruit_rgb_display.rgb import color565

def switchImages(index):
    if index%7 == 0 :
        return "images/plants/sprout.png"
    elif index%7 == 1:
        return "images/plants/bush.png"
    elif index%7  == 2:
        return "images/plants/tree1.png"
    elif index%7  == 3:
        return "images/plants/tree2.png"
    elif index%7  == 4:
        return "images/plants/tree3.png"
    elif index%7  == 5:
        return "images/plants/tree4.png"
    elif index%7 == 6:
        return "images/plants/tree5.png"
    elif index%7  == 7:
        return "images/plants/Untitled-1.png"

def openImage(url):
    image = Image.open(url)
    # Scale the image to the smaller screen dimension
    image_ratio = image.width / image.height
    screen_ratio = width / height
    if screen_ratio < image_ratio:
        scaled_width = image.width * height // image.height
        scaled_height = height
    else:
        scaled_width = width
        scaled_height = image.height * width // image.width
    image = image.resize((scaled_width, scaled_height), Image.BICUBIC)

    # Crop and center the image
    x = scaled_width // 2 - width // 2
    y = scaled_height // 2 - height // 2
    image = image.crop((x, y, x + width, y + height))

    return image
    

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
headerFont = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)
x =0
y = top
title = "Relapse Clock!"
draw.text((x,y), title, font = headerFont, fill="#FFFFFF")
disp.image(image, rotation)
userDate = input('How many days do you wish to stay drug-free?: ')
disp.fill(color565(10, 120, 17))  
time.sleep(1)
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
image = Image.open("images/plants/sprout.png")

index = 0

while True:
    # Resize Image
    
    getURL = switchImages(index)
    image = openImage(getURL)
    draw = ImageDraw.Draw(image)
    y = top
    draw.text((x,y), userDate, font = headerFont, fill="#000000")
    y += font.getsize(userDate)[1]*6
    #currentTime = time.strftime("%m/%d/%Y")
    #draw.text((x, y), "Current   " + currentTime, font=font, fill="#FFFFFF")
    d0 = date.today()
    d1 = d0 + timedelta(days=int(userDate))
    deadlineTime = d1.strftime("%m/%d/%Y Days Left")
    draw.text((x, y), "Finish Date:   " + deadlineTime, font=font, fill="#000000")
    y += font.getsize(userDate)[1]
    image.save('sample-out.jpg')
    # Display image.
    disp.image(image, rotation)
   
    if buttonB.value and not buttonA.value:  # just button A pressed
        index += 1 # set the screen to the users color
    if buttonA.value and not buttonB.value:  # just button B pressed
        index = 0  # set the screen to white


    time.sleep(1)



