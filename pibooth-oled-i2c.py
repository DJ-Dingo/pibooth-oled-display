# -*- coding: utf-8 -*-

"""Plugin to handle small OLED display."""

import time
import datetime
import os
# import fnmatch
import pibooth
from PIL import Image, ImageDraw, ImageFont
from luma.core.interface.serial import i2c, spi  #, pcf8574
# from luma.core.interface.parallel import bitbang_6800
from luma.core.render import canvas
# from luma.oled.device import ssd1306, ssd1309, ssd1325, ssd1331, sh1106
from luma.oled.device import ssd1306, ssd1309, ssd1322, ssd1325, ssd1327, ssd1331, ssd1351, ssd1362, sh1106
from pibooth.pictures import get_pygame_layout_image


__version__ = "1.0.4"
# DJ-Dingo, Kenneth Nicholas Jørgensen

@pibooth.hookimpl
def pibooth_configure(cfg):
    """Declare the new configuration options"""

    cfg.add_option('OLED_I2C', 'oled_devices', "sh1106",
                   "Choose OLED device - (sh1106=Default)",
                   "Choose OLED device", ["ssd1306", "ssd1309", "ssd1322", "ssd1325", "ssd1327", "ssd1331", "ssd1362", "sh1106"]) # , "ssd1351"
    cfg.add_option('OLED_I2C', 'oled_port_address', "0x3C",
                   'I2c address 0x3C(Default)',
                   "I2c address", "0x3C")
    cfg.add_option('OLED_I2C', 'oled_port', "1",
                   "Change the I2C port number 0, 1 or 2 - (Default = 1)")
    cfg.add_option('OLED_I2C', 'oled_width', "128",
                   'Change screen WIDTH 128(Default)',
                   "OLED screen width", ["32", "64", "96", "128", "256"])
    cfg.add_option('OLED_I2C', 'oled_height', "64",
                   'Change screen HEIGHT 32, 48, 64(Default), 96, 128, 256',
                   "OLED screen height", ["32", "48", "64", "96", "128", "256"])
    cfg.add_option('OLED_I2C', 'oled_color_mode', "1",
                   'Color mode (Default = 1) RGB, RGBA',
                   "Color mode(Default=1)", ["1", "RGB", "RGBA"])
    cfg.add_option('OLED_I2C', 'oled_rotate', "0",
                   'Rotate screen up/down (Default = 0)',
                   "Rotate screen up/down", ["0", "1", "2"])
                   # Logo
    cfg.add_option('OLED_I2C', 'oled_showlogo', "Yes",
                   "Logo instead of text",
                   "Logo instead of text", ['Yes', 'No'])
    cfg.add_option('OLED_I2C', 'oled_logo_path', "/home/pi/.config/pibooth/logo/",
                   "Pictures/Logo path")
    logo_path = cfg.get('OLED_I2C', 'oled_logo_path').strip('"')
    _logos = sorted(os.listdir(logo_path))  #'/home/pi/.config/pibooth/logo/'
    cfg.add_option('OLED_I2C', 'oled_logos', "pibooth_logo_64.png", # pibooth_logo_64.png
                   'Choose logo file',
                   "Choose logo file", _logos)  # _logos  res
    cfg.add_option('OLED_I2C', 'oled_states_pictures', "Yes",
                   "Show state pictures",
                   "Show state pictures", ['Yes', 'No'])
                   # Font
    cfg.add_option('OLED_I2C', 'oled_fonts_path', "/home/pi/.config/pibooth/oled_fonts/",
                   "fonts path")
    fonts_path = cfg.get('OLED_I2C', 'oled_fonts_path').strip('"')
    _fonts = sorted(os.listdir(fonts_path))   #'/home/pi/.config/pibooth/oled_fonts/'
    cfg.add_option('OLED_I2C', 'oled_font_1', "DejaVuSans.ttf",
                   'Text font 1',
                   "Text font 1", _fonts)
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
                    # Font 2
    cfg.add_option('OLED_I2C', 'oled_font_2', "DejaVuSans.ttf",
                   'Text font 2',
                   "Text font 2", _fonts)
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
        app.color_mode = cfg.get('OLED_I2C', 'oled_color_mode').strip('"')
        app.screen_width = int(cfg.get('OLED_I2C', 'oled_width').strip('"'))
        app.screen_height = int(cfg.get('OLED_I2C', 'oled_height').strip('"'))
        app.rotate_screen = int(cfg.get('OLED_I2C', 'oled_rotate'))
        app.showlogo = cfg.get('OLED_I2C', 'oled_showlogo').strip('"')
        app.logos = cfg.get('OLED_I2C', 'oled_logos').strip('"')
        app.logo_path = cfg.get('OLED_I2C', 'oled_logo_path').strip('"')
        app.states_pictures = cfg.get('OLED_I2C', 'oled_states_pictures').strip('"')
        app.font_1 = cfg.get('OLED_I2C', 'oled_font_1').strip('"')
        app.counter_1 = cfg.get('OLED_I2C', 'oled_counter_type1').strip('"')
        app.text_1 = cfg.get('OLED_I2C', 'oled_text_1').strip('"')
        app.size_1 = int(cfg.get('OLED_I2C', 'oled_size_1').strip('"'))
        app.right_1 = int(cfg.get('OLED_I2C', 'oled_text1_right').strip('"'))
        app.down_1 = int(cfg.get('OLED_I2C', 'oled_text1_down').strip('"'))
        app.font_2 = cfg.get('OLED_I2C', 'oled_font_2').strip('"')
        app.counter_2 = cfg.get('OLED_I2C', 'oled_counter_type2').strip('"')
        app.text_2 = cfg.get('OLED_I2C', 'oled_text_2').strip('"')
        app.size_2 = int(cfg.get('OLED_I2C', 'oled_size_2').strip('"'))
        app.right_2 = int(cfg.get('OLED_I2C', 'oled_text2_right').strip('"'))
        app.down_2 = int(cfg.get('OLED_I2C', 'oled_text2_down').strip('"'))
    except OSError:
        pass      

    try:
        # Connect to screen
        app.serial = i2c(port=app.port, address=app.port_address)
        d = app.devices.split()
        if "sh1106" in d:
            app.device = sh1106(app.serial, rotate=app.rotate_screen, width=app.screen_width, height=app.screen_height)
        elif "ssd1306" in d:
            app.device = ssd1306(app.serial, rotate=app.rotate_screen, width=app.screen_width, height=app.screen_height)
        elif "ssd1309" in d:
            app.device = ssd1309(app.serial, rotate=app.rotate_screen, width=app.screen_width, height=app.screen_height)
        elif "ssd1322" in d:
            app.device = ssd1322(app.serial, rotate=app.rotate_screen, width=app.screen_width, height=app.screen_height)
        elif "ssd1325" in d:
            app.device = ssd1325(app.serial, rotate=app.rotate_screen, width=app.screen_width, height=app.screen_height)
        elif "ssd1327" in d:
            app.device = ssd1327(app.serial, rotate=app.rotate_screen, width=app.screen_width, height=app.screen_height)
        elif "ssd1331" in d:
            app.device = ssd1331(app.serial, rotate=app.rotate_screen, width=app.screen_width, height=app.screen_height)
        elif "ssd1351" in d:
            app.device = ssd1351(app.serial, rotate=app.rotate_screen, width=app.screen_width, height=app.screen_height)
        elif "ssd1362" in d:
            app.device = ssd1362(app.serial, rotate=app.rotate_screen, width=app.screen_width, height=app.screen_height)
    except OSError:
        pass      

def write_text_to_oled(app, cfg):
    # Create blank image for drawing.
    try:
        app.image = Image.new(app.color_mode, (app.device.width, app.device.height))
        app.draw = ImageDraw.Draw(app.image)
        # Load a font.
        font_1 = ImageFont.truetype(app.font_1, app.size_1)
        font_2 = ImageFont.truetype(app.font_2, app.size_2)
        # Show logo Yes/No
        y = app.showlogo.split()
        if "No" in y:
            with canvas(app.device) as app.draw: # , dither=True
                # Draw the text1 or picture
                x = app.counter_1.split()
                if "Text_Only" in x:
                    app.draw.text((app.right_1, app.down_1), app.text_1, font=font_1, fill=255)
                elif "Taken_Photo" in x:
                    app.draw.text((app.right_1, app.down_1), app.text_1 + ('%s' % app.count.taken), font=font_1, fill=255)
                elif "Printed" in x:
                    app.draw.text((app.right_1, app.down_1), app.text_1 + ('%s' % app.count.printed), font=font_1, fill=255)
                elif "Forgotten" in x:
                    app.draw.text((app.right_1, app.down_1), app.text_1 + ('%s' % app.count.forgotten), font=font_1, fill=255)
                elif "Remaining_Duplicates" in x:
                    app.draw.text((app.right_1, app.down_1), app.text_1 + ('%s' % app.count.remaining_duplicates), font=font_1, fill=255)
                # Draw the text 2
                x = app.counter_2.split()
                if "Text_Only" in x:
                    app.draw.text((app.right_2, app.down_2), app.text_2, font=font_2, fill=255)
                elif "Taken_Photo" in x:
                    app.draw.text((app.right_2, app.down_2), app.text_2 + ('%s' % app.count.taken), font=font_2, fill=255)
                elif "Printed" in x:
                    app.draw.text((app.right_2, app.down_2), app.text_2 + ('%s' % app.count.printed), font=font_2, fill=255)
                elif "Forgotten" in x:
                    app.draw.text((app.right_2, app.down_2), app.text_2 + ('%s' % app.count.forgotten), font=font_2, fill=255)
                elif "Remaining_Duplicates" in x:
                    app.draw.text((app.right_2, app.down_2), app.text_2 + ('%s' % app.count.remaining_duplicates), font=font_2, fill=255)
                app.image=app.image.show()
        else:
            # Show logo Yes/No
            y = app.showlogo.split()
            if "Yes" in y:
                if app.device.height == 32:
                    app.image = Image.open(app.logo_path + app.logos).convert('1')
                elif app.device.height == 48:
                    app.image = Image.open(app.logo_path + app.logos).convert('1')
                elif app.device.height == 64:
                    app.image = Image.open(app.logo_path + app.logos).convert('1')
                elif app.device.height == 96:
                    app.image = Image.open(app.logo_path + app.logos).convert('1')
                elif app.device.height == 128:
                    app.image = Image.open(app.logo_path + app.logos).convert('1')
                # Display image
                app.device.display(app.image)
    except OSError:
        pass

@pibooth.hookimpl
def pibooth_startup(app, cfg):
    # Connect the OLED
    # startup.
    try:
        connect_oled_i2c(app, cfg)
        write_text_to_oled(app, cfg)
    except OSError:
        pass

@pibooth.hookimpl
def state_wait_enter(app, cfg):
    #Connect the OLED
    #enter in 'wait' state.
    try:
        connect_oled_i2c(app, cfg)
        write_text_to_oled(app, cfg)
    except OSError:
        pass

@pibooth.hookimpl
def state_choose_enter(app, cfg):
    # Write state picture on screen at choose_enter
    try:
        s = app.states_pictures.split()
        if "Yes" in s:
            if app.device.height == 32:
                app.image = Image.open('/home/pi/.config/pibooth/oled_states/layout2_32.png').convert('1')
            elif app.device.height == 48:
                app.image = Image.open('/home/pi/.config/pibooth/oled_states/layout2_48.png').convert('1')
            elif app.device.height == 64:
                app.image = Image.open('/home/pi/.config/pibooth/oled_states/layout2_64.png').convert('1')
            elif app.device.height == 96:
                app.image = Image.open('/home/pi/.config/pibooth/oled_states/layout2_96.png').convert('1')
            elif app.device.height == 128:
                app.image = Image.open('/home/pi/.config/pibooth/oled_states/layout2_128.png').convert('1')
        # Display image
        app.device.display(app.image)
    except OSError:
        pass

@pibooth.hookimpl
def state_chosen_do(app):
    # Write state picture on screen at chosen do
    try:
        s = app.states_pictures.split()
        if "Yes" in s:
            if app.device.height == 32:
                app.image = Image.open('/home/pi/.config/pibooth/oled_states/layout{0}_{1}.png'.format(app.capture_nbr, app.device.height)).convert('1')
            elif app.device.height == 48:
                app.image = Image.open('/home/pi/.config/pibooth/oled_states/layout{0}_{1}.png'.format(app.capture_nbr, app.device.height)).convert('1')
            elif app.device.height == 64:
                app.image = Image.open('/home/pi/.config/pibooth/oled_states/layout{0}_{1}.png'.format(app.capture_nbr, app.device.height)).convert('1')
            elif app.device.height == 96:
                app.image = Image.open('/home/pi/.config/pibooth/oled_states/layout{0}_{1}.png'.format(app.capture_nbr, app.device.height)).convert('1')
            elif app.device.height == 128:
                app.image = Image.open('/home/pi/.config/pibooth/oled_states/layout{0}_{1}.png'.format(app.capture_nbr, app.device.height)).convert('1')
                # Display image
        app.device.display(app.image)
    except OSError:
        pass

@pibooth.hookimpl
def state_preview_enter(app, cfg):
    # Write State picture on Oled screen preview_enter
    try:
        s = app.states_pictures.split()
        if "Yes" in s:
            if app.device.height == 32:
                app.image = Image.open('/home/pi/.config/pibooth/oled_states/capture_32.png').convert('1')
            elif app.device.height == 48:
                app.image = Image.open('/home/pi/.config/pibooth/oled_states/capture_48.png').convert('1')
            elif app.device.height == 64:
                app.image = Image.open('/home/pi/.config/pibooth/oled_states/capture_64.png').convert('1')
            elif app.device.height == 96:
                app.image = Image.open('/home/pi/.config/pibooth/oled_states/capture_96.png').convert('1')
            elif app.device.height == 128:
                app.image = Image.open('/home/pi/.config/pibooth/oled_states/capture_128.png').convert('1')
            # Display image
        app.device.display(app.image)
    except OSError:
        pass

@pibooth.hookimpl
def state_capture_do(app):
    # Write the State BLANK WHITE when picture taken to Oled screen at capture
    try:
        s = app.states_pictures.split()
        if "Yes" in s:    
            font_1 = ImageFont.truetype(app.font_1, app.size_1)
            font_2 = ImageFont.truetype(app.font_2, app.size_2)
            with canvas(app.device) as app.draw:
                app.draw.rectangle(app.device.bounding_box, outline="white", fill="white")
        # Display image
        app.image=app.image.show()
    except OSError:
        pass

@pibooth.hookimpl
def state_processing_enter(app):
    # Write the State picture to Oled screen at processing_enter
    try:
        s = app.states_pictures.split()
        if "Yes" in s:
            if app.device.height == 32:
                app.image = Image.open('/home/pi/.config/pibooth/oled_states/processing_32.png').convert('1')
            elif app.device.height == 48:
                app.image = Image.open('/home/pi/.config/pibooth/oled_states/processing_48.png').convert('1')
            elif app.device.height == 64:
                app.image = Image.open('/home/pi/.config/pibooth/oled_states/processing_64.png').convert('1')
            elif app.device.height == 96:
                app.image = Image.open('/home/pi/.config/pibooth/oled_states/processing_96.png').convert('1')
            elif app.device.height == 128:
                app.image = Image.open('/home/pi/.config/pibooth/oled_states/processing_128.png').convert('1')
        # Display image
        app.device.display(app.image)
    except OSError:
        pass

@pibooth.hookimpl
def state_print_do(app):
    # Write the State picture to Oled screen at print_do
    try:
        s = app.states_pictures.split()
        if "Yes" in s:
            if app.device.height == 32:
                app.image = Image.open('/home/pi/.config/pibooth/oled_states/printer_32.png').convert('1')
            elif app.device.height == 48:
                app.image = Image.open('/home/pi/.config/pibooth/oled_states/printer_48.png').convert('1')
            elif app.device.height == 64:
                app.image = Image.open('/home/pi/.config/pibooth/oled_states/printer_64.png').convert('1')
            elif app.device.height == 96:
                app.image = Image.open('/home/pi/.config/pibooth/oled_states/printer_96.png').convert('1')
            elif app.device.height == 128:
                app.image = Image.open('/home/pi/.config/pibooth/oled_states/printer_128.png').convert('1')
        # Display image
        app.device.display(app.image)
    except OSError:
        pass

@pibooth.hookimpl
def state_finish_do(app):
    # Write the State picture to Oled screen at finish_do
    try:
        s = app.states_pictures.split()
        if "Yes" in s:
            if app.device.height == 32:
                app.image = Image.open('/home/pi/.config/pibooth/oled_states/finished_32.png').convert('1')
            elif app.device.height == 48:
                app.image = Image.open('/home/pi/.config/pibooth/oled_states/finished_48.png').convert('1')
            elif app.device.height == 64:
                app.image = Image.open('/home/pi/.config/pibooth/oled_states/finished_64.png').convert('1')
            elif app.device.height == 96:
                app.image = Image.open('/home/pi/.config/pibooth/oled_states/finished_96.png').convert('1')
            elif app.device.height == 128:
                app.image = Image.open('/home/pi/.config/pibooth/oled_states/finished_128.png').convert('1')
        # Display image
        app.device.display(app.image)
    except OSError:
        pass

@pibooth.hookimpl
def state_failsafe_do(app):
    # Write the State picture to Oled screen at failsafe_do
    try:
        s = app.states_pictures.split()
        if "Yes" in s:
            if app.device.height == 32:
                app.image = Image.open('/home/pi/.config/pibooth/oled_states/printer_failure_32.png').convert('1')
            elif app.device.height == 48:
                app.image = Image.open('/home/pi/.config/pibooth/oled_states/printer_failure_48.png').convert('1')
            elif app.device.height == 64:
                app.image = Image.open('/home/pi/.config/pibooth/oled_states/printer_failure_64.png').convert('1')
            elif app.device.height == 96:
                app.image = Image.open('/home/pi/.config/pibooth/oled_states/printer_failure_96.png').convert('1')
            elif app.device.height == 128:
                app.image = Image.open('/home/pi/.config/pibooth/oled_states/printer_failure_128.png').convert('1')
        # Display image
        app.device.display(app.image)
    except OSError:
        pass

