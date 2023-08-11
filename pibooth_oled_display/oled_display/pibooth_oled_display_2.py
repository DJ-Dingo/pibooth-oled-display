# -*- coding: utf-8 -*-

"""
Pibooth Plugin to manage small OLED displays (via I2c or SPI).
Show various counters (e.g., photos taken), display time-date, 
text, logos, and animated GIFs.
"""
import os
import json
import glob
import time
import shutil
import datetime
import threading
import pkg_resources
from PIL import Image, ImageDraw, ImageFont, ImageSequence
from luma.core.sprite_system import framerate_regulator
from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1309, ssd1322, ssd1325, ssd1327, ssd1331, ssd1351, ssd1362, sh1106
import pibooth
from pibooth.utils import LOGGER


__version__ = "2.0.3"
# Github "DJ-Dingo", Kenneth Nicholas Jørgensen - Display 2


# Paths to Logo, Fonts and States
cache_dir = os.path.expanduser('~/.config/pibooth/')
user_font_dir = os.path.join(cache_dir, 'oled_display/fonts/')
user_logo_dir = os.path.join(cache_dir, 'oled_display/logo/')
user_states_dir = os.path.join(cache_dir, 'oled_display/states/')
default_font_dir = pkg_resources.resource_filename('pibooth_oled_display', 'oled_display/fonts/')
default_logo_dir = pkg_resources.resource_filename('pibooth_oled_display', 'oled_display/logo/')
default_states_dir = pkg_resources.resource_filename('pibooth_oled_display', 'oled_display/states/')
default_json_dir = pkg_resources.resource_filename('pibooth_oled_display', 'oled_display/json/')

# Subdirectories under 'states'
user_states_subdirs = ['capture', 'choose', 'failure', 'finished', 'layout', 'preview', 'printer', 'processing']

def ensure_directory(directory):
    """
    Ensure that the specified directory exists.
    If it doesn't exist, it's created.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)

# Ensure directories exist
ensure_directory(user_font_dir)
ensure_directory(user_logo_dir)
ensure_directory(user_states_dir)

# Ensure state subdirectories exist
for subdir in user_states_subdirs:
    ensure_directory(os.path.join(user_states_dir, subdir))


def get_script_version(filepath):
    """Extract the VERSION variable from a script."""
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'r') as f:
        for line in f:
            if line.startswith("__version__"):  # For .py files
                return line.split('=')[1].strip().strip('\"\'')
            elif '.. version::' in line:  # For .rst files
                return line.split('::')[1].strip()
    return None  # Return None if version is not found


def copy_files_to_config():
    dst_dir = os.path.expanduser('~/.config/pibooth/oled_display/')
    os.makedirs(dst_dir, exist_ok=True)  # Create destination directory if it doesn't exist

    files_to_copy = ['pibooth_oled_display_2.py', 'Date-Time_Format_Codes.rst']

    for file in files_to_copy:
        src_file = pkg_resources.resource_filename('pibooth_oled_display', f'oled_display/{file}')
        dst_file = os.path.join(dst_dir, file)

        src_version = get_script_version(src_file)
        dst_version = get_script_version(dst_file)

        #LOGGER.info("Checking file: %s", file)
        #LOGGER.info("Source (package) script version: %s", src_version)
        #LOGGER.info("Destination (local) script version: %s", dst_version)

        should_copy = not os.path.exists(dst_file) or src_version != dst_version
        #LOGGER.info("Should copy? %s", should_copy)

        old_version = get_script_version(dst_file)
        
        if should_copy:
            shutil.copy(src_file, dst_file)
            LOGGER.warning("Overwrote local version of")
            LOGGER.warning("'%s' ", file)
            LOGGER.warning("due to version mismatch or file not found")
            LOGGER.warning("Local: %s, Package: %s", old_version, get_script_version(src_file))

# Call the function
copy_files_to_config()

def update_json_file_2(filename, data):
    """
    This function opens JSON files and updates it with the provided data.
    :param filename: The name of the file to update
    :param data: The data to write to the file
    """
    # Construct the file path
    file_path = os.path.join(default_json_dir, filename)
    # Ensure the directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    # Open the file and write the data to it
    with open(file_path, 'w') as f:
        json.dump(data, f)

def get_files2(user_dir, default_dir, extensions, strategy):
    files = {}
    # Get the files from the user directory
    if os.path.isdir(user_dir):
        for filename in os.listdir(user_dir):
            if filename.split('.')[-1].lower() in extensions:
                files[filename] = os.path.join(user_dir, filename)

    # Get the files from the default directory
    if os.path.isdir(default_dir):
        for filename in os.listdir(default_dir):
            if filename.split('.')[-1].lower() in extensions:
                if strategy == 'include_all' and filename not in files:
                    files[filename] = os.path.join(default_dir, filename)
                elif strategy == 'overwrite':
                    files[filename] = os.path.join(default_dir, filename)
    return files

def get_state_files2(user_dir, default_dir):
    extensions = ['png']
    state_folders = ['capture', 'choose', 'failure', 'finished', 'layout', 'preview', 'printer', 'processing']
    state_files = {}
    for state in state_folders:
        user_state_dir = os.path.join(user_dir, state)
        default_state_dir = os.path.join(default_dir, state)
        # Process user directory
        if os.path.isdir(user_state_dir):
            for ext in extensions:
                for file_path in glob.glob(os.path.join(user_state_dir, '*.' + ext)):
                    file_name_with_ext = os.path.basename(file_path)
                    state_files[file_name_with_ext] = file_path

        # Process default directory (overwrites user files if they exist)
        if os.path.isdir(default_state_dir):
            for ext in extensions:
                for file_path in glob.glob(os.path.join(default_state_dir, '*.' + ext)):
                    file_name_with_ext = os.path.basename(file_path)
                    if file_name_with_ext not in state_files:
                        # Only add to state_files if it's not already there (i.e., if it wasn't in the user dir)
                        state_files[file_name_with_ext] = file_path
    return state_files


# List of fonts
fonts2 = get_files2(user_font_dir, default_font_dir, ['ttf', 'otf'], 'include_all')
# List of logos
logos2 = get_files2(user_logo_dir, default_logo_dir, ['png', 'tiff', 'gif', 'jpeg', 'jpg', 'svg', 'bmp'], 'include_all')
# List of states
states2 = get_state_files2(user_states_dir, default_states_dir)

# Create and update JSON files with the fonts, logos and states
update_json_file_2('fonts_2_cache.json', fonts2)
LOGGER.info("Updating FONTS  database for OLED display 2")
update_json_file_2('logos_2_cache.json', logos2)
LOGGER.info("Updating LOGO   database for OLED display 2")
update_json_file_2('states_2_cache.json', states2)
LOGGER.info("Updating STATES database for OLED display 2")

# Load the fonts, states and logo lists from the JSON files
with open(os.path.join(default_json_dir, 'fonts_2_cache.json')) as f:
    _fonts2 = json.load(f)  # This is now a dictionary, not a list
    _fonts2 = dict(sorted(_fonts2.items()))
with open(os.path.join(default_json_dir, 'logos_2_cache.json')) as f:
    _logos2 = json.load(f)  # This is now a dictionary, not a list
    _logos2 = dict(sorted(_logos2.items()))
with open(os.path.join(default_json_dir, 'states_2_cache.json')) as f:
    _states2 = json.load(f)  # This is now a dictionary, not a list


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
                   "Logo or Animated Gif can be placed in the folder '~/.config/pibooth/oled_display/logo/'",
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

HAS_LOGGED = False

def write_text_to_oled_2(app, cfg):
    """Method called to write text or image on the display
    """
    global HAS_LOGGED
    try:
        # Show logo Yes/No
        y = app.showlogo2.split()
        if "No" in y:
            try:
                # Create blank image for drawing.
                app.image2 = Image.new(app.color2_mode, (app.device2.width, app.device2.height))
                app.draw2 = ImageDraw.Draw(app.image2)
            except Exception as e:
                if not HAS_LOGGED:
                    LOGGER.warning("")
                    LOGGER.warning(f"OLED display 2: ERROR")
                    LOGGER.warning("Can't find device")
                    LOGGER.warning("Please check your wires to the display")
                    LOGGER.warning("")
                    HAS_LOGGED = True

            # Try to load the fonts, if any of them fails, load a default font
            try:
                if app.font2_1 not in _fonts2:
                    LOGGER.warning("")
                    LOGGER.warning("OLED display 2")
                    LOGGER.warning(f"{app.font2_1} for Font 1 not found,")
                    LOGGER.warning("using default font DejaVuSerif-Bold.ttf.")
                    LOGGER.warning("Please update the font in the configuration.")
                    LOGGER.warning("")
                    font2_1 = ImageFont.truetype(pkg_resources.resource_filename('pibooth_oled_display', 'oled_display/default/Default_DejaVuSerif-Bold.ttf'), app.size2_1)  # if error change to default font.
                else:
                    font2_1 = ImageFont.truetype(_fonts2[app.font2_1], app.size2_1)
            except IOError:
                LOGGER.warning("")
                LOGGER.warning("OLED display 2 - You removed a font")
                LOGGER.warning(f"{app.font2_1} for Font 1 not found,")
                LOGGER.warning("using default font DejaVuSerif-Bold.ttf.")
                LOGGER.warning("Please update the font in the configuration.")
                LOGGER.warning("")
                font2_1 = ImageFont.truetype(pkg_resources.resource_filename('pibooth_oled_display', 'oled_display/default/Default_DejaVuSerif-Bold.ttf'), app.size2_1)  # if error change to default font.
            try:
                if app.font2_2 not in _fonts2:
                    LOGGER.warning("")
                    LOGGER.warning("OLED display 2")
                    LOGGER.warning(f"{app.font2_2} for Font 2 not found,")
                    LOGGER.warning("using default font DejaVuSerif-Bold.ttf.")
                    LOGGER.warning("Please update the font in the configuration.")
                    LOGGER.warning("")
                    font2_2 = ImageFont.truetype(pkg_resources.resource_filename('pibooth_oled_display', 'oled_display/default/Default_DejaVuSerif-Bold.ttf'), app.size2_2)  # if error change to default font.
                else:
                    font2_2 = ImageFont.truetype(_fonts2[app.font2_2], app.size2_2)
            except IOError:
                LOGGER.warning("")
                LOGGER.warning("OLED display 2 - You removed a font")
                LOGGER.warning(f"{app.font2_2} for Font 2 not found,")
                LOGGER.warning("using default font DejaVuSerif-Bold.ttf.")
                LOGGER.warning("Please update the font in the configuration.")
                LOGGER.warning("")
                font2_2 = ImageFont.truetype(pkg_resources.resource_filename('pibooth_oled_display', 'oled_display/default/Default_DejaVuSerif-Bold.ttf'), app.size2_2)  # if error change to default font.
            try:
                if app.font2_3 not in _fonts2:
                    LOGGER.warning("")
                    LOGGER.warning("OLED display 2")
                    LOGGER.warning(f"{app.font2_3} for Font 3 not found,")
                    LOGGER.warning("using default font DejaVuSerif-Bold.ttf.")
                    LOGGER.warning("Please update the font in the configuration.")
                    LOGGER.warning("")
                    font2_3 = ImageFont.truetype(pkg_resources.resource_filename('pibooth_oled_display', 'oled_display/default/Default_DejaVuSerif-Bold.ttf'), app.size2_3)  # if error change to default font.
                else:
                    font2_3 = ImageFont.truetype(_fonts2[app.font2_3], app.size2_3)
            except IOError:
                LOGGER.warning("")
                LOGGER.warning("OLED display 2 - You removed a font")
                LOGGER.warning(f"{app.font2_3} for Font 3 not found,")
                LOGGER.warning("using default font DejaVuSerif-Bold.ttf.")
                LOGGER.warning("Please update the font in the configuration.")
                LOGGER.warning("")
                font2_3 = ImageFont.truetype(pkg_resources.resource_filename('pibooth_oled_display', 'oled_display/default/Default_DejaVuSerif-Bold.ttf'), app.size2_3)  # if error change to default font.


            c1 = app.text2_1_center.split()
            c2 = app.text2_2_center.split()
            c3 = app.text2_3_center.split()

            center1 = "Yes" in c1
            center2 = "Yes" in c2
            center3 = "Yes" in c3

            with canvas(app.device2) as app.draw2:
                draw_text_2(app, app.counter_type2_1, app.right2_1, app.down2_1, app.text2_1, font2_1, app.text21_color, center=center1)
                draw_text_2(app, app.counter_type2_2, app.right2_2, app.down2_2, app.text2_2, font2_2, app.text22_color, center=center2)
                draw_text_2(app, app.counter_type2_3, app.right2_3, app.down2_3, app.text2_3, font2_3, app.text23_color, center=center3)

        elif "Yes" in y:
            # Stop the previous gif thread if it exists
            if hasattr(app, 'gif_thread2') and app.gif_thread2.is_alive():
                return
                app.gif_thread2.stop()
                app.gif_thread2.join()

            default_logo_path = pkg_resources.resource_filename('pibooth_oled_display', 'oled_display/default/default_logo.png')
            # Try to use the selected logo, use default if it doesn't exist
            try:
                if app.logos2 not in _logos2:
                    LOGGER.warning("")
                    LOGGER.warning("OLED display 2")
                    LOGGER.warning(f"Logo {app.logos2} not found")
                    LOGGER.warning("Using default logo instead.")
                    LOGGER.warning("Please update the logo in the configuration.")
                    LOGGER.warning("")
                    app.gif_thread2 = GifThread2(app.device2, default_logo_path, app.color2_mode, app.animated_fps2)
                    app.gif_thread2.start()
                else:
                    # Start a new logo / gif thread 2
                    app.gif_thread2 = GifThread2(app.device2, _logos2[app.logos2], app.color2_mode, app.animated_fps2)
                    app.gif_thread2.start()
            except Exception as e:
                if not HAS_LOGGED:
                    LOGGER.warning("")
                    LOGGER.warning(f"OLED display 2: ERROR")
                    LOGGER.warning("Can't find device")
                    LOGGER.warning("Please check your wires to the display")
                    LOGGER.warning("")
                    HAS_LOGGED = True

    except OSError:
        pass


def choose_2(app, cfg, _states2):
    """Method called to write choose state on the display
    """
    s2 = app.states2_pictures.split()
    if "Yes" in s2:
        if hasattr(app, 'gif_thread2') and app.gif_thread2.is_alive():
            app.gif_thread2.stop()
        filename = f'choose_{app.device2.width}x{app.device2.height}.png'
        file_path = next((value for key, value in _states2.items() if key.endswith(filename)), None)
        if file_path:
            app.image2 = Image.open(file_path).convert(app.color2_mode)
        app.image2 = center_image_2(app, app.image2)
        app.device2.display(app.image2)
    else:
        # Write text instead of picture
        write_text_to_oled_2(app, cfg)


def chosen_2(app, cfg, _states2):
    """Method called to write chosen state on the display
    """
    s2 = app.states2_pictures.split()
    if "Yes" in s2:
        if hasattr(app, 'gif_thread2') and app.gif_thread2.is_alive():
            app.gif_thread2.stop()
        filename = f'layout{app.capture_nbr}_{app.device2.width}x{app.device2.height}.png'
        file_path = next((value for key, value in _states2.items() if key.endswith(filename)), None)
        if file_path:
            app.image2 = Image.open(file_path).convert(app.color2_mode)
        app.image2 = center_image_2(app, app.image2)
        app.device2.display(app.image2)
    else:
        # Write text instead of picture
        write_text_to_oled_2(app, cfg)

def preview_2(app, cfg, _states2):
    """Method called to write preview state on the display
    """
    t2 = app.states2_pictures.split()
    if "Yes" in t2:
        if hasattr(app, 'gif_thread2') and app.gif_thread2.is_alive():
            app.gif_thread2.stop()
        filename = f'preview_{app.device2.width}x{app.device2.height}.png'
        file_path = next((value for key, value in _states2.items() if key.endswith(filename)), None)
        if file_path:
            app.image2 = Image.open(file_path).convert(app.color2_mode)
        app.image2 = center_image_2(app, app.image2)
        app.device2.display(app.image2)
    else:
        # Write text instead of picture
        write_text_to_oled_2(app, cfg)

def capture_2(app, cfg, _states2):
    """Method called to write capture state on the display
    """
    s2 = app.states2_pictures.split()
    if "Yes" in s2:
        filename = f'capture_{app.device2.width}x{app.device2.height}.png'
        file_path = next((value for key, value in _states2.items() if key.endswith(filename)), None)
        if file_path:
            app.image2 = Image.open(file_path).convert(app.color2_mode)
        app.image2 = center_image_2(app, app.image2)
        app.device2.display(app.image2)
    else:
        # Write text instead of picture
        write_text_to_oled_2(app, cfg)

def processing_2(app, cfg, _states2):
    """Method called to write processing state on the display
    """
    s2 = app.states2_pictures.split()
    if "Yes" in s2:
        filename = f'processing_{app.device2.width}x{app.device2.height}.png'
        file_path = next((value for key, value in _states2.items() if key.endswith(filename)), None)
        if file_path:
            app.image2 = Image.open(file_path).convert(app.color2_mode)
        app.image2 = center_image_2(app, app.image2)
        app.device2.display(app.image2)
    else:
        # Write text instead of picture
        write_text_to_oled_2(app, cfg)

def print_2(app, cfg, _states2):
    """Method called to write print state on the display
    """
    s2 = app.states2_pictures.split()
    if "Yes" in s2:
        filename = f'printer_{app.device2.width}x{app.device2.height}.png'
        file_path = next((value for key, value in _states2.items() if key.endswith(filename)), None)
        if file_path:
            app.image2 = Image.open(file_path).convert(app.color2_mode)
        app.image2 = center_image_2(app, app.image2)
        app.device2.display(app.image2)
    else:
        # Write text instead of picture
        write_text_to_oled_2(app, cfg)

def finish_2(app, cfg, _states2):
    """Method called to write finish state on the display
    """
    s2 = app.states2_pictures.split()
    if "Yes" in s2:
        filename = f'finished_{app.device2.width}x{app.device2.height}.png'
        file_path = next((value for key, value in _states2.items() if key.endswith(filename)), None)
        if file_path:
            app.image2 = Image.open(file_path).convert(app.color2_mode)
        app.image2 = center_image_2(app, app.image2)
        app.device2.display(app.image2)
    else:
        # Write text instead of picture
        write_text_to_oled_2(app, cfg)

def failure_2(app, cfg, _states):
    """Method called to write finish state on the display
    """
    if hasattr(app, 'gif_thread2') and app.gif_thread2.is_alive():
        app.gif_thread2.stop()
    filename = f'failure_{app.device2.width}x{app.device2.height}.png'
    file_path = next((value for key, value in _states2.items() if key.endswith(filename)), None)
    if file_path:
        app.image2 = Image.open(file_path).convert(app.color2_mode)
    app.image2 = center_image_2(app, app.image2)
    # Display image
    app.device2.display(app.image2)



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
        choose_2(app, cfg, _states2)
    except:
        pass

@pibooth.hookimpl
def state_choose_do(app, cfg):
    # Write to the display at choose_do
    try:
        choose_2(app, cfg, _states2)
    except:
        pass

@pibooth.hookimpl
def state_choose_exit(app, cfg):
    # Write to the display at choose_exit
    try:
        choose_2(app, cfg, _states2)
    except:
        pass


####### CHOSEN ###############################
@pibooth.hookimpl
def state_chosen_enter(app, cfg):
    # Write to the display at chosen enter
    try:
        chosen_2(app, cfg, _states2)
    except:
        pass

@pibooth.hookimpl
def state_chosen_do(app, cfg):
    # Write to the display at chosen_do
    try:
        chosen_2(app, cfg, _states2)
    except:
        pass

@pibooth.hookimpl
def state_chosen_exit(app, cfg):
    # Write to the display at chosen_exit
    try:
        chosen_2(app, cfg, _states2)
    except:
        pass


####### PREVIEW ###############################
@pibooth.hookimpl
def state_preview_enter(app, cfg):
    # Write to the display at preview_enter
    try:
        preview_2(app, cfg, _states2)
    except:
        pass

@pibooth.hookimpl
def state_preview_do(app, cfg):
    # Write to the display at preview_do
    try:
        preview_2(app, cfg, _states2)
    except:
        pass

@pibooth.hookimpl
def state_preview_exit(app, cfg):
    # Write to the display at preview_exit
    try:
        preview_2(app, cfg, _states2)
    except:
        pass


####### CAPTURE ###############################
def state_capture_enter(app, cfg):
    # Write to the display at capture_enter
    try:
        capture_2(app, cfg, _states2)
    except:
        pass

@pibooth.hookimpl
def state_capture_do(app, cfg):
    # Write to the display at capture_do
    try:
        capture_2(app, cfg, _states2)
    except:
        pass

@pibooth.hookimpl
def state_capture_exit(app, cfg):
    # Write to the display at capture_exit
    try:
        capture_2(app, cfg, _states2)
    except:
        pass


####### PROCESSING #############################
@pibooth.hookimpl
def state_processing_enter(app, cfg):
    # Write to the display at processing_enter
    try:
        processing_2(app, cfg, _states2)
    except:
        pass

@pibooth.hookimpl
def state_processing_do(app, cfg):
    # Write to the display at processing_do
    try:
        processing_2(app, cfg, _states2)
    except:
        pass

@pibooth.hookimpl
def state_processing_exit(app, cfg):
    # Write to the display at processing_exit
    try:
        processing_2(app, cfg, _states2)
    except:
        pass


####### PRINT #################################
@pibooth.hookimpl
def state_print_enter(app, cfg):
    # Write to the display at print_enter
    try:
        print_2(app, cfg, _states2)
    except:
        pass

@pibooth.hookimpl
def state_print_do(app, cfg):
    # Write to the display at print_do
    try:
        print_2(app, cfg, _states2)
    except:
        pass

@pibooth.hookimpl
def state_print_exit(app, cfg):
    # Write to the display at print_exit
    try:
        print_2(app, cfg, _states2)
    except:
        pass


####### FINISH #################################
@pibooth.hookimpl
def state_finish_enter(app, cfg):
    # Write to the display at finish_enter
    try:
        finish_2(app, cfg, _states2)
    except:
        pass

@pibooth.hookimpl
def state_finish_do(app, cfg):
    # Write to the display at finish_do
    try:
        finish_2(app, cfg, _states2)
    except:
        pass

@pibooth.hookimpl
def state_finish_exit(app, cfg):
    # Write to the display at finish_exit
    try:
        finish_2(app, cfg, _states2)
    except:
        pass

####### FAILSAFE ###############################
@pibooth.hookimpl
def state_failsafe_enter(app):
    # Write to the display 2 at failsafe_enter
    try:
        failure_2(app, cfg, _states2)
    except:
        pass

@pibooth.hookimpl
def state_failsafe_do(app):
    # Write to the display 2 at failsafe_do
    try:
        failure_2(app, cfg, _states2)
    except:
        pass

####### CLEANUP ###############################
@pibooth.hookimpl
def pibooth_cleanup(app):
    # Turn off OLED display 2 at pibooth close
    try:
        if hasattr(app, 'gif_thread2') and app.gif_thread2.is_alive():
            app.gif_thread2.stop()
    except OSError:
        pass
