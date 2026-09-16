import time
import math
import digitalio
import board
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789

# Set this to True to run 1 hour per second (24 sec total). Set False for real-time.
SIMULATION_MODE = True 

# Setup SPI bus and display
spi = board.SPI()
disp = st7789.ST7789(
    spi, cs=digitalio.DigitalInOut(board.D5), dc=digitalio.DigitalInOut(board.D25),
    rst=None, baudrate=64000000, width=135, height=240, x_offset=53, y_offset=40,
)


# canvas setup
width = disp.height
height = disp.width
image = Image.new("RGB", (width, height))
draw = ImageDraw.Draw(image)
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)

# Turn on backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output(value=True)

simulated_seconds = 0

while True:
    if SIMULATION_MODE:
        # Advance 180 seconds per frame (at 20 frames a sec, this is 1 hour per sec)
        simulated_seconds = (simulated_seconds + 180) % (60*60*24)
    else:
        # Use exact real world time
        now = datetime.now()
        simulated_seconds = (now.hour * 60 * 60) + (now.minute * 60) + now.second

    hours = simulated_seconds / 3600.0

    # Basic Sky
    sky_color = (10, 10, 40) # dark blue
    if 6 <= hours < 18:
        sky_color = (135, 206, 235) # light blue
    draw.rectangle((0, 0, width, height), outline=0, fill=sky_color)

    # Orbits
    # trigonometry to map time to a circle
    sun_angle = (hours / 24.0) * (2 * math.pi) + (math.pi / 2)
    moon_angle = sun_angle + math.pi
    # convert a polar angle into X and Y screen coordinates
    sun_x, sun_y = (width/2) + 70 * math.cos(sun_angle), 100 + 70 * math.sin(sun_angle)
    moon_x, moon_y = (width/2) + 70 * math.cos(moon_angle), 100 + 70 * math.sin(moon_angle)

    draw.ellipse((sun_x-15, sun_y-15, sun_x+15, sun_y+15), fill=(255, 223, 0)) # yellow
    draw.ellipse((moon_x-12, moon_y-12, moon_x+12, moon_y+12), fill=(220, 220, 220)) # gray

    # Horizon: just a green rectangle at the bottom
    draw.rectangle((0, 100, width, height), outline=0, fill=(34, 139, 34))

    disp.image(image, rotation=90)
    time.sleep(0.05) # 1 / 0.05 = 20 FPS