# -*- coding: utf-8 -*-

"""Plugin to handle small OLED display."""

import time
import datetime
import os
import pibooth
import fnmatch 
import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

__version__ = "1.0.0"
# DJ-Dingo, Kenneth Nicholas Jørgensen

@pibooth.hookimpl
def pibooth_configure(cfg):
    """Declare the new configuration options"""
    
    cfg.add_option('OLED_I2C', 'oled_chip', "ssd1306",
                   "Choose chip - SSD1306(Default) or ")
    cfg.add_option('OLED_I2C', 'oled_port_address', "0x3C",
                   'Change Port Address 0x3C(Default)',
                   "Port Expander Address", "0x3C")
    cfg.add_option('OLED_I2C', 'oled_port', "1",
                   "Change the I2C port number 1 or 2 - (Default = 1)")
    cfg.add_option('OLED_I2C', 'oled_width', "128",
                   'Change WIDTH 128(Default)',
                   "OLED width", "128")
    cfg.add_option('OLED_I2C', 'oled_height', "64",
                   'Change HEIGHT 64(Default)',
                   "OLED height", ["32", "64"])
                   # Text 1
    _fonts = os.listdir('/home/pi/.config/pibooth/oled_fonts/')
    cfg.add_option('OLED_I2C', 'oled_font', "DejaVuSans-Bold.ttf",
                   'Choose font', 
                   "OLED text 1", _fonts)
    cfg.add_option('OLED_I2C', 'oled_text_1', "Pibooth",
                   'Make text 1',
                   "OLED text 1", "Pibooth")
    cfg.add_option('OLED_I2C', 'oled_size_1', "28",
                   'Make text 1 size',
                   "OLED text 1 size", "28")
    cfg.add_option('OLED_I2C', 'oled_text1_right', "0",
                   'Make text 1 to the right',
                   "OLED text 1 to the right", "0")
    cfg.add_option('OLED_I2C', 'oled_text1_down', "0",
                   'Make text 1 go down',
                   "OLED text 1 go down", "0")
                   # Counter
    cfg.add_option('OLED_I2C', 'oled_counter_type1', "Text_Only",
                   "Counter type 1- Could be either Taken_Photo, Printed, Forgotten, Remaining_Duplicates, Date_Time, PNG-Picture, Text_Only",
                   "Counter type 1", ['Taken_Photo', 'Printed', 'Forgotten', 'Remaining_Duplicates', 'Date_Time', 'PNG-Picture', 'Text_Only'])
                   # Pictures
    _pictures = os.listdir('/home/pi/.config/pibooth/oled_pictures/')
    cfg.add_option('OLED_I2C', 'oled_pictures', "happycat_oled_32.ppm",
                   'Choose pictures', 
                   "OLED pictures", _pictures)
                   # Text 2
    cfg.add_option('OLED_I2C', 'oled_text_2', "",
                   'Make text 2',
                   "OLED text 2", "")
    cfg.add_option('OLED_I2C', 'oled_size_2', "28",
                   'Make text 2 size',
                   "OLED text 2 size", "28")
    cfg.add_option('OLED_I2C', 'oled_text2_right', "16",
                   'Make text 2 to the right',
                   "OLED text 2 to the right", "16")
    cfg.add_option('OLED_I2C', 'oled_text2_down', "22",
                   'Make text 2 go down',
                   "OLED text 2 go down", "22")
    

def connect_oled_i2c(app, cfg):
    """connect to oled I2c"""
    app.port_address = cfg.get('OLED_I2C', 'oled_port_address').strip('"')
    app.screen_width = int(cfg.get('OLED_I2C', 'oled_width').strip('"'))
    app.screen_height = int(cfg.get('OLED_I2C', 'oled_height').strip('"'))
    app.font = cfg.get('OLED_I2C', 'oled_font').strip('"')
    app.text_1 = cfg.get('OLED_I2C', 'oled_text_1').strip('"')
    app.size_1 = int(cfg.get('OLED_I2C', 'oled_size_1').strip('"'))
    app.right_1 = int(cfg.get('OLED_I2C', 'oled_text1_right').strip('"'))
    app.down_1 = int(cfg.get('OLED_I2C', 'oled_text1_down').strip('"'))
    app.counter_1 = cfg.get('OLED_I2C', 'oled_counter_type1').strip('"')
    app.pictures = cfg.get('OLED_I2C', 'oled_pictures').strip('"')
    app.text_2 = cfg.get('OLED_I2C', 'oled_text_2').strip('"')
    app.size_2 = int(cfg.get('OLED_I2C', 'oled_size_2').strip('"'))
    app.right_2 = int(cfg.get('OLED_I2C', 'oled_text2_right').strip('"'))
    app.down_2 = int(cfg.get('OLED_I2C', 'oled_text2_down').strip('"'))

    
    # Setting some variables for our reset pin etc.
    RESET_PIN = digitalio.DigitalInOut(board.D4)
    # Very important... This lets py-gaugette 'know' what pins to use in order to reset the display
    i2c = board.I2C()
    oled = adafruit_ssd1306.SSD1306_I2C(app.screen_width, app.screen_height, i2c, addr=int(app.port_address, 16), reset=RESET_PIN)
    # Clear display.
    oled.fill(0)
    oled.show()
    # Create blank image for drawing.
    image = Image.new("1", (oled.width, oled.height))
    draw = ImageDraw.Draw(image)
    # Load a font.
    font = ImageFont.truetype(app.font, app.size_1)

    # Draw the text1 or picture
    x = app.counter_1.split()
    if "Text_Only" in x:
        draw.text((app.right_1, app.down_1), app.text_1, font=font, fill=255)
    elif "Taken_Photo" in x:
        draw.text((app.right_1, app.down_1), app.text_1 + ('%s' % app.count.taken), font=font, fill=255)
    elif "Printed" in x:
        draw.text((app.right_1, app.down_1), app.text_1 + ('%s' % app.count.printed), font=font, fill=255)
    elif "Forgotten" in x:
        draw.text((app.right_1, app.down_1), app.text_1 + ('%s' % app.count.forgotten), font=font, fill=255)
    elif "Remaining_Duplicates" in x:
        draw.text((app.right_1, app.down_1), app.text_1 + ('%s' % app.count.remaining_duplicates), font=font, fill=255)
    elif "PNG-Picture" in x:
        if app.screen_height == 32:
            image = Image.open('/home/pi/.config/pibooth/oled_pictures/' + app.pictures).convert('1')
        elif app.screen_height == 64:
            image = Image.open('/home/pi/.config/pibooth/oled_pictures/' + app.pictures).convert('1')
        
    # Draw the text2
    draw.text((app.right_2, app.down_2), app.text_2, font=font, fill=255)

# Display image
    oled.image(image)
    oled.show()


@pibooth.hookimpl
def pibooth_startup(app, cfg):
    # Connect the OLED
    # startup.
    connect_oled_i2c(app, cfg)

@pibooth.hookimpl
def state_wait_enter(app, cfg):
    # Connect the OLED
    # enter in 'wait' state.
    connect_oled_i2c(app, cfg)
