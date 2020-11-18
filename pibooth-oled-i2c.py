# -*- coding: utf-8 -*-

"""Plugin to handle small OLED display."""

import time
import datetime
import os
import pibooth
# import fnmatch
#from threading import Thread
from PIL import Image, ImageDraw, ImageFont
from luma.core.interface.serial import i2c, spi, pcf8574
from luma.core.interface.parallel import bitbang_6800
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1309, ssd1325, ssd1331, sh1106, ws0010

__version__ = "1.0.0"
# DJ-Dingo, Kenneth Nicholas Jørgensen

@pibooth.hookimpl
def pibooth_configure(cfg):
    """Declare the new configuration options"""
    
    cfg.add_option('OLED_I2C', 'oled_devices', "ssd1306",
                   "Choose OLED device - SSD1306(Default)",
                   "Choose OLED device", ["ssd1306", "ssd1309", "ssd1325", "ssd1331", "sh1106", "ws0010"])
#  "Choose OLED device", ["SSD1306", "SSD1309", "SSD1322", "SSD1362", "SSD1322_NHD", "SSD1325", "SSD1327", "SSD1331", "SSD1351", "SH1106", "WS0010", "WINSTAR_WEH"])
    cfg.add_option('OLED_I2C', 'oled_port_address', "0x3C",
                   'I2c address 0x3C(Default)',
                   "I2c address", "0x3C")
    cfg.add_option('OLED_I2C', 'oled_port', "1",
                   "Change the I2C port number 0, 1 or 2 - (Default = 1)")
    cfg.add_option('OLED_I2C', 'oled_width', "128",
                   'Change screen WIDTH 128(Default)',
                   "OLED screen width", "128")
    cfg.add_option('OLED_I2C', 'oled_height', "64",
                   'Change screen HEIGHT 32, 64(Default), 96, 128',
                   "OLED screen height", ["32", "64", "96", "128"])
    cfg.add_option('OLED_I2C', 'oled_rotate', "0",
                   'Rotate screen up/down (Default = 0)',
                   "Rotate screen up/down", ["0", "2"])
                   # Pictures
    cfg.add_option('OLED_I2C', 'oled_logo', "Yes",
                   "Logo instead of text",
                   "Logo instead of text", ['Yes', 'No'])
    cfg.add_option('OLED_I2C', 'oled_picture_path', "/home/pi/.config/pibooth/logo",
                   "Pictures/Logo path")
    pictures_path = cfg.get('OLED_I2C', 'oled_picture_path').strip('"')
    _height = cfg.get('OLED_I2C', 'oled_height').strip('"')
    _pictures = os.listdir(pictures_path)  #'/home/pi/.config/pibooth/logo/'
    matching = [s for s in _pictures if _height in s]
    cfg.add_option('OLED_I2C', 'oled_pictures', "",   #pibooth_logo_64.png
                   'Choose logo file',
                   "Choose logo file", matching)  #
    cfg.add_option('OLED_I2C', 'oled_states_pictures', "Yes",
                   "Show state pictures",
                   "Show state pictures", ['Yes', 'No'])
                   # Font
    cfg.add_option('OLED_I2C', 'oled_fonts_path', "/home/pi/.config/pibooth/oled_fonts/",
                   "fonts path")
    fonts_path = cfg.get('OLED_I2C', 'oled_fonts_path').strip('"')
    _fonts = os.listdir(fonts_path)   #'/home/pi/.config/pibooth/oled_fonts/'
    cfg.add_option('OLED_I2C', 'oled_font', "DejaVuSans.ttf",
                   'Choose font',
                   "Choose font", _fonts)
                    # Choose Counter, Text 1
    cfg.add_option('OLED_I2C', 'oled_counter_type1', "Text_Only",
                   "Text-1 counter type - Could be either Taken_Photo, Printed, Forgotten, Remaining_Duplicates, Text_Only",
                   "Text-1 counter type", ['Taken_Photo', 'Printed', 'Forgotten', 'Remaining_Duplicates','Text_Only'])
                   # Text 1
    cfg.add_option('OLED_I2C', 'oled_text_1', "Pibooth",
                   'Text-1',
                   "Text-1", "Pibooth")
    cfg.add_option('OLED_I2C', 'oled_size_1', "28",
                   'Text-1 size',
                   "Text-1 size", "28")
    cfg.add_option('OLED_I2C', 'oled_text1_right', "0",
                   'Text-1 move right',
                   "Text-1 move right", "0")
    cfg.add_option('OLED_I2C', 'oled_text1_down', "0",
                   'Text-1 move down',
                   "Text-1 move down", "0")
                    # Choose Counter2, Text 2
    cfg.add_option('OLED_I2C', 'oled_counter_type2', "Text_Only",
                   "Text-2 counter type - Could be either Taken_Photo, Printed, Forgotten, Remaining_Duplicates, Text_Only",
                   "Text-2 counter type", ['Taken_Photo', 'Printed', 'Forgotten', 'Remaining_Duplicates', 'Text_Only'])
                   # Text 2
    cfg.add_option('OLED_I2C', 'oled_text_2', "",
                   'Text-2',
                   "Text-2", "")
    cfg.add_option('OLED_I2C', 'oled_size_2', "28",
                   'Text-2 size',
                   "Text-2 size", "28")
    cfg.add_option('OLED_I2C', 'oled_text2_right', "16",
                   'Text-2 move right',
                   "Text-2 move right", "16")
    cfg.add_option('OLED_I2C', 'oled_text2_down', "22",
                   'Text-2 move down',
                   "Text-2 move down", "22")
    

def connect_oled_i2c(app, cfg):
    """connect to oled I2c"""
    try:
            
        app.devices = cfg.get('OLED_I2C', 'oled_devices').strip('"')
        app.port_address = cfg.get('OLED_I2C', 'oled_port_address').strip('"')
        app.port = int(cfg.get('OLED_I2C', 'oled_port').strip('"'))
        app.screen_width = int(cfg.get('OLED_I2C', 'oled_width').strip('"'))
        app.screen_height = int(cfg.get('OLED_I2C', 'oled_height').strip('"'))
        app.rotate_screen = int(cfg.get('OLED_I2C', 'oled_rotate'))
        app.logo = cfg.get('OLED_I2C', 'oled_logo').strip('"')
        app.pictures = cfg.get('OLED_I2C', 'oled_pictures').strip('"')
        app.states_pictures = cfg.get('OLED_I2C', 'oled_states_pictures').strip('"')
        app.font = cfg.get('OLED_I2C', 'oled_font').strip('"')
        app.counter_1 = cfg.get('OLED_I2C', 'oled_counter_type1').strip('"')
        app.text_1 = cfg.get('OLED_I2C', 'oled_text_1').strip('"')
        app.size_1 = int(cfg.get('OLED_I2C', 'oled_size_1').strip('"'))
        app.right_1 = int(cfg.get('OLED_I2C', 'oled_text1_right').strip('"'))
        app.down_1 = int(cfg.get('OLED_I2C', 'oled_text1_down').strip('"'))
        app.counter_2 = cfg.get('OLED_I2C', 'oled_counter_type2').strip('"')
        app.text_2 = cfg.get('OLED_I2C', 'oled_text_2').strip('"')
        app.size_2 = int(cfg.get('OLED_I2C', 'oled_size_2').strip('"'))
        app.right_2 = int(cfg.get('OLED_I2C', 'oled_text2_right').strip('"'))
        app.down_2 = int(cfg.get('OLED_I2C', 'oled_text2_down').strip('"'))
    except OSError:
        pass      
      
    # Connect to screen
    app.serial = i2c(port=app.port, address=app.port_address)
    d = app.devices.split()
    if "sh1106" in d:
        app.device = sh1106(app.serial, rotate=app.rotate_screen)
    elif "ssd1306" in d:
        app.device = ssd1306(app.serial, rotate=app.rotate_screen)
    elif "ssd1309" in d:
        app.device = ssd1309(app.serial, rotate=app.rotate_screen)
    elif "ssd1325" in d:
        app.device = ssd1325(app.serial, rotate=app.rotate_screen)
    elif "ssd1331" in d:
        app.device = ssd1331(app.serial, rotate=app.rotate_screen)
    elif "ws0010" in d:
        app.device = ws0010(app.serial, rotate=app.rotate_screen)


def write_text_to_oled(app, cfg):
    # Create blank image for drawing.
    app.image = Image.new("1", (app.device.width, app.device.height))
    app.draw = ImageDraw.Draw(app.image)
    # Load a font.
    font = ImageFont.truetype(app.font, app.size_1)
    font2 = ImageFont.truetype(app.font, app.size_2)
    
    y = app.logo.split()
    if "No" in y:
        with canvas(app.device) as app.draw:
            # Draw the text1 or picture
            x = app.counter_1.split()
            if "Text_Only" in x:
                app.draw.text((app.right_1, app.down_1), app.text_1, font=font, fill=255)
            elif "Taken_Photo" in x:
                app.draw.text((app.right_1, app.down_1), app.text_1 + ('%s' % app.count.taken), font=font, fill=255)
            elif "Printed" in x:
                app.draw.text((app.right_1, app.down_1), app.text_1 + ('%s' % app.count.printed), font=font, fill=255)
            elif "Forgotten" in x:
                app.draw.text((app.right_1, app.down_1), app.text_1 + ('%s' % app.count.forgotten), font=font, fill=255)
            elif "Remaining_Duplicates" in x:
                app.draw.text((app.right_1, app.down_1), app.text_1 + ('%s' % app.count.remaining_duplicates), font=font, fill=255)
                
            # Draw the text 2
            x = app.counter_2.split()
            if "Text_Only" in x:
                app.draw.text((app.right_2, app.down_2), app.text_2, font=font2, fill=255)
            elif "Taken_Photo" in x:
                app.draw.text((app.right_2, app.down_2), app.text_2 + ('%s' % app.count.taken), font=font2, fill=255)
            elif "Printed" in x:
                app.draw.text((app.right_2, app.down_2), app.text_2 + ('%s' % app.count.printed), font=font2, fill=255)
            elif "Forgotten" in x:
                app.draw.text((app.right_2, app.down_2), app.text_2 + ('%s' % app.count.forgotten), font=font2, fill=255)
            elif "Remaining_Duplicates" in x:
                app.draw.text((app.right_2, app.down_2), app.text_2 + ('%s' % app.count.remaining_duplicates), font=font2, fill=255)
            app.image=app.image.show()
    else:
        y = app.logo.split()
        if "Yes" in y:
            if app.screen_height == 32:
                app.image = Image.open('/home/pi/.config/pibooth/oled_pictures/' + app.pictures).convert('1')
            elif app.screen_height == 64:
                app.image = Image.open('/home/pi/.config/pibooth/oled_pictures/' + app.pictures).convert('1')
                # Display image
            app.device.display(app.image)    



@pibooth.hookimpl
def pibooth_startup(app, cfg):
    # Connect the OLED
    # startup.
    connect_oled_i2c(app, cfg)
    write_text_to_oled(app, cfg)
        
@pibooth.hookimpl
def state_wait_enter(app, cfg):
    # Connect the OLED
    # enter in 'wait' state.
    connect_oled_i2c(app, cfg)
    write_text_to_oled(app, cfg)
   
@pibooth.hookimpl
def state_chosen_do(app):
    # Load picture on screen at chosen do
    # Load picture on screen
    s = app.states_pictures.split()
    if "Yes" in s:
        if app.screen_height == 32:
            app.image = Image.open('/home/pi/.config/pibooth/oled_pictures/capture_32.png').convert('1')
        elif app.screen_height == 64:
            app.image = Image.open('/home/pi/.config/pibooth/oled_pictures/capture_64.png').convert('1')
            # Display image
            app.device.display(app.image)


@pibooth.hookimpl
def state_preview_enter(app, cfg):
    # Load picture on screen preview_enter
    # Load picture on screen
    s = app.states_pictures.split()
    if "Yes" in s:
        if app.screen_height == 32:
            app.image = Image.open('/home/pi/.config/pibooth/oled_pictures/capture_32.png').convert('1')
        elif app.screen_height == 64:
            app.image = Image.open('/home/pi/.config/pibooth/oled_pictures/capture_64.png').convert('1')
            # Display image
            app.device.display(app.image)


@pibooth.hookimpl
def state_capture_do(app):
    # Write the BLANK WHITE when picture taken to Oled screen at capture
    s = app.states_pictures.split()
    if "Yes" in s:    
        font = ImageFont.truetype(app.font, app.size_1)
        font2 = ImageFont.truetype(app.font, app.size_2)
        with canvas(app.device) as app.draw:
            app.draw.rectangle(app.device.bounding_box, outline="white", fill="white")
            app.image=app.image.show()


@pibooth.hookimpl
def state_processing_enter(app):
    # Write the picture to Oled screen at processing_enter
    # Load picture on screen
    s = app.states_pictures.split()
    if "Yes" in s:
        if app.screen_height == 32:
            app.image = Image.open('/home/pi/.config/pibooth/oled_pictures/processing_32.png').convert('1')
        elif app.screen_height == 64:
            app.image = Image.open('/home/pi/.config/pibooth/oled_pictures/processing_64.png').convert('1')
            # Display image
            app.device.display(app.image)


@pibooth.hookimpl
def state_print_do(app):
    # Write the picture to Oled screen at print_do
    # Load picture on screen
    s = app.states_pictures.split()
    if "Yes" in s:
        if app.screen_height == 32:
            app.image = Image.open('/home/pi/.config/pibooth/oled_pictures/printer_32.png').convert('1')
        elif app.screen_height == 64:
            app.image = Image.open('/home/pi/.config/pibooth/oled_pictures/printer_64.png').convert('1')
            # Display image
            app.device.display(app.image)


@pibooth.hookimpl
def state_finish_do(app):
    # Write the picture to Oled screen at finish_do
    # Load picture on screen
    s = app.states_pictures.split()
    if "Yes" in s:
        if app.screen_height == 32:
            app.image = Image.open('/home/pi/.config/pibooth/oled_pictures/finished_32.png').convert('1')
        elif app.screen_height == 64:
            app.image = Image.open('/home/pi/.config/pibooth/oled_pictures/finished_64.png').convert('1')
            # Display image
            app.device.display(app.image)


@pibooth.hookimpl
def state_failsafe_do(app):
    # Write the picture to Oled screen at failsafe_do
    # Load picture on screen
    s = app.states_pictures.split()
    if "Yes" in s:
        if app.screen_height == 32:
            app.image = Image.open('/home/pi/.config/pibooth/oled_pictures/printer_failure_32.png').convert('1')
        elif app.screen_height == 64:
            app.image = Image.open('/home/pi/.config/pibooth/oled_pictures/printer_failure_64.png').convert('1')
            # Display image
            app.device.display(app.image)

