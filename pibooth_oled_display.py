# -*- coding: utf-8 -*-

"""Plugin to handle small OLED display."""
import time
import datetime
import os
import pibooth  
from PIL import Image, ImageDraw, ImageFont #, ImageSequence # used for animated gif
# from luma.core.sprite_system import framerate_regulator # used for animated gif
from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1309, ssd1322, ssd1325, ssd1327, ssd1331, ssd1351, ssd1362, sh1106
# from pibooth.pictures import get_pygame_layout_image

__version__ = "1.0.0"
# DJ-Dingo, Kenneth Nicholas Jørgensen


@pibooth.hookimpl
def pibooth_configure(cfg):
    """Declare the new configuration options"""
    cfg.add_option('OLED DISPLAY SETUP', 'oled_devices', "sh1106",
                   "Choose OLED device - (sh1106=Default), ssd1306, ssd1309, ssd1322, ssd1325, ssd1327, ssd1331, ssd1362",
                   "Choose OLED device", ["ssd1306", "ssd1309", "ssd1322", "ssd1325", "ssd1327", "ssd1331", "ssd1362", "sh1106"]) # , "ssd1351"
    cfg.add_option('OLED DISPLAY SETUP', 'oled_i2c_or_spi', "I2c",
                   "I2c or SPI display connection",
                   "I2c or SPI connection", ["SPI", "I2c"])
    cfg.add_option('OLED DISPLAY SETUP', 'oled_port_address', "0x3C",
                   'I2c address 0x3C(Default)',
                   "I2c address", "0x3C")
    cfg.add_option('OLED DISPLAY SETUP', 'oled_spi_device_number', "0",
                   "Change SPI device number 0 or 1 - (Default = 0)",
                   "SPI device number 0 or 1", ["0", "1"])
    cfg.add_option('OLED DISPLAY SETUP', 'oled_port', "1",
                   "Change the I2c or SPI port number 0, 1 or 2 - (SPI = 0 - I2c = 1)",
                   "Port - I2c(1) or SPI(0)", ["0", "1", "2"])
    cfg.add_option('OLED DISPLAY SETUP', 'oled_spi_gpio_dc_pin', "24",
                   "SPI GPIO DC PIN (24)",
                   "SPI GPIO DC PIN (24)", "24")
    cfg.add_option('OLED DISPLAY SETUP', 'oled_spi_gpio_rst_pin', "25",
                   "GPIO RST PIN default(25)",
                   "GPIO RST PIN default(25)", "25")
                   # Display size    
    cfg.add_option('OLED DISPLAY SETUP', 'oled_width', "128",
                   'Change screen WIDTH 128(Default)',
                   "OLED screen width", ["32", "64", "96", "128", "256"])
    cfg.add_option('OLED DISPLAY SETUP', 'oled_height', "64",
                   'Change screen HEIGHT 32, 48, 64(Default), 96, 128, 256',
                   "OLED screen height", ["32", "48", "64", "96", "128", "256"])
    cfg.add_option('OLED DISPLAY SETUP', 'oled_color_mode', "1",
                   'Color mode (Default = 1) RGB, RGBA',
                   "Color mode", ["1", "RGB", "RGBA"])
    cfg.add_option('OLED DISPLAY SETUP', 'oled_rotate', "0",
                   'Rotate screen (Normal mode = 0 or 2)',
                   "Rotate screen", ["0", "1", "2", "3"])
                   # Logo
    cfg.add_option('OLED DISPLAY TEXT', 'oled_showlogo', "No",
                   "Show logo instead of text",
                   "logo instead of text", ['Yes', 'No']) # , 'Animated Gif'
    cfg.add_option('OLED DISPLAY TEXT', 'oled_logo_path', "/home/pi/.config/pibooth/oled_display/logo/",
                   "Pictures/Logo path")
    logo_path = cfg.get('OLED DISPLAY TEXT', 'oled_logo_path').strip('"')
    _logos = sorted(os.listdir(logo_path))
    cfg.add_option('OLED DISPLAY TEXT', 'oled_logos', "pibooth_logo_64.png",
                   'Choose logo file',
                   "Choose logo file", _logos)
    cfg.add_option('OLED DISPLAY TEXT', 'oled_states_pictures', "Yes",
                   "Show state pictures",
                   "Show state pictures", ['Yes', 'No'])
    cfg.add_option('OLED DISPLAY TEXT', 'oled_state_picture_path', "/home/pi/.config/pibooth/oled_display/states/",
                   "state picture path")
                    # Choose Text 1, Counters 1, Date-Time 1
    cfg.add_option('OLED DISPLAY TEXT', 'oled_counter_type1', "Taken_Photo",
                   "Text-1, Counter, Date-Time - Could be either Taken_Photo, Printed, Forgotten, Remaining_Duplicates, Date-Time, Empty, Text_Only",
                   "Text-1 Counter DateTime", ['Taken_Photo', 'Printed', 'Forgotten', 'Remaining_Duplicates', 'Date-Time', 'Empty','Text_Only'])
                   # Font
    cfg.add_option('OLED DISPLAY TEXT', 'oled_fonts_path', "/home/pi/.config/pibooth/oled_display/fonts/",
                   "fonts path")
    fonts_path = cfg.get('OLED DISPLAY TEXT', 'oled_fonts_path').strip('"')
    _fonts = sorted(os.listdir(fonts_path))
    cfg.add_option('OLED DISPLAY TEXT', 'oled_font_1', "DejaVuSerif-Bold.ttf",
                   'Text 1 font',
                   "Text 1 font", _fonts)
                   # Text 1 color
    cfg.add_option('OLED DISPLAY TEXT', 'oled_text1_color', "white",
                   'Text-1 color - use HTML color "name". On monochrome displays colors will be converted to "white")',
                   "Text-1 color", ["White", "Red", "Cyan", "Silver", "Blue", "Grey", "DarkBlue", "Black", "LightBlue", "Orange", "Purple", "Brown", "Yellow", "Maroon", "Lime", "Green", "Magenta", "Olive"])
                   # Text 1
    cfg.add_option('OLED DISPLAY TEXT', 'oled_text_1', '"Photos  "',
                   'Text-1',
                   "Text-1", '"Photos  "')
    cfg.add_option('OLED DISPLAY TEXT', 'oled_size_1', "19",
                   'Text-1 size',
                   "Text-1 size", "19")
    cfg.add_option('OLED DISPLAY TEXT', 'oled_text1_right', "0",
                   'Text-1 move right',
                   "Text-1 move right", "0")
    cfg.add_option('OLED DISPLAY TEXT', 'oled_text1_down', "0",
                   'Text-1 move down',
                   "Text-1 move down", "0")
                    # Choose Text 2, Counters 2, Date-Time 2
    cfg.add_option('OLED DISPLAY TEXT', 'oled_counter_type2', "Printed",
                   "Text-2, Counter, Date-Time - Could be either Taken_Photo, Printed, Forgotten, Remaining_Duplicates, Date-Time, Empty, Text_Only",
                   "Text-2 Counter DateTime", ['Taken_Photo', 'Printed', 'Forgotten', 'Remaining_Duplicates', 'Date-Time', 'Empty', 'Text_Only'])
                    # Font 2
    cfg.add_option('OLED DISPLAY TEXT', 'oled_font_2', "DejaVuSerif-Bold.ttf",
                   'Text 2 font',
                   "Text 2 font", _fonts)
                   # Text 2 color
    cfg.add_option('OLED DISPLAY TEXT', 'oled_text2_color', "white",
                   'Text-2 color - use HTML color "name". On monochrome displays colors will be converted to "white")',
                   "Text-2 color", ["White", "Red", "Cyan", "Silver", "Blue", "Grey", "DarkBlue", "Black", "LightBlue", "Orange", "Purple", "Brown", "Yellow", "Maroon", "Lime", "Green", "Magenta", "Olive"])
                   # Text 2
    cfg.add_option('OLED DISPLAY TEXT', 'oled_text_2', '"Printed "',
                   'Text-2',
                   "Text-2", '"Printed "')
    cfg.add_option('OLED DISPLAY TEXT', 'oled_size_2', "19",
                   'Text-2 size',
                   "Text-2 size", "19")
    cfg.add_option('OLED DISPLAY TEXT', 'oled_text2_right', "0",
                   'Text-2 move right',
                   "Text-2 move right", "0")
    cfg.add_option('OLED DISPLAY TEXT', 'oled_text2_down', "23",
                   'Text-2 move down',
                   "Text-2 move down", "23")
                    # Choose Text 3, Counters 3, Date-Time 3
    cfg.add_option('OLED DISPLAY TEXT', 'oled_counter_type3', "Remaining_Duplicates",
                   "Text-3, Counter, Date-Time - Could be either Taken_Photo, Printed, Forgotten, Remaining_Duplicates, Date-Time, Empty, Text_Only",
                   "Text-3 Counter DateTime", ['Taken_Photo', 'Printed', 'Forgotten', 'Remaining_Duplicates', 'Date-Time', 'Empty', 'Text_Only'])
                    # Font 3
    cfg.add_option('OLED DISPLAY TEXT', 'oled_font_3', "DejaVuSerif-Bold.ttf",
                   'Text 3 font',
                   "Text 3 font", _fonts)
                   # Text 3 color
    cfg.add_option('OLED DISPLAY TEXT', 'oled_text3_color', "white",
                   'Text-3 color - use HTML color "name". On monochrome displays colors will be converted to "white")',
                   "Text-3 color", ["White", "Red", "Cyan", "Silver", "Blue", "Grey", "DarkBlue", "Black", "LightBlue", "Orange", "Purple", "Brown", "Yellow", "Maroon", "Lime", "Green", "Magenta", "Olive"])
                   # Text 3
    cfg.add_option('OLED DISPLAY TEXT', 'oled_text_3', '"Remain "',
                   'Text-3',
                   "Text-3", '"Remain "')
    cfg.add_option('OLED DISPLAY TEXT', 'oled_size_3', "19",
                   'Text-3 size',
                   "Text-3 size", "19")
    cfg.add_option('OLED DISPLAY TEXT', 'oled_text3_right', "0",
                   'Text-3 move right',
                   "Text-3 move right", "0")
    cfg.add_option('OLED DISPLAY TEXT', 'oled_text3_down', "46",
                   'Text-3 move down',
                   "Text-3 move down", "46")
                    # Choose Text 4, Counters 4, Date-Time 4
    cfg.add_option('OLED DISPLAY TEXT', 'oled_counter_type4', "Empty",
                   "Text-4, Counter, Date-Time - Could be either Taken_Photo, Printed, Forgotten, Remaining_Duplicates, Date-Time, Empty, Text_Only",
                   "Text-4 Counter DateTime", ['Taken_Photo', 'Printed', 'Forgotten', 'Remaining_Duplicates', 'Date-Time', 'Empty', 'Text_Only'])
                    # Font 4
    cfg.add_option('OLED DISPLAY TEXT', 'oled_font_4', "DejaVuSerif-Bold.ttf",
                   'Text 4 font',
                   "Text 4 font", _fonts)
                   # Text 4 color
    cfg.add_option('OLED DISPLAY TEXT', 'oled_text4_color', "white",
                   'Text-4 color - use HTML color "name". On monochrome displays colors will be converted to "white")',
                   "Text-4 color", ["White", "Red", "Cyan", "Silver", "Blue", "Grey", "DarkBlue", "Black", "LightBlue", "Orange", "Purple", "Brown", "Yellow", "Maroon", "Lime", "Green", "Magenta", "Olive"])
                   # Text 4
    cfg.add_option('OLED DISPLAY TEXT', 'oled_text_4', '"Text 4"',
                   'Text-4',
                   "Text-4", '"Text 4"')
    cfg.add_option('OLED DISPLAY TEXT', 'oled_size_4', "19",
                   'Text-4 size',
                   "Text-4 size", "19")
    cfg.add_option('OLED DISPLAY TEXT', 'oled_text4_right', "0",
                   'Text-4 move right',
                   "Text-4 move right", "0")
    cfg.add_option('OLED DISPLAY TEXT', 'oled_text4_down', "0",
                   'Text-4 move down',
                   "Text-4 move down", "0")


def connect_oled_i2c_spi(app, cfg):
    """connect to oled I2c SPI"""
    try:
        # OLED display setup
        app.devices = cfg.get('OLED DISPLAY SETUP', 'oled_devices').strip('"')
        app.i2c_or_spi = cfg.get('OLED DISPLAY SETUP', 'oled_i2c_or_spi').strip('"')
        app.spi_gpio_dc_pin = int(cfg.get('OLED DISPLAY SETUP', 'oled_spi_gpio_dc_pin').strip('"'))
        app.spi_gpio_rst_pin = int(cfg.get('OLED DISPLAY SETUP', 'oled_spi_gpio_rst_pin'))
        app.port_address = cfg.get('OLED DISPLAY SETUP', 'oled_port_address').strip('"')
        app.spi_device_number = int(cfg.get('OLED DISPLAY SETUP', 'oled_spi_device_number'))
        app.port = int(cfg.get('OLED DISPLAY SETUP', 'oled_port').strip('"'))
        app.color_mode = cfg.get('OLED DISPLAY SETUP', 'oled_color_mode').strip('"')
        app.screen_width = int(cfg.get('OLED DISPLAY SETUP', 'oled_width').strip('"'))
        app.screen_height = int(cfg.get('OLED DISPLAY SETUP', 'oled_height').strip('"'))
        app.rotate_screen = int(cfg.get('OLED DISPLAY SETUP', 'oled_rotate').strip('"'))
        # Logo / States Images
        app.showlogo = cfg.get('OLED DISPLAY TEXT', 'oled_showlogo').strip('"')
        app.logos = cfg.get('OLED DISPLAY TEXT', 'oled_logos').strip('"')
        app.logo_path = cfg.get('OLED DISPLAY TEXT', 'oled_logo_path').strip('"')
        app.states_pictures = cfg.get('OLED DISPLAY TEXT', 'oled_states_pictures').strip('"')
        app.state_picture_path = cfg.get('OLED DISPLAY TEXT', 'oled_state_picture_path').strip('"')
        # Text 1, Counter, Date-Time
        app.font_1 = cfg.get('OLED DISPLAY TEXT', 'oled_font_1').strip('"')
        app.counter_1 = cfg.get('OLED DISPLAY TEXT', 'oled_counter_type1').strip('"')
        app.text1_color = cfg.get('OLED DISPLAY TEXT', 'oled_text1_color').strip('"')
        app.text_1 = cfg.get('OLED DISPLAY TEXT', 'oled_text_1').strip('"')
        app.size_1 = int(cfg.get('OLED DISPLAY TEXT', 'oled_size_1').strip('"'))
        app.right_1 = int(cfg.get('OLED DISPLAY TEXT', 'oled_text1_right').strip('"'))
        app.down_1 = int(cfg.get('OLED DISPLAY TEXT', 'oled_text1_down').strip('"'))
        # Text 2, Counter, Date-Time
        app.font_2 = cfg.get('OLED DISPLAY TEXT', 'oled_font_2').strip('"')
        app.counter_2 = cfg.get('OLED DISPLAY TEXT', 'oled_counter_type2').strip('"')
        app.text2_color = cfg.get('OLED DISPLAY TEXT', 'oled_text2_color').strip('"')
        app.text_2 = cfg.get('OLED DISPLAY TEXT', 'oled_text_2').strip('"')
        app.size_2 = int(cfg.get('OLED DISPLAY TEXT', 'oled_size_2').strip('"'))
        app.right_2 = int(cfg.get('OLED DISPLAY TEXT', 'oled_text2_right').strip('"'))
        app.down_2 = int(cfg.get('OLED DISPLAY TEXT', 'oled_text2_down').strip('"'))
        # Text 3, Counter, Date-Time
        app.font_3 = cfg.get('OLED DISPLAY TEXT', 'oled_font_3').strip('"')
        app.counter_3 = cfg.get('OLED DISPLAY TEXT', 'oled_counter_type3').strip('"')
        app.text3_color = cfg.get('OLED DISPLAY TEXT', 'oled_text3_color').strip('"')
        app.text_3 = cfg.get('OLED DISPLAY TEXT', 'oled_text_3').strip('"')
        app.size_3 = int(cfg.get('OLED DISPLAY TEXT', 'oled_size_3').strip('"'))
        app.right_3 = int(cfg.get('OLED DISPLAY TEXT', 'oled_text3_right').strip('"'))
        app.down_3 = int(cfg.get('OLED DISPLAY TEXT', 'oled_text3_down').strip('"'))
        # Text 4, Counter, Date-Time
        app.font_4 = cfg.get('OLED DISPLAY TEXT', 'oled_font_4').strip('"')
        app.counter_4 = cfg.get('OLED DISPLAY TEXT', 'oled_counter_type4').strip('"')
        app.text4_color = cfg.get('OLED DISPLAY TEXT', 'oled_text4_color').strip('"')
        app.text_4 = cfg.get('OLED DISPLAY TEXT', 'oled_text_4').strip('"')
        app.size_4 = int(cfg.get('OLED DISPLAY TEXT', 'oled_size_4').strip('"'))
        app.right_4 = int(cfg.get('OLED DISPLAY TEXT', 'oled_text4_right').strip('"'))
        app.down_4 = int(cfg.get('OLED DISPLAY TEXT', 'oled_text4_down').strip('"'))
    except OSError:
        pass

    try:
        # Choose I2c or SPI connection
        i = app.i2c_or_spi.split()
        if "SPI" in i:
            app.serial = spi(device=app.spi_device_number, port=app.port, gpio_DC=app.spi_gpio_dc_pin, gpio_RST=app.spi_gpio_rst_pin)
        elif "I2c" in i:
            app.serial = i2c(port=app.port, address=app.port_address)
    except OSError:
        pass
        
    try:  # Connect to screen
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
    """Method called to write text or image on the screen
    """
    try:
        # Create blank image for drawing.
        app.image = Image.new(app.color_mode, (app.device.width, app.device.height))
        app.draw = ImageDraw.Draw(app.image)
        
        # Load a font.
        font_1 = ImageFont.truetype(app.font_1, app.size_1)
        font_2 = ImageFont.truetype(app.font_2, app.size_2)
        font_3 = ImageFont.truetype(app.font_3, app.size_3)
        font_4 = ImageFont.truetype(app.font_4, app.size_4)
        # Show logo Yes/No
        y = app.showlogo.split()
        if "No" in y:
            with canvas(app.device) as app.draw: # , dither=True
                # Draw the text1 or picture
                x = app.counter_1.split()
                if "Text_Only" in x:
                    app.draw.text((app.right_1, app.down_1), app.text_1, font=font_1, fill=app.text1_color)
                elif "Taken_Photo" in x:
                    app.draw.text((app.right_1, app.down_1), app.text_1 + ('%s' % app.count.taken), font=font_1, fill=app.text1_color)
                elif "Printed" in x:
                    app.draw.text((app.right_1, app.down_1), app.text_1 + ('%s' % app.count.printed), font=font_1, fill=app.text1_color)
                elif "Forgotten" in x:
                    app.draw.text((app.right_1, app.down_1), app.text_1 + ('%s' % app.count.forgotten), font=font_1, fill=app.text1_color)
                elif "Remaining_Duplicates" in x:
                    app.draw.text((app.right_1, app.down_1), app.text_1 + ('%s' % app.count.remaining_duplicates), font=font_1, fill=app.text1_color)
                elif "Empty" in x:
                    app.draw.text((app.right_1, app.down_1), "", font=font_1, fill=app.text1_color)
                elif "Date-Time" in x:
                    if app.text_1 =="":
                        app.draw.text((app.right_1, app.down_1), time.strftime("%H:%M:%S"), font=font_1, fill=app.text1_color)
                    else:
                        app.draw.text((app.right_1, app.down_1), time.strftime(app.text_1), font=font_1, fill=app.text1_color)
                # Draw the text 2
                x = app.counter_2.split()
                if "Text_Only" in x:
                    app.draw.text((app.right_2, app.down_2), app.text_2, font=font_2, fill=app.text2_color)
                elif "Taken_Photo" in x:
                    app.draw.text((app.right_2, app.down_2), app.text_2 + ('%s' % app.count.taken), font=font_2, fill=app.text2_color)
                elif "Printed" in x:
                    app.draw.text((app.right_2, app.down_2), app.text_2 + ('%s' % app.count.printed), font=font_2, fill=app.text2_color)
                elif "Forgotten" in x:
                    app.draw.text((app.right_2, app.down_2), app.text_2 + ('%s' % app.count.forgotten), font=font_2, fill=app.text2_color)
                elif "Remaining_Duplicates" in x:
                    app.draw.text((app.right_2, app.down_2), app.text_2 + ('%s' % app.count.remaining_duplicates), font=font_2, fill=app.text2_color)
                elif "Empty" in x:
                    app.draw.text((app.right_2, app.down_2), "", font=font_2, fill=app.text2_color)
                elif "Date-Time" in x:
                    if app.text_2 =="":
                        app.draw.text((app.right_2, app.down_2), time.strftime("%H:%M:%S"), font=font_2, fill=app.text2_color)
                    else:
                        app.draw.text((app.right_2, app.down_2), time.strftime(app.text_2), font=font_2, fill=app.text2_color)
                # Draw the text 3
                x = app.counter_3.split()
                if "Text_Only" in x:
                    app.draw.text((app.right_3, app.down_3), app.text_3, font=font_3, fill=app.text3_color)
                elif "Taken_Photo" in x:
                    app.draw.text((app.right_3, app.down_3), app.text_3 + ('%s' % app.count.taken), font=font_3, fill=app.text3_color)
                elif "Printed" in x:
                    app.draw.text((app.right_3, app.down_3), app.text_3 + ('%s' % app.count.printed), font=font_3, fill=app.text3_color)
                elif "Forgotten" in x:
                    app.draw.text((app.right_3, app.down_3), app.text_3 + ('%s' % app.count.forgotten), font=font_3, fill=app.text3_color)
                elif "Remaining_Duplicates" in x:
                    app.draw.text((app.right_3, app.down_3), app.text_3 + ('%s' % app.count.remaining_duplicates), font=font_3, fill=app.text3_color)
                elif "Empty" in x:
                    app.draw.text((app.right_3, app.down_3), "", font=font_3, fill=app.text3_color)
                elif "Date-Time" in x:
                    if app.text_3 =="":
                        app.draw.text((app.right_3, app.down_3), time.strftime("%H:%M:%S"), font=font_3, fill=app.text3_color)
                    else:
                        app.draw.text((app.right_3, app.down_3), time.strftime(app.text_3), font=font_3, fill=app.text3_color)
                # Draw the text 4
                x = app.counter_4.split()
                if "Text_Only" in x:
                    app.draw.text((app.right_4, app.down_4), app.text_4, font=font_4, fill=app.text4_color)
                elif "Taken_Photo" in x:
                    app.draw.text((app.right_4, app.down_4), app.text_4 + ('%s' % app.count.taken), font=font_4, fill=app.text4_color)
                elif "Printed" in x:
                    app.draw.text((app.right_4, app.down_4), app.text_4 + ('%s' % app.count.printed), font=font_4, fill=app.text4_color)
                elif "Forgotten" in x:
                    app.draw.text((app.right_4, app.down_4), app.text_4 + ('%s' % app.count.forgotten), font=font_4, fill=app.text4_color)
                elif "Remaining_Duplicates" in x:
                    app.draw.text((app.right_4, app.down_4), app.text_4 + ('%s' % app.count.remaining_duplicates), font=font_4, fill=app.text4_color)
                elif "Empty" in x:
                    app.draw.text((app.right_4, app.down_4), "", font=font_4, fill=app.text4_color)
                elif "Date-Time" in x:
                    if app.text_4 =="":
                        app.draw.text((app.right_4, app.down_4), time.strftime("%H:%M:%S"), font=font_4, fill=app.text4_color)
                    else:
                        app.draw.text((app.right_4, app.down_4), time.strftime(app.text_4), font=font_4, fill=app.text4_color)
                # Display text - these are only used on some older setups
                # app.image=app.image.show()
                # app.device.display(app.image)
        else:       
            # Show logo Yes/No
            y = app.showlogo.split()
            if "Yes" in y:                
                if app.device.height == 32:
                    app.image = Image.open(app.logo_path + app.logos).convert(app.color_mode)
                elif app.device.height == 48:
                    app.image = Image.open(app.logo_path + app.logos).convert(app.color_mode)
                elif app.device.height == 64:
                    app.image = Image.open(app.logo_path + app.logos).convert(app.color_mode)
                elif app.device.height == 96:
                    app.image = Image.open(app.logo_path + app.logos).convert(app.color_mode)
                elif app.device.height == 128:
                    app.image = Image.open(app.logo_path + app.logos).convert(app.color_mode)
                elif app.device.height == 256:
                    app.image = Image.open(app.logo_path + app.logos).convert(app.color_mode)
                # Display image
                app.device.display(app.image)
    except:
        pass


def choose(app, cfg):
    """Method called to write choose state on the screen
    """
    s = app.states_pictures.split()
    if "Yes" in s:
        app.image = Image.open(app.state_picture_path + 'choose_{0}.png'.format(app.device.height)).convert(app.color_mode)
        app.device.display(app.image)
    else:
        # Write text instead of picture
        write_text_to_oled(app, cfg)

def chosen(app, cfg):
    """Method called to write chosen state on the screen
    """
    s = app.states_pictures.split()
    if "Yes" in s:
        app.image = Image.open(app.state_picture_path + 'layout{0}_{1}.png'.format(app.capture_nbr, app.device.height)).convert(app.color_mode)
        app.device.display(app.image)
    else:
        # Write text instead of picture
        write_text_to_oled(app, cfg)

def preview(app, cfg):
    """Method called to write preview state on the screen
    """
    s = app.states_pictures.split()
    if "Yes" in s:
        app.image = Image.open(app.state_picture_path + 'preview_{0}.png'.format(app.device.height)).convert(app.color_mode)
        app.device.display(app.image)
    else:
        # Write text instead of picture
        write_text_to_oled(app, cfg)

def capture(app, cfg):
    """Method called to write capture state on the screen
    """
    s = app.states_pictures.split()
    if "Yes" in s:
        app.image = Image.open(app.state_picture_path + 'capture_{0}.png'.format(app.device.height)).convert(app.color_mode)
        app.device.display(app.image)
    else:
        # Write text instead of picture
        write_text_to_oled(app, cfg)

def processing(app, cfg):
    """Method called to write processing state on the screen
    """
    s = app.states_pictures.split()
    if "Yes" in s:
        app.image = Image.open(app.state_picture_path + 'processing_{0}.png'.format(app.device.height)).convert(app.color_mode)
        app.device.display(app.image)
    else:
        # Write text instead of picture
        write_text_to_oled(app, cfg)

def print_(app, cfg):
    """Method called to write print state on the screen
    """
    s = app.states_pictures.split()
    if "Yes" in s:
        app.image = Image.open(app.state_picture_path + 'printer_{0}.png'.format(app.device.height)).convert(app.color_mode)
        app.device.display(app.image)
    else:
        # Write text instead of picture
        write_text_to_oled(app, cfg)

def finish(app, cfg):
    """Method called to write finish state on the screen
    """
    s = app.states_pictures.split()
    if "Yes" in s:
        app.image = Image.open(app.state_picture_path + 'finished_{0}.png'.format(app.device.height)).convert(app.color_mode)
        app.device.display(app.image)
    else:
        # Write text instead of picture
        write_text_to_oled(app, cfg)


@pibooth.hookimpl
def pibooth_startup(app, cfg):
    # Connect the OLED
    # startup.
    try:
        connect_oled_i2c_spi(app, cfg)
        
    except:
        pass


@pibooth.hookimpl
def state_wait_enter(app, cfg):
    #Connect the OLED
    #enter in 'wait' state.
    # Re-Write the date at wait_enter
    try:
        connect_oled_i2c_spi(app, cfg)
        write_text_to_oled(app, cfg)
    except:
        pass

@pibooth.hookimpl
def state_wait_do(app, cfg):
    #Connect the OLED
    #enter in 'wait_do' state.
    try:
        write_text_to_oled(app, cfg)
    except:
        pass

####### CHOOSE ###############################
@pibooth.hookimpl
def state_choose_enter(app, cfg):
    # Write state picture on screen at choose_enter
    # Re-Write the date at choose_enter
    try:
        choose(app, cfg)
    except:
        pass

@pibooth.hookimpl
def state_choose_do(app, cfg):
    # Write the state picture at choose_do
    # Re-Write the date at choose_do
    try:
        choose(app, cfg)
    except:
        pass
    
@pibooth.hookimpl
def state_choose_exit(app, cfg):
    # Write the state picture at choose_exit
    # Re-Write the date at choose_exit
    try:
        choose(app, cfg)
    except:
        pass


####### CHOSEN ###############################
@pibooth.hookimpl
def state_chosen_enter(app, cfg):
    # Write the state picture at chosen enter
    # Re-Write the date at chosen_enter
    try:
        chosen(app, cfg)
    except:
        pass

@pibooth.hookimpl
def state_chosen_do(app, cfg):
    # Write the state picture at chosen_do
    # Re-Write the date at chosen_do
    try:
        chosen(app, cfg)
    except:
        pass

@pibooth.hookimpl
def state_chosen_exit(app, cfg):
    # Write the state picture at chosen_exit
    # Re-Write the date at chosen_exit
    try:
        chosen(app, cfg)
    except:
        pass


####### PREVIEW ###############################
@pibooth.hookimpl
def state_preview_enter(app, cfg):
    # Write the State picture at preview_enter
    # Re-Write the date at preview_enter
    try:
        preview(app, cfg)
    except:
        pass

@pibooth.hookimpl
def state_preview_do(app, cfg):
    # Write the State picture at preview_do
    # Re-Write the date at preview_do
    try:
        preview(app, cfg)
    except:
        pass

@pibooth.hookimpl
def state_preview_exit(app, cfg):
    # Write the State picture at preview_exit
    # Re-Write the date at preview_exit
    try:
        preview(app, cfg)
    except:
        pass


####### CAPTURE ###############################
@pibooth.hookimpl
def state_capture_enter(app, cfg):
    # Write the State BLANK WHITE background at capture_enter
    # Re-Write the date at capture_enter
    try:
        capture(app, cfg)
    except:
        pass

@pibooth.hookimpl
def state_capture_do(app, cfg):
    # Write the State BLANK WHITE background at capture_do
    # Re-Write the date at capture_do
    try:
        capture(app, cfg)
    except:
        pass

@pibooth.hookimpl
def state_capture_exit(app, cfg):
    # Write the State BLANK WHITE background at capture_exit
    # Re-Write the date at capture_exit
    try:
        capture(app, cfg)
    except:
        pass


####### PROCESSING #############################
@pibooth.hookimpl
def state_processing_enter(app, cfg):
    # Write the State picture at processing_enter
    # Re-Write the date at processing_enter
    try:
        processing(app, cfg)
    except:
        pass

@pibooth.hookimpl
def state_processing_do(app, cfg):
    # Write the State picture at processing_do
    # Re-Write the date at processing_do
    try:
        processing(app, cfg)
    except:
        pass

@pibooth.hookimpl
def state_processing_exit(app, cfg):
    # Write the State picture at processing_exit
    # Re-Write the date at processing_exit
    try:
        processing(app, cfg)
    except:
        pass


####### PRINT #################################
@pibooth.hookimpl
def state_print_enter(app, cfg):
    # Write the State picture at print_enter
    # Re-Write the date at print_enter
    try:
        print_(app, cfg)
    except:
        pass

@pibooth.hookimpl
def state_print_do(app, cfg):
    # Write the State picture at print_do
    # Re-Write the date at print_do
    try:
        print_(app, cfg)
    except:
        pass

@pibooth.hookimpl
def state_print_exit(app, cfg):
    # Write the State picture at print_exit
    # Re-Write the date at print_exit
    try:
        print_(app, cfg)
    except:
        pass


####### FINISH #################################
@pibooth.hookimpl
def state_finish_enter(app, cfg):
    # Write the State picture at finish_enter
    # Re-Write the date at finish_enter
    try:
        finish(app, cfg)
    except:
        pass

@pibooth.hookimpl
def state_finish_do(app, cfg):
    # Write the State picture at finish_do
    # Re-Write the date at finish_do
    try:
        finish(app, cfg)
    except:
        pass

@pibooth.hookimpl
def state_finish_exit(app, cfg):
    # Write the State picture at finish_exit
    # Re-Write the date at finish_exit
    try:
        finish(app, cfg)
        GPIO.cleanup()
    except:
        pass


####### FAILSAFE ###############################
@pibooth.hookimpl
def state_failsafe_do(app):
    # Write the State picture at failsafe_do
    try:
        app.image = Image.open(app.state_picture_path + 'failure_{0}.png'.format(app.device.height)).convert(app.color_mode)
        # Display image
        app.device.display(app.image)
    except:
        pass


