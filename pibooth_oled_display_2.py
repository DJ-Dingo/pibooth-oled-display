# -*- coding: utf-8 -*-

"""Plugin to handle small OLED display I2c or SPI."""
import time
import datetime
import os
import pibooth  
from PIL import Image, ImageDraw, ImageFont # , ImageSequence used for animated gif
# from luma.core.sprite_system import framerate_regulator # used for animated gif
from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1309, ssd1322, ssd1325, ssd1327, ssd1331, ssd1351, ssd1362, sh1106


__version__ = "2.0.0"
# Github "DJ-Dingo", Kenneth Nicholas Jørgensen - Display 2


@pibooth.hookimpl
def pibooth_configure(cfg):
    """Declare the new configuration options"""
                   # Devices SETUP
    cfg.add_option('OLED DISPLAY 2 (SETUP)', 'oled2_devices', "ssd1306",
                   "Choose OLED device 2 - (ssd1306=Default), ssd1309, ssd1322, ssd1325, ssd1327, ssd1331, ssd1362, sh1106",
                   "Choose OLED device 2", ["ssd1306", "ssd1309", "ssd1322", "ssd1325", "ssd1327", "ssd1331", "ssd1362", "sh1106"]) # , "ssd1351"
                   # I2c or SPI
    cfg.add_option('OLED DISPLAY 2 (SETUP)', 'oled2_i2c_or_spi', "I2c",
                   "I2c or SPI display 2 connection",
                   "I2c or SPI connection", ["SPI", "I2c"])
                   # I2c address
    cfg.add_option('OLED DISPLAY 2 (SETUP)', 'oled2_port_address', "0x3D",
                   'I2c address 0x3D(Default)',
                   "I2c address", "0x3D")
                   # Device number
    cfg.add_option('OLED DISPLAY 2 (SETUP)', 'oled2_spi_device_number', "0",
                   "Change SPI device number 0, 1, 2 - (Default = 0)",
                   "SPI device number 0, 1, 2", ["0", "1", "2"])
                   # Port
    cfg.add_option('OLED DISPLAY 2 (SETUP)', 'oled2_port', "1",
                   "Change the I2c or SPI port number 0, 1 or 2 - (SPI = 0,1,2 - I2c = 1)",
                   "Port - I2c(1) or SPI(0)", ["0", "1", "2"])
                   # DC pin
    cfg.add_option('OLED DISPLAY 2 (SETUP)', 'oled2_spi_gpio_dc_pin', "24",
                   "SPI only GPIO DC PIN (24)",
                   "SPI only GPIO DC PIN (24)", "24")
                   # Reset pin
    cfg.add_option('OLED DISPLAY 2 (SETUP)', 'oled2_spi_gpio_rst_pin', "25",
                   "SPI only GPIO RST PIN (25)",
                   "SPI only GPIO RST PIN (25)", "25")
                   # Display size   
    cfg.add_option('OLED DISPLAY 2 (SETUP)', 'oled2_width', "128",
                   'Change screen WIDTH, 32, 48, 64, 80, 96, 128(Default), 160, 256]',
                   "OLED screen width", ["32", "48", "64", "80", "96", "128", "160", "256"])
    cfg.add_option('OLED DISPLAY 2 (SETUP)', 'oled2_height', "64",
                   'Change screen HEIGHT 32, 48, 64(Default), 80, 96, 128, 160, 256',
                   "OLED screen height", ["32", "48", "64", "80", "96", "128", "160", "256"])
                   # Color mode
    cfg.add_option('OLED DISPLAY 2 (SETUP)', 'oled2_color_mode', "1",
                   'Color mode - (Default monochrome = 1) RGB, RGBA',
                   "Color mode (Monochrome = 1)", ["1", "RGB", "RGBA"])
                   # Rotate screen
    cfg.add_option('OLED DISPLAY 2 (SETUP)', 'oled2_rotate', "0",
                   'Rotate screen - (Normal mode = 0 or 2)',
                   "Rotate screen - 0 or 2", ["0", "1", "2", "3"])

                   # TEXT SETUP
                   # Pi Username
    home_directory = os.path.expanduser("~")
                   # States
    cfg.add_option('OLED DISPLAY 2 (MODIFY)', 'oled2_states_pictures', "Yes",
                   "Show state pictures - Yes or No",
                   "Show state pictures", ['Yes', 'No'])
    cfg.add_option('OLED DISPLAY 2 (MODIFY)', 'oled2_state_picture_path', os.path.join(home_directory, ".config/pibooth/oled_display/states/"),
                   "state picture path")
                   # Logo
    cfg.add_option('OLED DISPLAY 2 (MODIFY)', 'oled2_showlogo', "No",
                   "Show logo instead of text - Yes or No",
                   "logo instead of text", ['Yes', 'No']) # , 'Animated Gif'
    cfg.add_option('OLED DISPLAY 2 (MODIFY)', 'oled2_logo_path', os.path.join(home_directory, ".config/pibooth/oled_display/logo/"),
                   "Pictures/Logo path")
    logo_path = cfg.get('OLED DISPLAY 2 (MODIFY)', 'oled2_logo_path').strip('"')
    _logos = sorted(os.listdir(logo_path))
    cfg.add_option('OLED DISPLAY 2 (MODIFY)', 'oled2_logos', "pibooth_64.png",
                   'Choose logo file',
                   "Choose logo file", _logos)
                   # Choose Text 1, Counters 1, Date-Time 1
    cfg.add_option('OLED DISPLAY 2 (MODIFY)', 'oled2_counter_type1', "Taken_Photo",
                   "Text-1 - Counters, Text, Date-Time - Could be either Taken_Photo, Printed, Forgotten, Remaining_Duplicates, Date-Time, Empty, Text_Only",
                   "Text-1 Counter/Text/Time", ['Taken_Photo', 'Printed', 'Forgotten', 'Remaining_Duplicates', 'Date-Time', 'Empty','Text_Only'])
                   # Font 1
    cfg.add_option('OLED DISPLAY 2 (MODIFY)', 'oled2_fonts_path', os.path.join(home_directory, ".config/pibooth/oled_display/fonts/"),
                   "fonts path")
    fonts_path = cfg.get('OLED DISPLAY 2 (MODIFY)', 'oled2_fonts_path').strip('"')
    _fonts = sorted(os.listdir(fonts_path))
    cfg.add_option('OLED DISPLAY 2 (MODIFY)', 'oled2_font_1', "DejaVuSerif-Bold.ttf",
                   'Text 1 font',
                   "Text 1 font", _fonts)
                   # Text 1 color
    cfg.add_option('OLED DISPLAY 2 (MODIFY)', 'oled2_text1_color', "white",
                   'Text-1 color - use HTML color "name". On monochrome displays colors will be converted to "white")',
                   "Text-1 color", ["White", "Red", "Cyan", "Silver", "Blue", "Grey", "DarkBlue", "Black", "LightBlue", "Orange", "Purple", "Brown", "Yellow", "Maroon", "Lime", "Green", "Magenta", "Olive"])
                   # Text 1
    cfg.add_option('OLED DISPLAY 2 (MODIFY)', 'oled2_text_1', '"Photos  "',
                   'Text-1 - Any text with extra space after before a counter, or leave empty to have counter only',
                   "Text-1", '"Photos  "')
                   # Text 1 center on display
    cfg.add_option('OLED DISPLAY 2 (MODIFY)', 'oled2_text_1_center', "No",
                   'Text-1 - Center text on the display',
                   "Text-1 center on display", ['Yes', 'No'])
                   # Text 1 size
    cfg.add_option('OLED DISPLAY 2 (MODIFY)', 'oled2_size_1', "19",
                   'Text-1 size - 19 is default if 3 x text/counters are used on the display at the same time',
                   "Text-1 size", "19")
                   # Move text 1 to the right
    cfg.add_option('OLED DISPLAY 2 (MODIFY)', 'oled2_text1_right', "0",
                   'Text-1 - move text to right on the display',
                   "Text-1 move to right", "0")
                   # Move text 1 down
    cfg.add_option('OLED DISPLAY 2 (MODIFY)', 'oled2_text1_down', "0",
                   'Text-1 - move text down on the display',
                   "Text-1 move down", "0")
                   # Choose Text 2, Counters 2, Date-Time 2
    cfg.add_option('OLED DISPLAY 2 (MODIFY)', 'oled2_counter_type2', "Printed",
                   "Text-2 - Counters, Text, Date-Time - Could be either Taken_Photo, Printed, Forgotten, Remaining_Duplicates, Date-Time, Empty, Text_Only",
                   "Text-2 Counter/Text/Time", ['Taken_Photo', 'Printed', 'Forgotten', 'Remaining_Duplicates', 'Date-Time', 'Empty', 'Text_Only'])
                   # Font 2
    cfg.add_option('OLED DISPLAY 2 (MODIFY)', 'oled2_font_2', "DejaVuSerif-Bold.ttf",
                   'Text 2 font',
                   "Text 2 font", _fonts)
                   # Text 2 color
    cfg.add_option('OLED DISPLAY 2 (MODIFY)', 'oled2_text2_color', "white",
                   'Text-2 color - use HTML color "name". On monochrome displays colors will be converted to "white")',
                   "Text-2 color", ["White", "Red", "Cyan", "Silver", "Blue", "Grey", "DarkBlue", "Black", "LightBlue", "Orange", "Purple", "Brown", "Yellow", "Maroon", "Lime", "Green", "Magenta", "Olive"])
                   # Text 2
    cfg.add_option('OLED DISPLAY 2 (MODIFY)', 'oled2_text_2', '"Printed "',
                   'Text-2 - Any text with extra space after before a counter, or leave empty to have counter only',
                   "Text-2", '"Printed "')
                   # Text 2 center on display
    cfg.add_option('OLED DISPLAY 2 (MODIFY)', 'oled2_text_2_center', "No",
                   'Text-2 - Center text on the display',
                   "Text-2 center on display", ['Yes', 'No'])
                   # Text 2 size
    cfg.add_option('OLED DISPLAY 2 (MODIFY)', 'oled2_size_2', "19",
                   'Text-2 size - 19 is default if 3 x text/counters are used on the display at the same time',
                   "Text-2 size", "19")
                   # Move text 2 to the right
    cfg.add_option('OLED DISPLAY 2 (MODIFY)', 'oled2_text2_right', "0",
                   'Text-2 - move text to right on the display',
                   "Text-2 move to right", "0")
                   # Move text 2 down
    cfg.add_option('OLED DISPLAY 2 (MODIFY)', 'oled2_text2_down', "23",
                   'Text-2 - move text down on the display',
                   "Text-2 move down", "23")
                   # Choose Text 3, Counters 3, Date-Time 3
    cfg.add_option('OLED DISPLAY 2 (MODIFY)', 'oled2_counter_type3', "Remaining_Duplicates",
                   "Text-3, Counter, Date-Time - Could be either Taken_Photo, Printed, Forgotten, Remaining_Duplicates, Date-Time, Empty, Text_Only",
                   "Text-3 Counter/Text/Time", ['Taken_Photo', 'Printed', 'Forgotten', 'Remaining_Duplicates', 'Date-Time', 'Empty', 'Text_Only'])
                   # Font 3
    cfg.add_option('OLED DISPLAY 2 (MODIFY)', 'oled2_font_3', "DejaVuSerif-Bold.ttf",
                   'Text 3 font',
                   "Text 3 font", _fonts)
                   # Text 3 color
    cfg.add_option('OLED DISPLAY 2 (MODIFY)', 'oled2_text3_color', "white",
                   'Text-3 color - use HTML color "name". On monochrome displays colors will be converted to "white")',
                   "Text-3 color", ["White", "Red", "Cyan", "Silver", "Blue", "Grey", "DarkBlue", "Black", "LightBlue", "Orange", "Purple", "Brown", "Yellow", "Maroon", "Lime", "Green", "Magenta", "Olive"])
                   # Text 3
    cfg.add_option('OLED DISPLAY 2 (MODIFY)', 'oled2_text_3', '"Remain "',
                   'Text-3 - Any text with extra space after before a counter, or leave empty to have counter only',
                   "Text-3", '"Remain "')
                   # Text 3 center on display
    cfg.add_option('OLED DISPLAY 2 (MODIFY)', 'oled2_text_3_center', "No",
                   'Text-3 - Center text on the display',
                   "Text-3 center on display", ['Yes', 'No'])
                   # Text 3 size
    cfg.add_option('OLED DISPLAY 2 (MODIFY)', 'oled2_size_3', "19",
                   'Text-3 size - 19 is default if 3 x text/counters are used on the display at the same time',
                   "Text-3 size", "19")
                   # Move text 3, to the right
    cfg.add_option('OLED DISPLAY 2 (MODIFY)', 'oled2_text3_right', "0",
                   'Text-3 - move text to right on the display',
                   "Text-3 move to right", "0")
                   # Move text 3 down
    cfg.add_option('OLED DISPLAY 2 (MODIFY)', 'oled2_text3_down', "46",
                   'Text-3 - move text down on the display',
                   "Text-3 move down", "46")


def connect_oled_i2c_spi_2(app, cfg):
    """connect to oled I2c SPI"""
    try:
        # OLED DISPLAY 2 (SETUP)
        app.devices2 = cfg.get('OLED DISPLAY 2 (SETUP)', 'oled2_devices').strip('"')
        app.i2c_or_spi2 = cfg.get('OLED DISPLAY 2 (SETUP)', 'oled2_i2c_or_spi').strip('"')
        app.spi_gpio_dc2_pin = int(cfg.get('OLED DISPLAY 2 (SETUP)', 'oled2_spi_gpio_dc_pin').strip('"'))
        app.spi_gpio_rst2_pin = int(cfg.get('OLED DISPLAY 2 (SETUP)', 'oled2_spi_gpio_rst_pin').strip('"'))
        app.port2_address = cfg.get('OLED DISPLAY 2 (SETUP)', 'oled2_port_address').strip('"')
        app.spi_device2_number = int(cfg.get('OLED DISPLAY 2 (SETUP)', 'oled2_spi_device_number'))
        app.port2 = int(cfg.get('OLED DISPLAY 2 (SETUP)', 'oled2_port').strip('"'))
        app.color2_mode = cfg.get('OLED DISPLAY 2 (SETUP)', 'oled2_color_mode').strip('"')
        app.screen2_width = int(cfg.get('OLED DISPLAY 2 (SETUP)', 'oled2_width').strip('"'))
        app.screen2_height = int(cfg.get('OLED DISPLAY 2 (SETUP)', 'oled2_height').strip('"'))
        app.rotate2_screen = int(cfg.get('OLED DISPLAY 2 (SETUP)', 'oled2_rotate').strip('"'))
        # Logo / States Images
        app.showlogo2 = cfg.get('OLED DISPLAY 2 (MODIFY)', 'oled2_showlogo').strip('"')
        app.logos2 = cfg.get('OLED DISPLAY 2 (MODIFY)', 'oled2_logos').strip('"')
        app.logo2_path = cfg.get('OLED DISPLAY 2 (MODIFY)', 'oled2_logo_path').strip('"')
        app.states2_pictures = cfg.get('OLED DISPLAY 2 (MODIFY)', 'oled2_states_pictures').strip('"')
        app.state2_picture_path = cfg.get('OLED DISPLAY 2 (MODIFY)', 'oled2_state_picture_path').strip('"')
        # Text 1, Text 2, Text3, Counters, Date-Time, Empty, Size, Right, Down, Color
        for i in range(1, 4):  # loop from 1 to 3
            setattr(app, f'font2_{i}', cfg.get('OLED DISPLAY 2 (MODIFY)', f'oled2_font_{i}').strip('"'))
            setattr(app, f'counter_type2_{i}', cfg.get('OLED DISPLAY 2 (MODIFY)', f'oled2_counter_type{i}').strip('"'))
            setattr(app, f'text2{i}_color', cfg.get('OLED DISPLAY 2 (MODIFY)', f'oled2_text{i}_color').strip('"'))
            setattr(app, f'text2_{i}', cfg.get('OLED DISPLAY 2 (MODIFY)', f'oled2_text_{i}').strip('"'))
            setattr(app, f'text2_{i}_center', cfg.get('OLED DISPLAY 2 (MODIFY)', f'oled2_text_{i}_center').strip('"'))
            setattr(app, f'size2_{i}', int(cfg.get('OLED DISPLAY 2 (MODIFY)', f'oled2_size_{i}').strip('"')))
            setattr(app, f'right2_{i}', int(cfg.get('OLED DISPLAY 2 (MODIFY)', f'oled2_text{i}_right').strip('"')))
            setattr(app, f'down2_{i}', int(cfg.get('OLED DISPLAY 2 (MODIFY)', f'oled2_text{i}_down').strip('"')))
    except OSError:
        pass

    try:
        # Choose I2c or SPI connection
        i2 = app.i2c_or_spi2.split()
        if "SPI" in i2:
            app.serial2 = spi(device=app.spi_device2_number, port=app.port2, gpio_DC=app.spi_gpio_dc2_pin, gpio_RST=app.spi_gpio_rst2_pin)
        elif "I2c" in i2:
            app.serial2 = i2c(port=app.port2, address=app.port2_address)
    except OSError:
        pass
        
    try:  # Connect to screen
        device2_dict = {
            "sh1106": sh1106,
            "ssd1306": ssd1306,
            "ssd1309": ssd1309,
            "ssd1322": ssd1322,
            "ssd1325": ssd1325,
            "ssd1327": ssd1327,
            "ssd1331": ssd1331,
            "ssd1351": ssd1351,
            "ssd1362": ssd1362
        }

        d2 = app.devices2.split()
        for device_name in d2:
            if device_name in device2_dict:
                app.device2 = device2_dict[device_name](app.serial2, rotate=app.rotate2_screen, width=app.screen2_width, height=app.screen2_height)
                break
    except OSError:
        pass



def draw_text_2(app, counter, right, down, text, font, color, center=False):
    x = counter.split()
    final_text = text

    if "Taken_Photo" in x:
        final_text = text + ('%s' % app.count.taken)
    elif "Printed" in x:
        final_text = text + ('%s' % app.count.printed)
    elif "Forgotten" in x:
        final_text = text + ('%s' % app.count.forgotten)
    elif "Remaining_Duplicates" in x:
        final_text = text + ('%s' % app.count.remaining_duplicates)
    elif "Empty" in x:
        final_text = ""
    elif "Date-Time" in x:
        if text == "":
            final_text = time.strftime("%H:%M:%S")
        else:
            final_text = time.strftime(text)
    elif "Text_Only" in x:
        final_text = text

    if center:
        W, H = app.device2.width, app.device2.height
        w, h = font.getsize(final_text)
        right = (W - w) // 2

    app.draw.text((right, down), final_text, font=font, fill=color)


def write_text_to_oled_2(app, cfg):
    """Method called to write text or image on the display
    """
    try:
        # Create blank image for drawing.
        app.image = Image.new(app.color2_mode, (app.device2.width, app.device2.height))
        app.draw = ImageDraw.Draw(app.image)
        # Load a font.
        font_1 = ImageFont.truetype(app.font2_1, app.size2_1)
        font_2 = ImageFont.truetype(app.font2_2, app.size2_2)
        font_3 = ImageFont.truetype(app.font2_3, app.size2_3)

        # Show logo Yes/No
        y = app.showlogo2.split()
        if "No" in y:
            c1 = app.text2_1_center.split()
            c2 = app.text2_2_center.split()
            c3 = app.text2_3_center.split()

            center1 = "Yes" in c1
            center2 = "Yes" in c2
            center3 = "Yes" in c3
            
            with canvas(app.device2) as app.draw:
                draw_text_2(app, app.counter_type2_1, app.right2_1, app.down2_1, app.text2_1, font_1, app.text21_color, center=center1)
                draw_text_2(app, app.counter_type2_2, app.right2_2, app.down2_2, app.text2_2, font_2, app.text22_color, center=center2)
                draw_text_2(app, app.counter_type2_3, app.right2_3, app.down2_3, app.text2_3, font_3, app.text23_color, center=center3)
            # app.device2.display(app.image)
            
        elif "Yes" in y:                
            if app.device2.height in [32, 48, 64, 80, 96, 128, 160, 256]:
                app.image = Image.open(app.logo2_path + app.logos2).convert(app.color2_mode)
                # Display image
                app.device2.display(app.image)
            # Animated Gif is not working
        elif "Animated Gif" in y:
            with Image.open(app.logo2_path + app.logos2) as im:
                regulator = framerate_regulator(fps=5)  # adjust the fps to suit your needs
                for frame in ImageSequence.Iterator(im):
                    resized_frame = frame.resize((app.device2.width, app.device2.height), Image.ANTIALIAS)
                    with regulator:
                        app.device2.display(resized_frame.convert(app.color_mode))
    except OSError:
        pass



def choose_2(app, cfg):
    """Method called to write choose state on the display
    """
    s2 = app.states2_pictures.split()
    if "Yes" in s2:
        app.image = Image.open(app.state2_picture_path + 'choose_{0}.png'.format(app.device2.height)).convert(app.color2_mode)
        app.device2.display(app.image)
    else:
        # Write text instead of picture
        write_text_to_oled_2(app, cfg)

def chosen_2(app, cfg):
    """Method called to write chosen state on the display
    """
    s2 = app.states2_pictures.split()
    if "Yes" in s2:
        app.image = Image.open(app.state2_picture_path + 'layout{0}_{1}.png'.format(app.capture_nbr, app.device2.height)).convert(app.color2_mode)
        app.device2.display(app.image)
    else:
        # Write text instead of picture
        write_text_to_oled_2(app, cfg)

def preview_2(app, cfg):
    """Method called to write preview state on the display
    """
    s2 = app.states2_pictures.split()
    if "Yes" in s2:
        app.image = Image.open(app.state2_picture_path + 'preview_{0}.png'.format(app.device2.height)).convert(app.color2_mode)
        app.device2.display(app.image)
    else:
        # Write text instead of picture
        write_text_to_oled_2(app, cfg)

def capture_2(app, cfg):
    """Method called to write capture state on the display
    """
    s2 = app.states2_pictures.split()
    if "Yes" in s2:
        app.image = Image.open(app.state2_picture_path + 'capture_{0}.png'.format(app.device2.height)).convert(app.color2_mode)
        app.device2.display(app.image)
    else:
        # Write text instead of picture
        write_text_to_oled_2(app, cfg)

def processing_2(app, cfg):
    """Method called to write processing state on the display
    """
    s2 = app.states2_pictures.split()
    if "Yes" in s2:
        app.image = Image.open(app.state2_picture_path + 'processing_{0}.png'.format(app.device2.height)).convert(app.color2_mode)
        app.device2.display(app.image)
    else:
        # Write text instead of picture
        write_text_to_oled_2(app, cfg)

def print_2(app, cfg):
    """Method called to write print state on the display
    """
    s2 = app.states2_pictures.split()
    if "Yes" in s2:
        app.image = Image.open(app.state2_picture_path + 'printer_{0}.png'.format(app.device2.height)).convert(app.color2_mode)
        app.device2.display(app.image)
    else:
        # Write text instead of picture
        write_text_to_oled_2(app, cfg)

def finish_2(app, cfg):
    """Method called to write finish state on the display
    """
    s2 = app.states2_pictures.split()
    if "Yes" in s2:
        app.image = Image.open(app.state2_picture_path + 'finished_{0}.png'.format(app.device2.height)).convert(app.color2_mode)
        app.device2.display(app.image)
    else:
        # Write text instead of picture
        write_text_to_oled_2(app, cfg)


@pibooth.hookimpl
def pibooth_startup(app, cfg):
    # Connect the OLED
    # Write to the display at startup.
    try:
        connect_oled_i2c_spi_2(app, cfg)
        write_text_to_oled_2(app, cfg)
    except:
        pass

@pibooth.hookimpl
def state_wait_enter(app, cfg):
    # Connect the OLED
    # enter in 'wait' state.
    # Re-Write to the display at wait_enter
    try:
        connect_oled_i2c_spi_2(app, cfg)
        write_text_to_oled_2(app, cfg)
    except:
        pass

@pibooth.hookimpl
def state_wait_do(app, cfg):
    # Connect the OLED
    # Enter in 'wait_do' state.
    # Re-Write to the display 
    try:
        write_text_to_oled_2(app, cfg)
    except:
        pass


####### CHOOSE ###############################
@pibooth.hookimpl
def state_choose_enter(app, cfg):
    # Write to the display at choose_enter
    try:
        choose_2(app, cfg)
    except:
        pass

@pibooth.hookimpl
def state_choose_do(app, cfg):
    # Write to the display at choose_do
    try:
        choose_2(app, cfg)
    except:
        pass

@pibooth.hookimpl
def state_choose_exit(app, cfg):
    # Write to the display at choose_exit
    try:
        choose_2(app, cfg)
    except:
        pass


####### CHOSEN ###############################
@pibooth.hookimpl
def state_chosen_enter(app, cfg):
    # Write to the display at chosen enter
    try:
        chosen_2(app, cfg)
    except:
        pass

@pibooth.hookimpl
def state_chosen_do(app, cfg):
    # Write to the display at chosen_do
    try:
        chosen_2(app, cfg)
    except:
        pass

@pibooth.hookimpl
def state_chosen_exit(app, cfg):
    # Write to the display at chosen_exit
    try:
        chosen_2(app, cfg)
    except:
        pass


####### PREVIEW ###############################
@pibooth.hookimpl
def state_preview_enter(app, cfg):
    # Write to the display at preview_enter
    try:
        preview_2(app, cfg)
    except:
        pass

@pibooth.hookimpl
def state_preview_do(app, cfg):
    # Write to the display at preview_do
    try:
        preview_2(app, cfg)
    except:
        pass

@pibooth.hookimpl
def state_preview_exit(app, cfg):
    # Write to the display at preview_exit
    try:
        preview_2(app, cfg)
    except:
        pass


####### CAPTURE ###############################
def state_capture_enter(app, cfg):
    # Write to the display at capture_enter
    try:
        capture_2(app, cfg)
    except:
        pass

@pibooth.hookimpl
def state_capture_do(app, cfg):
    # Write to the display at capture_do
    try:
        capture_2(app, cfg)
    except:
        pass

@pibooth.hookimpl
def state_capture_exit(app, cfg):
    # Write to the display at capture_exit
    try:
        capture_2(app, cfg)
    except:
        pass


####### PROCESSING #############################
@pibooth.hookimpl
def state_processing_enter(app, cfg):
    # Write to the display at processing_enter
    try:
        processing_2(app, cfg)
    except:
        pass

@pibooth.hookimpl
def state_processing_do(app, cfg):
    # Write to the display at processing_do
    try:
        processing_2(app, cfg)
    except:
        pass

@pibooth.hookimpl
def state_processing_exit(app, cfg):
    # Write to the display at processing_exit
    try:
        processing_2(app, cfg)
    except:
        pass


####### PRINT #################################
@pibooth.hookimpl
def state_print_enter(app, cfg):
    # Write to the display at print_enter
    try:
        print_2(app, cfg)
    except:
        pass

@pibooth.hookimpl
def state_print_do(app, cfg):
    # Write to the display at print_do
    try:
        print_2(app, cfg)
    except:
        pass

@pibooth.hookimpl
def state_print_exit(app, cfg):
    # Write to the display at print_exit
    try:
        print_2(app, cfg)
    except:
        pass


####### FINISH #################################
@pibooth.hookimpl
def state_finish_enter(app, cfg):
    # Write to the display at finish_enter
    try:
        finish_2(app, cfg)
    except:
        pass

@pibooth.hookimpl
def state_finish_do(app, cfg):
    # Write to the display at finish_do
    try:
        finish_2(app, cfg)
    except:
        pass

@pibooth.hookimpl
def state_finish_exit(app, cfg):
    # Write to the display at finish_exit
    try:
        finish_2(app, cfg)
        GPIO.cleanup()
        cleanup()
    except:
        pass


####### FAILSAFE ###############################
@pibooth.hookimpl
def state_failsafe_do(app):
    # Write to the display at failsafe_do
    try:
        app.image = Image.open(app.state2_picture_path + 'failure_{0}.png'.format(app.device2.height)).convert(app.color2_mode)
        # Display image
        app.device2.display(app.image)
    except:
        pass
