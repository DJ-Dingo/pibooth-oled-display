# -*- coding: utf-8 -*-c

"""Plugin to handle small OLED display I2c or SPI."""
import os
import json
import time
import datetime
import threading
from PIL import Image, ImageDraw, ImageFont, ImageSequence
from luma.core.sprite_system import framerate_regulator
from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1309, ssd1322, ssd1325, ssd1327, ssd1331, ssd1351, ssd1362, sh1106
import pibooth
from pibooth.utils import LOGGER


__version__ = "2.0.1"
# Github "DJ-Dingo", Kenneth Nicholas Jørgensen - Display 2


# Paths to Logo and Fonts
cache_dir = os.path.expanduser('~/.config/pibooth/')
fonts_dir = os.path.join(cache_dir, 'oled_display/fonts/')
logos_dir = os.path.join(cache_dir, 'oled_display/logo/')

def update_json_file_2(filename, data):
    """
    This function opens a JSON file and updates it with the provided data.
    :param filename: The name of the file to update
    :param data: The data to write to the file
    """
    # Construct the file path
    file_path = os.path.join(cache_dir, filename)
    # Open the file and write the data to it
    with open(file_path, 'w') as f:
        json.dump(data, f)

def list_fonts_2(directory, *extension):
    """
    This function lists all files in fonts directory.
    :param directory: The directory to scan
    :param extension: Extension 
    :return: A list of all files in the directory
    """
    return [file for file in os.listdir(directory) if file.endswith(extension) and os.path.isfile(os.path.join(directory, file))]

def list_logos_2(directory):
    """
    This function lists all files in logos directory.
    :param directory: The directory to scan
    :return: A list of all files in the logos directory
    """
    return [file for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file))]

def get_fonts():
    # Ensure the directory exists
    if not os.path.exists(fonts_dir):
        os.makedirs(fonts_dir)
    # Now it's safe to list the files in the directory
    return list_fonts(fonts_dir, '.ttf', '.otf')

def get_logos():
    # Ensure the directory exists
    if not os.path.exists(logos_dir):
        os.makedirs(logos_dir)
    # Now it's safe to list the files in the directory
    return list_logos(logos_dir)

# Get the list of all default font names
fonts = get_fonts()
# Get the list of all logo names
logos = get_logos()

# Create and update JSON files with the fonts and logos
update_json_file_2('fonts_2_cache.json', fonts_2)
LOGGER.info("Updating fonts database for OLED display 2")
update_json_file_2('logos_2_cache.json', logos_2)
LOGGER.info("Updating logo database for OLED display 2")


@pibooth.hookimpl
def pibooth_configure(cfg):
    """Declare the new configuration options"""
                   # Devices SETUP
    cfg.add_option('OLED DISPLAY 2 (SETUP)', 'oled2_devices', "ssd1306",
                   "Choose OLED device 2 'ssd1306 (Default)', 'ssd1309', 'ssd1322', 'ssd1325', 'ssd1327', 'ssd1331', 'ssd1362', 'sh1106'",
                   "Choose OLED device 2", ["ssd1306", "ssd1309", "ssd1322", "ssd1325", "ssd1327", "ssd1331", "ssd1362", "sh1106"])
                   # I2c or SPI
    cfg.add_option('OLED DISPLAY 2 (SETUP)', 'oled2_i2c_or_spi', "I2c",
                   "Display 2 connection 'I2c' or 'SPI'",
                   "I2c or SPI connection", ["SPI", "I2c"])
                   # I2c address
    cfg.add_option('OLED DISPLAY 2 (SETUP)', 'oled2_port_address', "0x3d",
                   'I2c address (Default=0x3d)',
                   "I2c address", "0x3d")
                   # Device number
    cfg.add_option('OLED DISPLAY 2 (SETUP)', 'oled2_spi_device_number', "0",
                   "Change SPI device number '0', '1' or '2' (Default = 0)",
                   "SPI device number 0, 1, 2", ["0", "1", "2"])
                   # Port
    cfg.add_option('OLED DISPLAY 2 (SETUP)', 'oled2_port', "1",
                   "Change the I2c or SPI port number - (I2c = '1' - SPI = '0', '1', '2')",
                   "Port - I2c(1) or SPI(0)", ["0", "1", "2"])
                   # DC pin
    cfg.add_option('OLED DISPLAY 2 (SETUP)', 'oled2_spi_gpio_dc_pin', "24",
                   "SPI only GPIO DC PIN (Default=24)",
                   "SPI only GPIO DC PIN (24)", "24")
                   # Reset pin
    cfg.add_option('OLED DISPLAY 2 (SETUP)', 'oled2_spi_gpio_rst_pin', "25",
                   "SPI only GPIO RST PIN (Default=25)",
                   "SPI only GPIO RST PIN (25)", "25")
                   # Display size   
    cfg.add_option('OLED DISPLAY 2 (SETUP)', 'oled2_width', "128",
                   "Change screen WIDTH - '32', '48', '64', '80', '96', '128(Default)', '160', '240', '256', '320'",
                   "OLED screen width", ["32", "48", "64", "80", "96", "128", "160", "240", "256", "320"])
    cfg.add_option('OLED DISPLAY 2 (SETUP)', 'oled2_height', "64",
                   "Change screen HEIGHT - '32', '48', '64(Default)', '80', '96', '128', '160', '240', '256', '320'",
                   "OLED screen height", ["32", "48", "64", "80", "96", "128", "160", "240", "256", "320"])
                   # Color mode
    cfg.add_option('OLED DISPLAY 2 (SETUP)', 'oled2_color_mode', "1",
                   "Color mode - '1 = Monochrome (Default)', 'RGB', 'RGBA'",
                   "Color mode (Monochrome = 1)", ["1", "RGB", "RGBA"])
                   # Rotate screen
    cfg.add_option('OLED DISPLAY 2 (SETUP)', 'oled2_rotate', "0",
                   "Rotate screen - '0 (Default)', '1', '2', '3'",
                   "Rotate screen - 0 or 2", ["0", "1", "2", "3"])
                   # States, Logo, Fonts path
    # Load the font and logo lists from the JSON files
    cache_dir = os.path.expanduser('~/.config/pibooth/')
    with open(os.path.join(cache_dir, 'fonts_2_cache.json')) as f:
        _fonts2 = json.load(f)
    with open(os.path.join(cache_dir, 'logos_2_cache.json')) as f:
        _logos2 = json.load(f)
                   # TEXT SETUP
                   # States Yes/No
    cfg.add_option('OLED DISPLAY 2 (MODIFY)', 'oled2_states_pictures', "Yes",
                   "Show state pictures - 'Yes' or 'No'",
                   "Show state pictures", ['Yes', 'No'])
                   # Logo or animated gif
    cfg.add_option('OLED DISPLAY 2 (MODIFY)', 'oled2_showlogo', "No",
                   "Show Logo or Animated Gif (instead of text) - 'Yes' or 'No'",
                   "Logo instead of text", ['Yes', 'No'])
    cfg.add_option('OLED DISPLAY 2 (MODIFY)', 'oled2_logos', "128x64_Pibooth_2.gif",
                   "Logo or Animated Gif in the folder '~/.config/pibooth/oled_display/logo/'",
                   "Logo or Animated Gif", _logos2)
                   # FPS
    cfg.add_option('OLED DISPLAY 2 (MODIFY)', 'oled2_animated_fps', "15",
                   "FPS (Frames Per Second) speed for Animated Gif",
                   "FPS for Animated Gif", "15")
                   # Choose Text 1, Counters 1, Date-Time 1
    cfg.add_option('OLED DISPLAY 2 (MODIFY)', 'oled2_counter_type1', "Taken_Photo",
                   "Text-1 - Counters, Text, Date-Time - Could be either 'Taken_Photo', 'Printed', 'Forgotten', 'Remaining_Duplicates', 'Date-Time', 'Empty', 'Text_Only'",
                   "Text-1 Counter/Time", ['Taken_Photo', 'Printed', 'Forgotten', 'Remaining_Duplicates', 'Date-Time', 'Empty','Text_Only'])
                   # Font 1
    cfg.add_option('OLED DISPLAY 2 (MODIFY)', 'oled2_font_1', "DejaVuSerif-Bold.ttf",
                   "Text-1 Font - You can add more fonts 'Truetype(.ttf)' or 'Opentype(.otf)', in the folder '~/.config/pibooth/oled_display/fonts/'",
                   "Text-1 Font", _fonts2)
                   # Text 1 color
    cfg.add_option('OLED DISPLAY 2 (MODIFY)', 'oled2_text1_color', "white",
                   "Text-1 Color - uses HTML color names. E.g. 'White', 'Red', 'Cyan', 'Silver', 'Blue', 'Grey', 'DarkBlue', 'Black', 'LightBlue', 'Orange', 'Purple', 'Brown', 'Yellow', 'Maroon', 'Lime', 'Green', 'Magenta', 'Olive'. On Monochrome displays colors will be converted to 'White')",
                   "Text-1 Color", ["White", "Red", "Cyan", "Silver", "Blue", "Grey", "DarkBlue", "Black", "LightBlue", "Orange", "Purple", "Brown", "Yellow", "Maroon", "Lime", "Green", "Magenta", "Olive"])
                   # Text 1
    cfg.add_option('OLED DISPLAY 2 (MODIFY)', 'oled2_text_1', '"Photos  "',
                   'Text-1 - Text with space after to use with counter, or leave empty for counter only',
                   "Text-1 or Empty", '"Photos  "')
                   # Text 1 center on display
    cfg.add_option('OLED DISPLAY 2 (MODIFY)', 'oled2_text_1_center', "No",
                   "Text-1 - Center text on display 'Yes' or 'No'",
                   "Text-1 Center", ['Yes', 'No'])
                   # Text 1 size
    cfg.add_option('OLED DISPLAY 2 (MODIFY)', 'oled2_size_1', "19",
                   'Text-1 Size - 19 is default if 3 x text/counters are used on the display at the same time',
                   "Text-1 Size", "19")
                   # Move text 1 to the right
    cfg.add_option('OLED DISPLAY 2 (MODIFY)', 'oled2_text1_right', "0",
                   "Text-1 - Move text 'Right' on display",
                   "Text-1 Move Right", "0")
                   # Move text 1 down
    cfg.add_option('OLED DISPLAY 2 (MODIFY)', 'oled2_text1_down', "0",
                   "Text-1 - Move text 'Down' on display",
                   "Text-1 Move Down", "0")
                   # Choose Text 2, Counters 2, Date-Time 2
    cfg.add_option('OLED DISPLAY 2 (MODIFY)', 'oled2_counter_type2', "Printed",
                   "Text-2 - Counters, Text, Date-Time - Could be either 'Taken_Photo', 'Printed', 'Forgotten', 'Remaining_Duplicates', 'Date-Time', 'Empty', 'Text_Only'",
                   "Text-2 Counter/Time", ['Taken_Photo', 'Printed', 'Forgotten', 'Remaining_Duplicates', 'Date-Time', 'Empty', 'Text_Only'])
                   # Font 2
    cfg.add_option('OLED DISPLAY 2 (MODIFY)', 'oled2_font_2', "DejaVuSerif-Bold.ttf",
                   "Text-2 Font - You can add more fonts 'Truetype(.ttf)' or 'Opentype(.otf)', in the folder '~/.config/pibooth/oled_display/fonts/'",
                   "Text-2 Font", _fonts2)
                   # Text 2 color
    cfg.add_option('OLED DISPLAY 2 (MODIFY)', 'oled2_text2_color', "white",
                   "Text-2 Color - uses HTML color names. E.g. 'White', 'Red', 'Cyan', 'Silver', 'Blue', 'Grey', 'DarkBlue', 'Black', 'LightBlue', 'Orange', 'Purple', 'Brown', 'Yellow', 'Maroon', 'Lime', 'Green', 'Magenta', 'Olive'. On Monochrome displays colors will be converted to 'White')",
                   "Text-2 Color", ["White", "Red", "Cyan", "Silver", "Blue", "Grey", "DarkBlue", "Black", "LightBlue", "Orange", "Purple", "Brown", "Yellow", "Maroon", "Lime", "Green", "Magenta", "Olive"])
                   # Text 2
    cfg.add_option('OLED DISPLAY 2 (MODIFY)', 'oled2_text_2', '"Printed "',
                   'Text-2 - Text with space after to use with counter, or leave empty for counter only',
                   "Text-2 or Empty", '"Printed "')
                   # Text 2 center on display
    cfg.add_option('OLED DISPLAY 2 (MODIFY)', 'oled2_text_2_center', "No",
                   "Text-2 - Center text on display 'Yes' or 'No'",
                   "Text-2 Center", ['Yes', 'No'])
                   # Text 2 size
    cfg.add_option('OLED DISPLAY 2 (MODIFY)', 'oled2_size_2', "19",
                   'Text-2 Size - 19 is default if 3 x text/counters are used on the display at the same time',
                   "Text-2 Size", "19")
                   # Move text 2 to the right
    cfg.add_option('OLED DISPLAY 2 (MODIFY)', 'oled2_text2_right', "0",
                   "Text-2 - Move text 'Right' on display",
                   "Text-2 Move Right", "0")
                   # Move text 2 down
    cfg.add_option('OLED DISPLAY 2 (MODIFY)', 'oled2_text2_down', "23",
                   "Text-2 - Move text 'Down' on display",
                   "Text-2 Move Down", "23")
                   # Choose Text 3, Counters 3, Date-Time 3
    cfg.add_option('OLED DISPLAY 2 (MODIFY)', 'oled2_counter_type3', "Remaining_Duplicates",
                   "Text-3, Counter, Date-Time - Could be either 'Taken_Photo', 'Printed', 'Forgotten', 'Remaining_Duplicates', 'Date-Time', 'Empty', 'Text_Only'",
                   "Text-3 Counter/Time", ['Taken_Photo', 'Printed', 'Forgotten', 'Remaining_Duplicates', 'Date-Time', 'Empty', 'Text_Only'])
                   # Font 3
    cfg.add_option('OLED DISPLAY 2 (MODIFY)', 'oled2_font_3', "DejaVuSerif-Bold.ttf",
                   "Text-3 Font - You can add more fonts 'Truetype(.ttf)' or 'Opentype(.otf)', in the folder '~/.config/pibooth/oled_display/fonts/'",
                   "Text-3 Font", _fonts2)
                   # Text 3 color
    cfg.add_option('OLED DISPLAY 2 (MODIFY)', 'oled2_text3_color', "white",
                   "Text-3 Color - uses HTML color names. E.g. 'White', 'Red', 'Cyan', 'Silver', 'Blue', 'Grey', 'DarkBlue', 'Black', 'LightBlue', 'Orange', 'Purple', 'Brown', 'Yellow', 'Maroon', 'Lime', 'Green', 'Magenta', 'Olive'. On Monochrome displays colors will be converted to 'White')",
                   "Text-3 Color", ["White", "Red", "Cyan", "Silver", "Blue", "Grey", "DarkBlue", "Black", "LightBlue", "Orange", "Purple", "Brown", "Yellow", "Maroon", "Lime", "Green", "Magenta", "Olive"])
                   # Text 3
    cfg.add_option('OLED DISPLAY 2 (MODIFY)', 'oled2_text_3', '"Remain "',
                   'Text-3 - Text with space after to use with counter, or leave empty for counter only',
                   "Text-3 or Empty", '"Remain "')
                   # Text 3 center on display
    cfg.add_option('OLED DISPLAY 2 (MODIFY)', 'oled2_text_3_center', "No",
                   "Text-3 - Center text on display 'Yes' or 'No'",
                   "Text-3 Center", ['Yes', 'No'])
                   # Text 3 size
    cfg.add_option('OLED DISPLAY 2 (MODIFY)', 'oled2_size_3', "19",
                   'Text-3 Size - 19 is default if 3 x text/counters are used on the display at the same time',
                   "Text-3 Size", "19")
                   # Move text 3, to the right
    cfg.add_option('OLED DISPLAY 2 (MODIFY)', 'oled2_text3_right', "0",
                   "Text-3 - Move text 'Right' on display",
                   "Text-3 Move Right", "0")
                   # Move text 3 down
    cfg.add_option('OLED DISPLAY 2 (MODIFY)', 'oled2_text3_down', "46",
                   "Text-3 - Move text 'Down' on display",
                   "Text-3 Move Down", "46")


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
        # Path setup
        home_directory = os.path.expanduser('~')
        app.logo2_path = os.path.join(home_directory, ".config/pibooth/oled_display/logo/")
        app.state2_picture_path = os.path.join(home_directory, ".config/pibooth/oled_display/states/")
        app.fonts2_path = os.path.join(home_directory, ".config/pibooth/oled_display/fonts/")

        # OLED display modify
        # Logo / Fonts / States Images
        app.showlogo2 = cfg.get('OLED DISPLAY 2 (MODIFY)', 'oled2_showlogo').strip('"')
        app.logos2 = cfg.get('OLED DISPLAY 2 (MODIFY)', 'oled2_logos').strip('"')
        app.states2_pictures = cfg.get('OLED DISPLAY 2 (MODIFY)', 'oled2_states_pictures').strip('"')
        app.animated_fps2 = int(cfg.get('OLED DISPLAY 2 (MODIFY)', 'oled2_animated_fps').strip('"'))

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


class GifThread2(threading.Thread):
    def __init__(self, device, gif_path, color_mode, fps):
        super(GifThread2, self).__init__()
        self.device2 = device
        self.gif_path2 = gif_path
        self.color_mode2 = color_mode
        self.fps2 = fps
        self._stop_event = threading.Event()
        
    def stop(self):
        self._stop_event.set()

    def run(self):
        regulator = framerate_regulator(fps=self.fps2) # adjust the fps to suit your needs
        with Image.open(self.gif_path2) as im:            
            # Loop over each frame in the animated image
            for i, frame in enumerate(ImageSequence.Iterator(im)):
                # If the stop event is set, break the loop
                if self._stop_event.is_set():
                    break
                # Calculate the position to center the image
                upper_left_corner = ((self.device2.width - frame.width) // 2, (self.device2.height - frame.height) // 2)
                # Create a new image with the device's dimensions
                base_frame = Image.new(self.color_mode2, self.device2.size)
                # Paste the frame into the center of the base_frame
                base_frame.paste(frame, upper_left_corner)
                # Display the frame
                with regulator:
                    self.device2.display(base_frame)


def center_image_2(app, image2):
    W, H = app.device2.width, app.device2.height
    w, h = image2.size
    x = (W - w) // 2
    y = (H - h) // 2

    # Create blank image for drawing.
    output_image2 = Image.new(app.color2_mode, (app.device2.width, app.device2.height))
    output_image2.paste(image2, (x, y))
    return output_image2

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

    app.draw2.text((right, down), final_text, font=font, fill=color)


def write_text_to_oled_2(app, cfg):
    """Method called to write text or image on the display
    """
    try:
        # Create blank image for drawing.
        app.image2 = Image.new(app.color2_mode, (app.device2.width, app.device2.height))
        app.draw2 = ImageDraw.Draw(app.image2)
        # Load a font.
        font_1 = ImageFont.truetype(os.path.join(app.fonts_path, app.font2_1), app.size2_1)
        font_2 = ImageFont.truetype(os.path.join(app.fonts_path, app.font2_2), app.size2_2)
        font_3 = ImageFont.truetype(os.path.join(app.fonts_path, app.font2_3), app.size2_3)

        # Show logo Yes/No
        y = app.showlogo2.split()
        if "No" in y:
            c1 = app.text2_1_center.split()
            c2 = app.text2_2_center.split()
            c3 = app.text2_3_center.split()

            center1 = "Yes" in c1
            center2 = "Yes" in c2
            center3 = "Yes" in c3
            
            with canvas(app.device2) as app.draw2:
                draw_text_2(app, app.counter_type2_1, app.right2_1, app.down2_1, app.text2_1, font_1, app.text21_color, center=center1)
                draw_text_2(app, app.counter_type2_2, app.right2_2, app.down2_2, app.text2_2, font_2, app.text22_color, center=center2)
                draw_text_2(app, app.counter_type2_3, app.right2_3, app.down2_3, app.text2_3, font_3, app.text23_color, center=center3)
            # app.device2.display(app.image2)

        elif "Yes" in y:
            # Stop the previous gif thread if it exists
            if hasattr(app, 'gif_thread2') and app.gif_thread2.is_alive():
                return
                app.gif_thread2.stop()
                app.gif_thread2.join()
            # Start a new gif thread
            app.gif_thread2 = GifThread2(app.device2, os.path.join(app.logo2_path, app.logos2), app.color2_mode, app.animated_fps2)
            app.gif_thread2.start()

    except OSError:
        pass


def choose_2(app, cfg):
    """Method called to write choose state on the display
    """
    s2 = app.states2_pictures.split()
    if "Yes" in s2:
        if hasattr(app, 'gif_thread2') and app.gif_thread2.is_alive():
            app.gif_thread2.stop()
        app.image2 = Image.open(os.path.join(app.state2_picture_path, f'choose/choose_{app.device2.width}x{app.device2.height}.png')).convert(app.color2_mode)
        app.image2 = center_image_2(app, app.image2)
        app.device2.display(app.image2)
    else:
        # Write text instead of picture
        write_text_to_oled_2(app, cfg)

def chosen_2(app, cfg):
    """Method called to write chosen state on the display
    """
    s2 = app.states2_pictures.split()
    if "Yes" in s2:
        if hasattr(app, 'gif_thread2') and app.gif_thread2.is_alive():
            app.gif_thread2.stop()
        app.image2 = Image.open(os.path.join(app.state2_picture_path, f'layout/layout{app.capture_nbr}_{app.device2.width}x{app.device2.height}.png')).convert(app.color2_mode)
        app.image2 = center_image_2(app, app.image2)
        app.device2.display(app.image2)
    else:
        # Write text instead of picture
        write_text_to_oled_2(app, cfg)

def preview_2(app, cfg):
    """Method called to write preview state on the display
    """
    s2 = app.states2_pictures.split()
    if "Yes" in s2:
        if hasattr(app, 'gif_thread2') and app.gif_thread2.is_alive():
            app.gif_thread2.stop()
        app.image2 = Image.open(os.path.join(app.state2_picture_path, f'preview/preview_{app.device2.width}x{app.device2.height}.png')).convert(app.color2_mode)
        app.image2 = center_image_2(app, app.image2)
        app.device2.display(app.image2)
    else:
        # Write text instead of picture
        write_text_to_oled_2(app, cfg)

def capture_2(app, cfg):
    """Method called to write capture state on the display
    """
    s2 = app.states2_pictures.split()
    if "Yes" in s2:
        app.image2 = Image.open(os.path.join(app.state2_picture_path, f'capture/capture_{app.device2.width}x{app.device2.height}.png')).convert(app.color2_mode)
        app.image2 = center_image_2(app, app.image2)
        app.device2.display(app.image2)
    else:
        # Write text instead of picture
        write_text_to_oled_2(app, cfg)

def processing_2(app, cfg):
    """Method called to write processing state on the display
    """
    s2 = app.states2_pictures.split()
    if "Yes" in s2:
        app.image2 = Image.open(os.path.join(app.state2_picture_path, f'processing/processing_{app.device2.width}x{app.device2.height}.png')).convert(app.color2_mode)
        app.image2 = center_image_2(app, app.image2)
        app.device2.display(app.image2)
    else:
        # Write text instead of picture
        write_text_to_oled_2(app, cfg)

def print_2(app, cfg):
    """Method called to write print state on the display
    """
    s2 = app.states2_pictures.split()
    if "Yes" in s2:
        app.image2 = Image.open(os.path.join(app.state2_picture_path, f'printer/printer_{app.device2.width}x{app.device2.height}.png')).convert(app.color2_mode)
        app.image2 = center_image_2(app, app.image2)
        app.device2.display(app.image2)
    else:
        # Write text instead of picture
        write_text_to_oled_2(app, cfg)

def finish_2(app, cfg):
    """Method called to write finish state on the display
    """
    s2 = app.states2_pictures.split()
    if "Yes" in s2:
        app.image2 = Image.open(os.path.join(app.state2_picture_path, f'finished/finished_{app.device2.width}x{app.device2.height}.png')).convert(app.color2_mode)
        app.image2 = center_image_2(app, app.image2)
        app.device2.display(app.image2)
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
        if hasattr(app, 'gif_thread2') and app.gif_thread2.is_alive():
            app.gif_thread2.stop()
        app.image2 = Image.open(os.path.join(app.state2_picture_path, f'failure/failure_{app.device2.width}x{app.device2.height}.png')).convert(app.color2_mode)
        app.image2 = center_image_2(app, app.image2)
        # Display image
        app.device2.display(app.image2)
    except:
        pass
