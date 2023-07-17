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
# Github "DJ-Dingo", Kenneth Nicholas Jørgensen - Display 1


@pibooth.hookimpl
def pibooth_configure(cfg):
    """Declare the new configuration options"""
                   # Devices SETUP
    cfg.add_option('OLED DISPLAY - (SETUP)', 'oled_devices', "ssd1306",
                   "Choose OLED device - (ssd1306=Default), ssd1309, ssd1322, ssd1325, ssd1327, ssd1331, ssd1362, sh1106",
                   "Choose OLED device", ["ssd1306", "ssd1309", "ssd1322", "ssd1325", "ssd1327", "ssd1331", "ssd1362", "sh1106"]) # , "ssd1351"
                   # I2c or SPI
    cfg.add_option('OLED DISPLAY - (SETUP)', 'oled_i2c_or_spi', "I2c",
                   "I2c or SPI display connection",
                   "I2c or SPI connection", ["SPI", "I2c"])
                   # I2c address
    cfg.add_option('OLED DISPLAY - (SETUP)', 'oled_port_address', "0x3C",
                   'I2c address 0x3C(Default)',
                   "I2c address", "0x3C")
                   # Device number
    cfg.add_option('OLED DISPLAY - (SETUP)', 'oled_spi_device_number', "0",
                   "Change SPI device number 0, 1, 2 - (Default = 0)",
                   "SPI device number 0, 1, 2", ["0", "1", "2"])
                   # Port
    cfg.add_option('OLED DISPLAY - (SETUP)', 'oled_port', "1",
                   "Change the I2c or SPI port number 0, 1 or 2 - (SPI = 0,1,2 - I2c = 1)",
                   "Port - I2c(1) or SPI(0)", ["0", "1", "2"])
                   # DC pin
    cfg.add_option('OLED DISPLAY - (SETUP)', 'oled_spi_gpio_dc_pin', "24",
                   "SPI only GPIO DC PIN (24)",
                   "SPI only GPIO DC PIN (24)", "24")
                   # Reset pin
    cfg.add_option('OLED DISPLAY - (SETUP)', 'oled_spi_gpio_rst_pin', "25",
                   "SPI only GPIO RST PIN (25)",
                   "SPI only GPIO RST PIN (25)", "25")
                   # Display size   
    cfg.add_option('OLED DISPLAY - (SETUP)', 'oled_width', "128",
                   'Change screen WIDTH, 32, 48, 64, 80, 96, 128(Default), 160, 256]',
                   "OLED screen width", ["32", "48", "64", "80", "96", "128", "160", "256"])
    cfg.add_option('OLED DISPLAY - (SETUP)', 'oled_height', "64",
                   'Change screen HEIGHT 32, 48, 64(Default), 80, 96, 128, 160, 256',
                   "OLED screen height", ["32", "48", "64", "80", "96", "128", "160", "256"])
                   # Color mode
    cfg.add_option('OLED DISPLAY - (SETUP)', 'oled_color_mode', "1",
                   'Color mode - (Default monochrome = 1) RGB, RGBA',
                   "Color mode (Monochrome = 1)", ["1", "RGB", "RGBA"])
                   # Rotate screen
    cfg.add_option('OLED DISPLAY - (SETUP)', 'oled_rotate', "0",
                   'Rotate screen - (Normal mode = 0 or 2)',
                   "Rotate screen - 0 or 2", ["0", "1", "2", "3"])

                   # TEXT SETUP
                   # Pi Username
    home_directory = os.path.expanduser("~")
                   # States
    cfg.add_option('OLED DISPLAY - (MODIFY)', 'oled_states_pictures', "Yes",
                   "Show state pictures - Yes or No",
                   "Show state pictures", ['Yes', 'No'])
    cfg.add_option('OLED DISPLAY - (MODIFY)', 'oled_state_picture_path', os.path.join(home_directory, ".config/pibooth/oled_display/states/"),
                   "state picture path")
                   # Logo
    cfg.add_option('OLED DISPLAY - (MODIFY)', 'oled_showlogo', "No",
                   "Show logo instead of text - Yes or No",
                   "logo instead of text", ['Yes', 'No']) # , 'Animated Gif'
    cfg.add_option('OLED DISPLAY - (MODIFY)', 'oled_logo_path', os.path.join(home_directory, ".config/pibooth/oled_display/logo/"),
                   "Pictures/Logo path")
    logo_path = cfg.get('OLED DISPLAY - (MODIFY)', 'oled_logo_path').strip('"')
    _logos = sorted(os.listdir(logo_path))
    cfg.add_option('OLED DISPLAY - (MODIFY)', 'oled_logos', "pibooth_64.png",
                   'Choose logo file',
                   "Choose logo file", _logos)
                   # Choose Text 1, Counters 1, Date-Time 1
    cfg.add_option('OLED DISPLAY - (MODIFY)', 'oled_counter_type1', "Taken_Photo",
                   "Text-1 - Counters, Text, Date-Time - Could be either Taken_Photo, Printed, Forgotten, Remaining_Duplicates, Date-Time, Empty, Text_Only",
                   "Text-1 Counter/Text/Time", ['Taken_Photo', 'Printed', 'Forgotten', 'Remaining_Duplicates', 'Date-Time', 'Empty','Text_Only'])
                   # Font 1
    cfg.add_option('OLED DISPLAY - (MODIFY)', 'oled_fonts_path', os.path.join(home_directory, ".config/pibooth/oled_display/fonts/"),
                   "fonts path")
    fonts_path = cfg.get('OLED DISPLAY - (MODIFY)', 'oled_fonts_path').strip('"')
    _fonts = sorted(os.listdir(fonts_path))
    cfg.add_option('OLED DISPLAY - (MODIFY)', 'oled_font_1', "DejaVuSerif-Bold.ttf",
                   'Text 1 font',
                   "Text 1 font", _fonts)
                   # Text 1 color
    cfg.add_option('OLED DISPLAY - (MODIFY)', 'oled_text1_color', "white",
                   'Text-1 color - use HTML color "name". On monochrome displays colors will be converted to "white")',
                   "Text-1 color", ["White", "Red", "Cyan", "Silver", "Blue", "Grey", "DarkBlue", "Black", "LightBlue", "Orange", "Purple", "Brown", "Yellow", "Maroon", "Lime", "Green", "Magenta", "Olive"])
                   # Text 1
    cfg.add_option('OLED DISPLAY - (MODIFY)', 'oled_text_1', '"Photos  "',
                   'Text-1 - Any text with extra space after before a counter, or leave empty to have counter only',
                   "Text-1", '"Photos  "')
                   # Text 1 center on display
    cfg.add_option('OLED DISPLAY - (MODIFY)', 'oled_text_1_center', "No",
                   'Text-1 - Center text on the display',
                   "Text-1 center on display", ['Yes', 'No'])
                   # Text 1 size
    cfg.add_option('OLED DISPLAY - (MODIFY)', 'oled_size_1', "19",
                   'Text-1 size - 19 is default if 3 x text/counters are used on the display at the same time',
                   "Text-1 size", "19")
                   # Move text 1 to the right
    cfg.add_option('OLED DISPLAY - (MODIFY)', 'oled_text1_right', "0",
                   'Text-1 - move text to right on the display',
                   "Text-1 move to right", "0")
                   # Move text 1 down
    cfg.add_option('OLED DISPLAY - (MODIFY)', 'oled_text1_down', "0",
                   'Text-1 - move text down on the display',
                   "Text-1 move down", "0")
                   # Choose Text 2, Counters 2, Date-Time 2
    cfg.add_option('OLED DISPLAY - (MODIFY)', 'oled_counter_type2', "Printed",
                   "Text-2 - Counters, Text, Date-Time - Could be either Taken_Photo, Printed, Forgotten, Remaining_Duplicates, Date-Time, Empty, Text_Only",
                   "Text-2 Counter/Text/Time", ['Taken_Photo', 'Printed', 'Forgotten', 'Remaining_Duplicates', 'Date-Time', 'Empty', 'Text_Only'])
                   # Font 2
    cfg.add_option('OLED DISPLAY - (MODIFY)', 'oled_font_2', "DejaVuSerif-Bold.ttf",
                   'Text 2 font',
                   "Text 2 font", _fonts)
                   # Text 2 color
    cfg.add_option('OLED DISPLAY - (MODIFY)', 'oled_text2_color', "white",
                   'Text-2 color - use HTML color "name". On monochrome displays colors will be converted to "white")',
                   "Text-2 color", ["White", "Red", "Cyan", "Silver", "Blue", "Grey", "DarkBlue", "Black", "LightBlue", "Orange", "Purple", "Brown", "Yellow", "Maroon", "Lime", "Green", "Magenta", "Olive"])
                   # Text 2
    cfg.add_option('OLED DISPLAY - (MODIFY)', 'oled_text_2', '"Printed "',
                   'Text-2 - Any text with extra space after before a counter, or leave empty to have counter only',
                   "Text-2", '"Printed "')
                   # Text 2 center on display
    cfg.add_option('OLED DISPLAY - (MODIFY)', 'oled_text_2_center', "No",
                   'Text-2 - Center text on the display',
                   "Text-2 center on display", ['Yes', 'No'])
                   # Text 2 size
    cfg.add_option('OLED DISPLAY - (MODIFY)', 'oled_size_2', "19",
                   'Text-2 size - 19 is default if 3 x text/counters are used on the display at the same time',
                   "Text-2 size", "19")
                   # Move text 2 to the right
    cfg.add_option('OLED DISPLAY - (MODIFY)', 'oled_text2_right', "0",
                   'Text-2 - move text to right on the display',
                   "Text-2 move to right", "0")
                   # Move text 2 down
    cfg.add_option('OLED DISPLAY - (MODIFY)', 'oled_text2_down', "23",
                   'Text-2 - move text down on the display',
                   "Text-2 move down", "23")
                   # Choose Text 3, Counters 3, Date-Time 3
    cfg.add_option('OLED DISPLAY - (MODIFY)', 'oled_counter_type3', "Remaining_Duplicates",
                   "Text-3, Counter, Date-Time - Could be either Taken_Photo, Printed, Forgotten, Remaining_Duplicates, Date-Time, Empty, Text_Only",
                   "Text-3 Counter/Text/Time", ['Taken_Photo', 'Printed', 'Forgotten', 'Remaining_Duplicates', 'Date-Time', 'Empty', 'Text_Only'])
                   # Font 3
    cfg.add_option('OLED DISPLAY - (MODIFY)', 'oled_font_3', "DejaVuSerif-Bold.ttf",
                   'Text 3 font',
                   "Text 3 font", _fonts)
                   # Text 3 color
    cfg.add_option('OLED DISPLAY - (MODIFY)', 'oled_text3_color', "white",
                   'Text-3 color - use HTML color "name". On monochrome displays colors will be converted to "white")',
                   "Text-3 color", ["White", "Red", "Cyan", "Silver", "Blue", "Grey", "DarkBlue", "Black", "LightBlue", "Orange", "Purple", "Brown", "Yellow", "Maroon", "Lime", "Green", "Magenta", "Olive"])
                   # Text 3
    cfg.add_option('OLED DISPLAY - (MODIFY)', 'oled_text_3', '"Remain "',
                   'Text-3 - Any text with extra space after before a counter, or leave empty to have counter only',
                   "Text-3", '"Remain "')
                   # Text 3 center on display
    cfg.add_option('OLED DISPLAY - (MODIFY)', 'oled_text_3_center', "No",
                   'Text-3 - Center text on the display',
                   "Text-3 center on display", ['Yes', 'No'])
                   # Text 3 size
    cfg.add_option('OLED DISPLAY - (MODIFY)', 'oled_size_3', "19",
                   'Text-3 size - 19 is default if 3 x text/counters are used on the display at the same time',
                   "Text-3 size", "19")
                   # Move text 3, to the right
    cfg.add_option('OLED DISPLAY - (MODIFY)', 'oled_text3_right', "0",
                   'Text-3 - move text to right on the display',
                   "Text-3 move to right", "0")
                   # Move text 3 down
    cfg.add_option('OLED DISPLAY - (MODIFY)', 'oled_text3_down', "46",
                   'Text-3 - move text down on the display',
                   "Text-3 move down", "46")


def connect_oled_i2c_spi(app, cfg):
    """connect to oled I2c SPI"""
    try:
        # OLED display setup
        app.devices = cfg.get('OLED DISPLAY - (SETUP)', 'oled_devices').strip('"')
        app.i2c_or_spi = cfg.get('OLED DISPLAY - (SETUP)', 'oled_i2c_or_spi').strip('"')
        app.spi_gpio_dc_pin = int(cfg.get('OLED DISPLAY - (SETUP)', 'oled_spi_gpio_dc_pin').strip('"'))
        app.spi_gpio_rst_pin = int(cfg.get('OLED DISPLAY - (SETUP)', 'oled_spi_gpio_rst_pin').strip('"'))
        app.port_address = cfg.get('OLED DISPLAY - (SETUP)', 'oled_port_address').strip('"')
        app.spi_device_number = int(cfg.get('OLED DISPLAY - (SETUP)', 'oled_spi_device_number'))
        app.port = int(cfg.get('OLED DISPLAY - (SETUP)', 'oled_port').strip('"'))
        app.color_mode = cfg.get('OLED DISPLAY - (SETUP)', 'oled_color_mode').strip('"')
        app.screen_width = int(cfg.get('OLED DISPLAY - (SETUP)', 'oled_width').strip('"'))
        app.screen_height = int(cfg.get('OLED DISPLAY - (SETUP)', 'oled_height').strip('"'))
        app.rotate_screen = int(cfg.get('OLED DISPLAY - (SETUP)', 'oled_rotate').strip('"'))
        # Logo / States Images
        app.showlogo = cfg.get('OLED DISPLAY - (MODIFY)', 'oled_showlogo').strip('"')
        app.logos = cfg.get('OLED DISPLAY - (MODIFY)', 'oled_logos').strip('"')
        app.logo_path = cfg.get('OLED DISPLAY - (MODIFY)', 'oled_logo_path').strip('"')
        app.states_pictures = cfg.get('OLED DISPLAY - (MODIFY)', 'oled_states_pictures').strip('"')
        app.state_picture_path = cfg.get('OLED DISPLAY - (MODIFY)', 'oled_state_picture_path').strip('"')
        # Text 1, Text 2, Text3, Counters, Date-Time, Empty, Size, Right, Down, Color
        for i in range(1, 4):  # loop from 1 to 3
            setattr(app, f'font_{i}', cfg.get('OLED DISPLAY - (MODIFY)', f'oled_font_{i}').strip('"'))
            setattr(app, f'counter_type_{i}', cfg.get('OLED DISPLAY - (MODIFY)', f'oled_counter_type{i}').strip('"'))
            setattr(app, f'text{i}_color', cfg.get('OLED DISPLAY - (MODIFY)', f'oled_text{i}_color').strip('"'))
            setattr(app, f'text_{i}', cfg.get('OLED DISPLAY - (MODIFY)', f'oled_text_{i}').strip('"'))
            setattr(app, f'text_{i}_center', cfg.get('OLED DISPLAY - (MODIFY)', f'oled_text_{i}_center').strip('"'))
            setattr(app, f'size_{i}', int(cfg.get('OLED DISPLAY - (MODIFY)', f'oled_size_{i}').strip('"')))
            setattr(app, f'right_{i}', int(cfg.get('OLED DISPLAY - (MODIFY)', f'oled_text{i}_right').strip('"')))
            setattr(app, f'down_{i}', int(cfg.get('OLED DISPLAY - (MODIFY)', f'oled_text{i}_down').strip('"')))
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
        device_dict = {
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

        d = app.devices.split()
        for device_name in d:
            if device_name in device_dict:
                app.device = device_dict[device_name](app.serial, rotate=app.rotate_screen, width=app.screen_width, height=app.screen_height)
                break
    except OSError:
        pass


def draw_text(app, counter, right, down, text, font, color, center=False):
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
        W, H = app.device.width, app.device.height
        w, h = font.getsize(final_text)
        right = (W - w) // 2

    app.draw.text((right, down), final_text, font=font, fill=color)


def write_text_to_oled(app, cfg):
    """Method called to write text or image on the display
    """
    try:
        # Create blank image for drawing.
        app.image = Image.new(app.color_mode, (app.device.width, app.device.height))
        app.draw = ImageDraw.Draw(app.image)
        # Load a font.
        font_1 = ImageFont.truetype(app.font_1, app.size_1)
        font_2 = ImageFont.truetype(app.font_2, app.size_2)
        font_3 = ImageFont.truetype(app.font_3, app.size_3)

        # Show logo Yes/No
        y = app.showlogo.split()
        if "No" in y:
            c1 = app.text_1_center.split()
            c2 = app.text_2_center.split()
            c3 = app.text_3_center.split()

            center1 = "Yes" in c1
            center2 = "Yes" in c2
            center3 = "Yes" in c3
            
            with canvas(app.device) as app.draw:
                draw_text(app, app.counter_type_1, app.right_1, app.down_1, app.text_1, font_1, app.text1_color, center=center1)
                draw_text(app, app.counter_type_2, app.right_2, app.down_2, app.text_2, font_2, app.text2_color, center=center2)
                draw_text(app, app.counter_type_3, app.right_3, app.down_3, app.text_3, font_3, app.text3_color, center=center3)
            # app.device.display(app.image)
            
        elif "Yes" in y:                
            if app.device.height in [32, 48, 64, 80, 96, 128, 160, 256]:
                app.image = Image.open(app.logo_path + app.logos).convert(app.color_mode)
                # Display image
                app.device.display(app.image)
            # Animated Gif is not working
        elif "Animated Gif" in y:
            with Image.open(app.logo_path + app.logos) as im:
                regulator = framerate_regulator(fps=5)  # adjust the fps to suit your needs
                for frame in ImageSequence.Iterator(im):
                    resized_frame = frame.resize((app.device.width, app.device.height), Image.ANTIALIAS)
                    with regulator:
                        app.device.display(resized_frame.convert(app.color_mode))
    except OSError:
        pass


def choose(app, cfg):
    """Method called to write choose state on the display
    """
    s = app.states_pictures.split()
    if "Yes" in s:
        app.image = Image.open(app.state_picture_path + 'choose_{0}.png'.format(app.device.height)).convert(app.color_mode)
        app.device.display(app.image)
    else:
        # Write text instead of picture
        write_text_to_oled(app, cfg)

def chosen(app, cfg):
    """Method called to write chosen state on the display
    """
    s = app.states_pictures.split()
    if "Yes" in s:
        app.image = Image.open(app.state_picture_path + 'layout{0}_{1}.png'.format(app.capture_nbr, app.device.height)).convert(app.color_mode)
        app.device.display(app.image)
    else:
        # Write text instead of picture
        write_text_to_oled(app, cfg)

def preview(app, cfg):
    """Method called to write preview state on the display
    """
    s = app.states_pictures.split()
    if "Yes" in s:
        app.image = Image.open(app.state_picture_path + 'preview_{0}.png'.format(app.device.height)).convert(app.color_mode)
        app.device.display(app.image)
    else:
        # Write text instead of picture
        write_text_to_oled(app, cfg)

def capture(app, cfg):
    """Method called to write capture state on the display
    """
    s = app.states_pictures.split()
    if "Yes" in s:
        app.image = Image.open(app.state_picture_path + 'capture_{0}.png'.format(app.device.height)).convert(app.color_mode)
        app.device.display(app.image)
    else:
        # Write text instead of picture
        write_text_to_oled(app, cfg)

def processing(app, cfg):
    """Method called to write processing state on the display
    """
    s = app.states_pictures.split()
    if "Yes" in s:
        app.image = Image.open(app.state_picture_path + 'processing_{0}.png'.format(app.device.height)).convert(app.color_mode)
        app.device.display(app.image)
    else:
        # Write text instead of picture
        write_text_to_oled(app, cfg)

def print_(app, cfg):
    """Method called to write print state on the display
    """
    s = app.states_pictures.split()
    if "Yes" in s:
        app.image = Image.open(app.state_picture_path + 'printer_{0}.png'.format(app.device.height)).convert(app.color_mode)
        app.device.display(app.image)
    else:
        # Write text instead of picture
        write_text_to_oled(app, cfg)

def finish(app, cfg):
    """Method called to write finish state on the display
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
    # Write to the display at startup.
    try:
        connect_oled_i2c_spi(app, cfg)
        write_text_to_oled(app, cfg)
    except:
        pass

@pibooth.hookimpl
def state_wait_enter(app, cfg):
    # Connect the OLED
    # enter in 'wait' state.
    # Re-Write to the display at wait_enter
    try:
        connect_oled_i2c_spi(app, cfg)
        write_text_to_oled(app, cfg)
    except:
        pass

@pibooth.hookimpl
def state_wait_do(app, cfg):
    # Connect the OLED
    # Enter in 'wait_do' state.
    # Re-Write to the display 
    try:
        write_text_to_oled(app, cfg)
    except:
        pass


####### CHOOSE ###############################
@pibooth.hookimpl
def state_choose_enter(app, cfg):
    # Write to the display at choose_enter
    try:
        choose(app, cfg)
    except:
        pass

@pibooth.hookimpl
def state_choose_do(app, cfg):
    # Write to the display at choose_do
    try:
        choose(app, cfg)
    except:
        pass

@pibooth.hookimpl
def state_choose_exit(app, cfg):
    # Write to the display at choose_exit
    try:
        choose(app, cfg)
    except:
        pass


####### CHOSEN ###############################
@pibooth.hookimpl
def state_chosen_enter(app, cfg):
    # Write to the display at chosen enter
    try:
        chosen(app, cfg)
    except:
        pass

@pibooth.hookimpl
def state_chosen_do(app, cfg):
    # Write to the display at chosen_do
    try:
        chosen(app, cfg)
    except:
        pass

@pibooth.hookimpl
def state_chosen_exit(app, cfg):
    # Write to the display at chosen_exit
    try:
        chosen(app, cfg)
    except:
        pass


####### PREVIEW ###############################
@pibooth.hookimpl
def state_preview_enter(app, cfg):
    # Write to the display at preview_enter
    try:
        preview(app, cfg)
    except:
        pass

@pibooth.hookimpl
def state_preview_do(app, cfg):
    # Write to the display at preview_do
    try:
        preview(app, cfg)
    except:
        pass

@pibooth.hookimpl
def state_preview_exit(app, cfg):
    # Write to the display at preview_exit
    try:
        preview(app, cfg)
    except:
        pass


####### CAPTURE ###############################
def state_capture_enter(app, cfg):
    # Write to the display at capture_enter
    try:
        capture(app, cfg)
    except:
        pass

@pibooth.hookimpl
def state_capture_do(app, cfg):
    # Write to the display at capture_do
    try:
        capture(app, cfg)
    except:
        pass

@pibooth.hookimpl
def state_capture_exit(app, cfg):
    # Write to the display at capture_exit
    try:
        capture(app, cfg)
    except:
        pass


####### PROCESSING #############################
@pibooth.hookimpl
def state_processing_enter(app, cfg):
    # Write to the display at processing_enter
    try:
        processing(app, cfg)
    except:
        pass

@pibooth.hookimpl
def state_processing_do(app, cfg):
    # Write to the display at processing_do
    try:
        processing(app, cfg)
    except:
        pass

@pibooth.hookimpl
def state_processing_exit(app, cfg):
    # Write to the display at processing_exit
    try:
        processing(app, cfg)
    except:
        pass


####### PRINT #################################
@pibooth.hookimpl
def state_print_enter(app, cfg):
    # Write to the display at print_enter
    try:
        print_(app, cfg)
    except:
        pass

@pibooth.hookimpl
def state_print_do(app, cfg):
    # Write to the display at print_do
    try:
        print_(app, cfg)
    except:
        pass

@pibooth.hookimpl
def state_print_exit(app, cfg):
    # Write to the display at print_exit
    try:
        print_(app, cfg)
    except:
        pass


####### FINISH #################################
@pibooth.hookimpl
def state_finish_enter(app, cfg):
    # Write to the display at finish_enter
    try:
        finish(app, cfg)
    except:
        pass

@pibooth.hookimpl
def state_finish_do(app, cfg):
    # Write to the display at finish_do
    try:
        finish(app, cfg)
    except:
        pass

@pibooth.hookimpl
def state_finish_exit(app, cfg):
    # Write to the display at finish_exit
    try:
        finish(app, cfg)
        GPIO.cleanup()
        cleanup()
    except:
        pass


####### FAILSAFE ###############################
@pibooth.hookimpl
def state_failsafe_do(app):
    # Write to the display at failsafe_do
    try:
        app.image = Image.open(app.state_picture_path + 'failure_{0}.png'.format(app.device.height)).convert(app.color_mode)
        # Display image
        app.device.display(app.image)
    except:
        pass
