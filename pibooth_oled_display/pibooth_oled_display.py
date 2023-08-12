# -*- coding: utf-8 -*-

"""Pibooth Plugin to manage small OLED displays (via I2c or SPI). Show various counters (e.g., photos taken), display time-date, text, logos, and animated GIFs."""
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
# Github "DJ-Dingo", Kenneth Nicholas Jørgensen - Display 1


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


def update_json_file(filename, data):
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

def get_files(user_dir, default_dir, extensions, strategy):
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

def get_state_files(user_dir, default_dir):
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
fonts = get_files(user_font_dir, default_font_dir, ['ttf', 'otf'], 'include_all')
# List of logos
logos = get_files(user_logo_dir, default_logo_dir, ['png', 'tiff', 'gif', 'jpeg', 'jpg', 'svg', 'bmp'], 'include_all')
# List of states
states = get_state_files(user_states_dir, default_states_dir)

# Create and update JSON files with the fonts, logos and states
update_json_file('fonts_1_cache.json', fonts)
LOGGER.info("Updating FONTS  database for OLED display 1")
update_json_file('logos_1_cache.json', logos)
LOGGER.info("Updating LOGO   database for OLED display 1")
update_json_file('states_1_cache.json', states)
LOGGER.info("Updating STATES database for OLED display 1")

# Load the fonts, states and logo lists from the JSON files
with open(os.path.join(default_json_dir, 'fonts_1_cache.json')) as f:
    _fonts = json.load(f)  # This is now a dictionary, not a list
    _fonts = dict(sorted(_fonts.items()))
with open(os.path.join(default_json_dir, 'logos_1_cache.json')) as f:
    _logos = json.load(f)  # This is now a dictionary, not a list
    _logos = dict(sorted(_logos.items()))
with open(os.path.join(default_json_dir, 'states_1_cache.json')) as f:
    _states = json.load(f)  # This is now a dictionary, not a list


@pibooth.hookimpl
def pibooth_configure(cfg):
    """Declare the new configuration options"""
                   # Devices SETUP
    cfg.add_option('OLED DISPLAY - (SETUP)', 'oled_devices', "ssd1306",
                   "Choose OLED device - 'ssd1306 (Default)', 'ssd1309', 'ssd1322', 'ssd1325', 'ssd1327', 'ssd1331', 'ssd1362', 'sh1106'",
                   "Choose OLED device", ["ssd1306", "ssd1309", "ssd1322", "ssd1325", "ssd1327", "ssd1331", "ssd1362", "sh1106"])
                   # I2c or SPI
    cfg.add_option('OLED DISPLAY - (SETUP)', 'oled_i2c_or_spi', "I2c",
                   "Display connection 'I2c' or 'SPI'",
                   "I2c or SPI connection", ["SPI", "I2c"])
                   # I2c address
    cfg.add_option('OLED DISPLAY - (SETUP)', 'oled_port_address', "0x3c",
                   'I2c address (Default=0x3c)',
                   "I2c address", "0x3c")
                   # Device number
    cfg.add_option('OLED DISPLAY - (SETUP)', 'oled_spi_device_number', "0",
                   "Change SPI device number '0', '1' or '2' (Default = 0)",
                   "SPI device number 0, 1, 2", ["0", "1", "2"])
                   # Port
    cfg.add_option('OLED DISPLAY - (SETUP)', 'oled_port', "1",
                   "Change the I2c or SPI port number - (I2c = '1' - SPI = '0', '1', '2')",
                   "Port - I2c(1) or SPI(0)", ["0", "1", "2"])
                   # DC pin
    cfg.add_option('OLED DISPLAY - (SETUP)', 'oled_spi_gpio_dc_pin', "24",
                   "SPI only GPIO DC PIN (Default=24)",
                   "SPI only GPIO DC PIN (24)", "24")
                   # Reset pin
    cfg.add_option('OLED DISPLAY - (SETUP)', 'oled_spi_gpio_rst_pin', "25",
                   "SPI only GPIO RST PIN (Default=25)",
                   "SPI only GPIO RST PIN (25)", "25")
                   # Display size   
    cfg.add_option('OLED DISPLAY - (SETUP)', 'oled_width', "128",
                   "Change screen WIDTH - '32', '48', '64', '80', '96', '128(Default)', '160', '240', '256', '320'",
                   "OLED screen width", ["32", "48", "64", "80", "96", "128", "160", "240", "256", "320"])
    cfg.add_option('OLED DISPLAY - (SETUP)', 'oled_height', "64",
                   "Change screen HEIGHT - '32', '48', '64(Default)', '80', '96', '128', '160', '240', '256', '320'",
                   "OLED screen height", ["32", "48", "64", "80", "96", "128", "160", "240", "256", "320"])
                   # Color mode
    cfg.add_option('OLED DISPLAY - (SETUP)', 'oled_color_mode', "1",
                   "Color mode - '1 = Monochrome (Default)', 'RGB', 'RGBA'",
                   "Color mode (Monochrome = 1)", ["1", "RGB", "RGBA"])
                   # Rotate screen
    cfg.add_option('OLED DISPLAY - (SETUP)', 'oled_rotate', "0",
                   "Rotate screen - '0 (Default)', '1', '2', '3'",
                   "Rotate screen - 0 or 2", ["0", "1", "2", "3"])
                   # TEXT SETUP
                   # States Yes/No
    cfg.add_option('OLED DISPLAY - (MODIFY)', 'oled_states_pictures', "Yes",
                   "Show state pictures - 'Yes' or 'No'",
                   "Show state pictures", ['Yes', 'No'])
                   # Logo or animated gif
    cfg.add_option('OLED DISPLAY - (MODIFY)', 'oled_showlogo', "No",
                   "Show Logo or Animated Gif (instead of text) - 'Yes' or 'No'",
                   "Logo instead of text", ['Yes', 'No'])
    cfg.add_option('OLED DISPLAY - (MODIFY)', 'oled_logos', "128x64_Pibooth_2.gif",
                   "Logo or Animated Gif can be placed in the folder '~/.config/pibooth/oled_display/logo/'",
                   "Logo or Animated Gif", _logos)
                   # FPS
    cfg.add_option('OLED DISPLAY - (MODIFY)', 'oled_animated_fps', "15",
                   "FPS (Frames Per Second) speed for Animated Gif",
                   "FPS for Animated Gif", "15")
                   # Choose Text 1, Counters 1, Date-Time 1
    cfg.add_option('OLED DISPLAY - (MODIFY)', 'oled_counter_type1', "Taken_Photo",
                   "Text-1 - Counters, Text, Date-Time - Could be either 'Taken_Photo', 'Printed', 'Forgotten', 'Remaining_Duplicates', 'Date-Time', 'Empty', 'Text_Only'",
                   "Text-1 Counter/Time", ['Taken_Photo', 'Printed', 'Forgotten', 'Remaining_Duplicates', 'Date-Time', 'Empty','Text_Only'])
                   # Font 1
    cfg.add_option('OLED DISPLAY - (MODIFY)', 'oled_font_1', "DejaVuSerif-Bold.ttf",
                   "Text-1 Font - You can add more fonts 'Truetype(.ttf)' or 'Opentype(.otf)', in the folder '~/.config/pibooth/oled_display/fonts/'",
                   "Text-1 Font", _fonts)
                   # Text 1 color
    cfg.add_option('OLED DISPLAY - (MODIFY)', 'oled_text1_color', "white",
                   "Text-1 Color - uses HTML color names. E.g. 'White', 'Red', 'Cyan', 'Silver', 'Blue', 'Grey', 'DarkBlue', 'Black', 'LightBlue', 'Orange', 'Purple', 'Brown', 'Yellow', 'Maroon', 'Lime', 'Green', 'Magenta', 'Olive'. On Monochrome displays colors will be converted to 'White')",
                   "Text-1 Color", ["White", "Red", "Cyan", "Silver", "Blue", "Grey", "DarkBlue", "Black", "LightBlue", "Orange", "Purple", "Brown", "Yellow", "Maroon", "Lime", "Green", "Magenta", "Olive"])
                   # Text 1
    cfg.add_option('OLED DISPLAY - (MODIFY)', 'oled_text_1', '"Photos  "',
                   'Text-1 - Text with space after to use with counter, or leave empty for counter only',
                   "Text-1 or Empty", '"Photos  "')
                   # Text 1 center on display
    cfg.add_option('OLED DISPLAY - (MODIFY)', 'oled_text_1_center', "No",
                   "Text-1 - Center text on display 'Yes' or 'No'",
                   "Text-1 Center", ['Yes', 'No'])
                   # Text 1 size
    cfg.add_option('OLED DISPLAY - (MODIFY)', 'oled_size_1', "19",
                   'Text-1 Size - 19 is default if 3 x text/counters are used on the display at the same time',
                   "Text-1 Size", "19")
                   # Move text 1 to the right
    cfg.add_option('OLED DISPLAY - (MODIFY)', 'oled_text1_right', "0",
                   "Text-1 - Move text 'Right' on display",
                   "Text-1 Move Right", "0")
                   # Move text 1 down
    cfg.add_option('OLED DISPLAY - (MODIFY)', 'oled_text1_down', "0",
                   "Text-1 - Move text 'Down' on display",
                   "Text-1 Move Down", "0")
                   # Choose Text 2, Counters 2, Date-Time 2
    cfg.add_option('OLED DISPLAY - (MODIFY)', 'oled_counter_type2', "Printed",
                   "Text-2 - Counters, Text, Date-Time - Could be either 'Taken_Photo', 'Printed', 'Forgotten', 'Remaining_Duplicates', 'Date-Time', 'Empty', 'Text_Only'",
                   "Text-2 Counter/Time", ['Taken_Photo', 'Printed', 'Forgotten', 'Remaining_Duplicates', 'Date-Time', 'Empty', 'Text_Only'])
                   # Font 2
    cfg.add_option('OLED DISPLAY - (MODIFY)', 'oled_font_2', "DejaVuSerif-Bold.ttf",
                   "Text-2 Font - You can add more fonts 'Truetype(.ttf)' or 'Opentype(.otf)', in the folder '~/.config/pibooth/oled_display/fonts/'",
                   "Text-2 Font", _fonts)
                   # Text 2 color
    cfg.add_option('OLED DISPLAY - (MODIFY)', 'oled_text2_color', "white",
                   "Text-2 Color - uses HTML color names. E.g. 'White', 'Red', 'Cyan', 'Silver', 'Blue', 'Grey', 'DarkBlue', 'Black', 'LightBlue', 'Orange', 'Purple', 'Brown', 'Yellow', 'Maroon', 'Lime', 'Green', 'Magenta', 'Olive'. On Monochrome displays colors will be converted to 'White')",
                   "Text-2 Color", ["White", "Red", "Cyan", "Silver", "Blue", "Grey", "DarkBlue", "Black", "LightBlue", "Orange", "Purple", "Brown", "Yellow", "Maroon", "Lime", "Green", "Magenta", "Olive"])
                   # Text 2
    cfg.add_option('OLED DISPLAY - (MODIFY)', 'oled_text_2', '"Printed "',
                   'Text-2 - Text with space after to use with counter, or leave empty for counter only',
                   "Text-2 or Empty", '"Printed "')
                   # Text 2 center on display
    cfg.add_option('OLED DISPLAY - (MODIFY)', 'oled_text_2_center', "No",
                   "Text-2 - Center text on display 'Yes' or 'No'",
                   "Text-2 Center", ['Yes', 'No'])
                   # Text 2 size
    cfg.add_option('OLED DISPLAY - (MODIFY)', 'oled_size_2', "19",
                   'Text-2 Size - 19 is default if 3 x text/counters are used on the display at the same time',
                   "Text-2 Size", "19")
                   # Move text 2 to the right
    cfg.add_option('OLED DISPLAY - (MODIFY)', 'oled_text2_right', "0",
                   "Text-2 - Move text 'Right' on display",
                   "Text-2 Move Right", "0")
                   # Move text 2 down
    cfg.add_option('OLED DISPLAY - (MODIFY)', 'oled_text2_down', "23",
                   "Text-2 - Move text 'Down' on display",
                   "Text-2 Move Down", "23")
                   # Choose Text 3, Counters 3, Date-Time 3
    cfg.add_option('OLED DISPLAY - (MODIFY)', 'oled_counter_type3', "Remaining_Duplicates",
                   "Text-3, Counter, Date-Time - Could be either 'Taken_Photo', 'Printed', 'Forgotten', 'Remaining_Duplicates', 'Date-Time', 'Empty', 'Text_Only'",
                   "Text-3 Counter/Time", ['Taken_Photo', 'Printed', 'Forgotten', 'Remaining_Duplicates', 'Date-Time', 'Empty', 'Text_Only'])
                   # Font 3
    cfg.add_option('OLED DISPLAY - (MODIFY)', 'oled_font_3', "DejaVuSerif-Bold.ttf",
                   "Text-3 Font - You can add more fonts 'Truetype(.ttf)' or 'Opentype(.otf)', in the folder '~/.config/pibooth/oled_display/fonts/'",
                   "Text-3 Font", _fonts)
                   # Text 3 color
    cfg.add_option('OLED DISPLAY - (MODIFY)', 'oled_text3_color', "white",
                   "Text-3 Color - uses HTML color names. E.g. 'White', 'Red', 'Cyan', 'Silver', 'Blue', 'Grey', 'DarkBlue', 'Black', 'LightBlue', 'Orange', 'Purple', 'Brown', 'Yellow', 'Maroon', 'Lime', 'Green', 'Magenta', 'Olive'. On Monochrome displays colors will be converted to 'White')",
                   "Text-3 Color", ["White", "Red", "Cyan", "Silver", "Blue", "Grey", "DarkBlue", "Black", "LightBlue", "Orange", "Purple", "Brown", "Yellow", "Maroon", "Lime", "Green", "Magenta", "Olive"])
                   # Text 3
    cfg.add_option('OLED DISPLAY - (MODIFY)', 'oled_text_3', '"Remain "',
                   'Text-3 - Text with space after to use with counter, or leave empty for counter only',
                   "Text-3 or Empty", '"Remain "')
                   # Text 3 center on display
    cfg.add_option('OLED DISPLAY - (MODIFY)', 'oled_text_3_center', "No",
                   "Text-3 - Center text on display 'Yes' or 'No'",
                   "Text-3 Center", ['Yes', 'No'])
                   # Text 3 size
    cfg.add_option('OLED DISPLAY - (MODIFY)', 'oled_size_3', "19",
                   'Text-3 Size - 19 is default if 3 x text/counters are used on the display at the same time',
                   "Text-3 Size", "19")
                   # Move text 3, to the right
    cfg.add_option('OLED DISPLAY - (MODIFY)', 'oled_text3_right', "0",
                   "Text-3 - Move text 'Right' on display",
                   "Text-3 Move Right", "0")
                   # Move text 3 down
    cfg.add_option('OLED DISPLAY - (MODIFY)', 'oled_text3_down', "46",
                   "Text-3 - Move text 'Down' on display",
                   "Text-3 Move Down", "46")

def connect_oled_i2c_spi(app, cfg):
    """connect to oled I2c SPI"""
    try:
        # OLED DISPLAY - (SETUP)
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

        # OLED display modify
        # Logo / Fonts / States Images
        app.showlogo = cfg.get('OLED DISPLAY - (MODIFY)', 'oled_showlogo').strip('"')
        app.logos = cfg.get('OLED DISPLAY - (MODIFY)', 'oled_logos').strip('"')
        app.states_pictures = cfg.get('OLED DISPLAY - (MODIFY)', 'oled_states_pictures').strip('"')
        app.animated_fps = int(cfg.get('OLED DISPLAY - (MODIFY)', 'oled_animated_fps').strip('"'))

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


class GifThread(threading.Thread):
    def __init__(self, device, gif_path, color_mode, fps):
        super(GifThread, self).__init__()
        self.device = device
        self.gif_path = gif_path
        self.color_mode = color_mode
        self.fps = fps
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def run(self):
        regulator = framerate_regulator(fps=self.fps) # adjust the fps to suit your needs
        with Image.open(self.gif_path) as im:            
            # Loop over each frame in the animated image
            for i, frame in enumerate(ImageSequence.Iterator(im)):
                # If the stop event is set, break the loop
                if self._stop_event.is_set():
                    break
                # Calculate the position to center the image
                upper_left_corner = ((self.device.width - frame.width) // 2, (self.device.height - frame.height) // 2)
                # Create a new image with the device's dimensions
                base_frame = Image.new(self.color_mode, self.device.size)
                # Paste the frame into the center of the base_frame
                base_frame.paste(frame, upper_left_corner)
                # Display the frame
                with regulator:
                    self.device.display(base_frame)


def center_image(app, image):
    W, H = app.device.width, app.device.height
    w, h = image.size
    x = (W - w) // 2
    y = (H - h) // 2

    # Create blank image for drawing.
    output_image = Image.new(app.color_mode, (app.device.width, app.device.height))
    output_image.paste(image, (x, y))
    return output_image

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

HAS_LOGGED = False

def write_text_to_oled(app, cfg):
    """Method called to write text or image on the display
    """
    global HAS_LOGGED
    try:
        # Show logo Yes/No
        y = app.showlogo.split()
        if "No" in y:
            try:
                # Create blank image for drawing.
                app.image = Image.new(app.color_mode, (app.device.width, app.device.height))
                app.draw = ImageDraw.Draw(app.image)
            except Exception as e:
                if not HAS_LOGGED:
                    LOGGER.warning("")
                    LOGGER.warning(f"OLED display 1: ERROR")
                    LOGGER.warning("Can't find device")
                    LOGGER.warning("Please check your wires to the display")
                    LOGGER.warning("")
                    HAS_LOGGED = True

            # Try to load the fonts, if any of them fails, load a default font
            try:
                if app.font_1 not in _fonts:
                    LOGGER.warning("")
                    LOGGER.warning("OLED display 1")
                    LOGGER.warning(f"{app.font_1} for Font 1 not found,")
                    LOGGER.warning("using default font DejaVuSerif-Bold.ttf.")
                    LOGGER.warning("Please update the font in the configuration.")
                    LOGGER.warning("")
                    font_1 = ImageFont.truetype(pkg_resources.resource_filename('pibooth_oled_display', 'oled_display/default/Default_DejaVuSerif-Bold.ttf'), app.size_1)  # if error change to default font.
                else:
                    font_1 = ImageFont.truetype(_fonts[app.font_1], app.size_1)
            except IOError:
                LOGGER.warning("")
                LOGGER.warning("OLED display 1 - You removed a font")
                LOGGER.warning(f"{app.font_1} for Font 1 not found,")
                LOGGER.warning("using default font DejaVuSerif-Bold.ttf.")
                LOGGER.warning("Please update the font in the configuration.")
                LOGGER.warning("")
                font_1 = ImageFont.truetype(pkg_resources.resource_filename('pibooth_oled_display', 'oled_display/default/Default_DejaVuSerif-Bold.ttf'), app.size_1)  # if error change to default font.
            try:
                if app.font_2 not in _fonts:
                    LOGGER.warning("")
                    LOGGER.warning("OLED display 1")
                    LOGGER.warning(f"{app.font_2} for Font 2 not found,")
                    LOGGER.warning("using default font DejaVuSerif-Bold.ttf.")
                    LOGGER.warning("Please update the font in the configuration.")
                    LOGGER.warning("")
                    font_2 = ImageFont.truetype(pkg_resources.resource_filename('pibooth_oled_display', 'oled_display/default/Default_DejaVuSerif-Bold.ttf'), app.size_2)  # if error change to default font.
                else:
                    font_2 = ImageFont.truetype(_fonts[app.font_2], app.size_2)
            except IOError:
                LOGGER.warning("")
                LOGGER.warning("OLED display 1 - You removed a font")
                LOGGER.warning(f"{app.font_2} for Font 2 not found,")
                LOGGER.warning("using default font DejaVuSerif-Bold.ttf.")
                LOGGER.warning("Please update the font in the configuration.")
                LOGGER.warning("")
                font_2 = ImageFont.truetype(pkg_resources.resource_filename('pibooth_oled_display', 'oled_display/default/Default_DejaVuSerif-Bold.ttf'), app.size_2)  # if error change to default font.
            try:
                if app.font_3 not in _fonts:
                    LOGGER.warning("")
                    LOGGER.warning("OLED display 1")
                    LOGGER.warning(f"{app.font_3} for Font 3 not found,")
                    LOGGER.warning("using default font DejaVuSerif-Bold.ttf.")
                    LOGGER.warning("Please update the font in the configuration.")
                    LOGGER.warning("")
                    font_3 = ImageFont.truetype(pkg_resources.resource_filename('pibooth_oled_display', 'oled_display/default/Default_DejaVuSerif-Bold.ttf'), app.size_3)  # if error change to default font.
                else:
                    font_3 = ImageFont.truetype(_fonts[app.font_3], app.size_3)
            except IOError:
                LOGGER.warning("")
                LOGGER.warning("OLED display 1 - You removed a font")
                LOGGER.warning(f"{app.font_3} for Font 3 not found,")
                LOGGER.warning("using default font DejaVuSerif-Bold.ttf.")
                LOGGER.warning("Please update the font in the configuration.")
                LOGGER.warning("")
                font_3 = ImageFont.truetype(pkg_resources.resource_filename('pibooth_oled_display', 'oled_display/default/Default_DejaVuSerif-Bold.ttf'), app.size_3)  # if error change to default font.


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

        elif "Yes" in y:
            # Stop the previous gif thread if it exists
            if hasattr(app, 'gif_thread') and app.gif_thread.is_alive():
                return
                app.gif_thread.stop()
                app.gif_thread.join()

            default_logo_path = pkg_resources.resource_filename('pibooth_oled_display', 'oled_display/default/default_logo.png')
            # Try to use the selected logo, use default if it doesn't exist
            try:
                if app.logos not in _logos:
                    LOGGER.warning("")
                    LOGGER.warning("OLED display 1")
                    LOGGER.warning(f"Logo {app.logos} not found")
                    LOGGER.warning("Using default logo instead.")
                    LOGGER.warning("Please update the logo in the configuration.")
                    LOGGER.warning("")
                    app.gif_thread = GifThread(app.device, default_logo_path, app.color_mode, app.animated_fps)
                    app.gif_thread.start()
                else:
                    # Start a new logo / gif thread
                    app.gif_thread = GifThread(app.device, _logos[app.logos], app.color_mode, app.animated_fps)
                    app.gif_thread.start()
            except Exception as e:
                if not HAS_LOGGED:
                    LOGGER.warning("")
                    LOGGER.warning(f"OLED display 1: ERROR")
                    LOGGER.warning("Can't find device")
                    LOGGER.warning("Please check your wires to the display")
                    LOGGER.warning("")
                    HAS_LOGGED = True

    except OSError:
        pass


def choose(app, cfg, _states):
    """Method called to write choose state on the display
    """
    s = app.states_pictures.split()
    if "Yes" in s:
        if hasattr(app, 'gif_thread') and app.gif_thread.is_alive():
            app.gif_thread.stop()
        filename = f'choose_{app.device.width}x{app.device.height}.png'
        file_path = next((value for key, value in _states.items() if key.endswith(filename)), None)
        if file_path:
            app.image = Image.open(file_path).convert(app.color_mode)
        app.image = center_image(app, app.image)
        app.device.display(app.image)
    else:
        # Write text instead of picture
        write_text_to_oled(app, cfg)

def chosen(app, cfg, _states):
    """Method called to write chosen state on the display
    """
    s = app.states_pictures.split()
    if "Yes" in s:
        if hasattr(app, 'gif_thread') and app.gif_thread.is_alive():
            app.gif_thread.stop()
        filename = f'layout{app.capture_nbr}_{app.device.width}x{app.device.height}.png'
        file_path = next((value for key, value in _states.items() if key.endswith(filename)), None)
        if file_path:
            app.image = Image.open(file_path).convert(app.color_mode)
        app.image = center_image(app, app.image)
        app.device.display(app.image)
    else:
        # Write text instead of picture
        write_text_to_oled(app, cfg)

def preview(app, cfg, _states):
    """Method called to write preview state on the display
    """
    t = app.states_pictures.split()
    if "Yes" in t:
        if hasattr(app, 'gif_thread') and app.gif_thread.is_alive():
            app.gif_thread.stop()

        filename = f'preview_{app.device.width}x{app.device.height}.png'
        file_path = next((value for key, value in _states.items() if key.endswith(filename)), None)
        if file_path:
            app.image = Image.open(file_path).convert(app.color_mode)
        app.image = center_image(app, app.image)
        app.device.display(app.image)
    else:
        # Write text instead of picture
        write_text_to_oled(app, cfg)

def capture(app, cfg, _states):
    """Method called to write capture state on the display
    """
    s = app.states_pictures.split()
    if "Yes" in s:
        filename = f'capture_{app.device.width}x{app.device.height}.png'
        file_path = next((value for key, value in _states.items() if key.endswith(filename)), None)
        if file_path:
            app.image = Image.open(file_path).convert(app.color_mode)
        app.image = center_image(app, app.image)
        app.device.display(app.image)
    else:
        # Write text instead of picture
        write_text_to_oled(app, cfg)

def processing(app, cfg, _states):
    """Method called to write processing state on the display
    """
    s = app.states_pictures.split()
    if "Yes" in s:
        filename = f'processing_{app.device.width}x{app.device.height}.png'
        file_path = next((value for key, value in _states.items() if key.endswith(filename)), None)
        if file_path:
            app.image = Image.open(file_path).convert(app.color_mode)
        app.image = center_image(app, app.image)
        app.device.display(app.image)
    else:
        # Write text instead of picture
        write_text_to_oled(app, cfg)

def print_(app, cfg, _states):
    """Method called to write print state on the display
    """
    s = app.states_pictures.split()
    if "Yes" in s:
        filename = f'printer_{app.device.width}x{app.device.height}.png'
        file_path = next((value for key, value in _states.items() if key.endswith(filename)), None)
        if file_path:
            app.image = Image.open(file_path).convert(app.color_mode)
        app.image = center_image(app, app.image)
        app.device.display(app.image)
    else:
        # Write text instead of picture
        write_text_to_oled(app, cfg)

def finish(app, cfg, _states):
    """Method called to write finish state on the display
    """
    s = app.states_pictures.split()
    if "Yes" in s:
        filename = f'finished_{app.device.width}x{app.device.height}.png'
        file_path = next((value for key, value in _states.items() if key.endswith(filename)), None)
        if file_path:
            app.image = Image.open(file_path).convert(app.color_mode)
        app.image = center_image(app, app.image)
        app.device.display(app.image)
    else:
        # Write text instead of picture
        write_text_to_oled(app, cfg)

def failure(app, cfg, _states):
    """Method called to write finish state on the display
    """
    if hasattr(app, 'gif_thread') and app.gif_thread.is_alive():
        app.gif_thread.stop()
    filename = f'failure_{app.device.width}x{app.device.height}.png'
    file_path = next((value for key, value in _states.items() if key.endswith(filename)), None)
    if file_path:
        app.image = Image.open(file_path).convert(app.color_mode)
    app.image = center_image(app, app.image)
    # Display image
    app.device.display(app.image)



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
        choose(app, cfg, _states)
    except:
        pass

@pibooth.hookimpl
def state_choose_do(app, cfg):
    # Write to the display at choose_do
    try:
        choose(app, cfg, _states)
    except:
        pass

@pibooth.hookimpl
def state_choose_exit(app, cfg):
    # Write to the display at choose_exit
    try:
        choose(app, cfg, _states)
    except:
        pass


####### CHOSEN ###############################
@pibooth.hookimpl
def state_chosen_enter(app, cfg):
    # Write to the display at chosen enter
    try:
        chosen(app, cfg, _states)
    except:
        pass

@pibooth.hookimpl
def state_chosen_do(app, cfg):
    # Write to the display at chosen_do
    try:
        chosen(app, cfg, _states)
    except:
        pass

@pibooth.hookimpl
def state_chosen_exit(app, cfg):
    # Write to the display at chosen_exit
    try:
        chosen(app, cfg, _states)
    except:
        pass


####### PREVIEW ###############################
@pibooth.hookimpl
def state_preview_enter(app, cfg):
    # Write to the display at preview_enter
    try:
        preview(app, cfg, _states)
    except:
        pass

@pibooth.hookimpl
def state_preview_do(app, cfg):
    # Write to the display at preview_do
    try:
        preview(app, cfg, _states)
    except:
        pass

@pibooth.hookimpl
def state_preview_exit(app, cfg):
    # Write to the display at preview_exit
    try:
        preview(app, cfg, _states)
    except:
        pass


####### CAPTURE ###############################
def state_capture_enter(app, cfg):
    # Write to the display at capture_enter
    try:
        capture(app, cfg, _states)
    except:
        pass

@pibooth.hookimpl
def state_capture_do(app, cfg):
    # Write to the display at capture_do
    try:
        capture(app, cfg, _states)
    except:
        pass

@pibooth.hookimpl
def state_capture_exit(app, cfg):
    # Write to the display at capture_exit
    try:
        capture(app, cfg, _states)
    except:
        pass


####### PROCESSING #############################
@pibooth.hookimpl
def state_processing_enter(app, cfg):
    # Write to the display at processing_enter
    try:
        processing(app, cfg, _states)
    except:
        pass

@pibooth.hookimpl
def state_processing_do(app, cfg):
    # Write to the display at processing_do
    try:
        processing(app, cfg, _states)
    except:
        pass

@pibooth.hookimpl
def state_processing_exit(app, cfg):
    # Write to the display at processing_exit
    try:
        processing(app, cfg, _states)
    except:
        pass


####### PRINT #################################
@pibooth.hookimpl
def state_print_enter(app, cfg):
    # Write to the display at print_enter
    try:
        print_(app, cfg, _states)
    except:
        pass

@pibooth.hookimpl
def state_print_do(app, cfg):
    # Write to the display at print_do
    try:
        print_(app, cfg, _states)
    except:
        pass

@pibooth.hookimpl
def state_print_exit(app, cfg):
    # Write to the display at print_exit
    try:
        print_(app, cfg, _states)
    except:
        pass


####### FINISH #################################
@pibooth.hookimpl
def state_finish_enter(app, cfg):
    # Write to the display at finish_enter
    try:
        finish(app, cfg, _states)
    except:
        pass

@pibooth.hookimpl
def state_finish_do(app, cfg):
    # Write to the display at finish_do
    try:
        finish(app, cfg, _states)
    except:
        pass

@pibooth.hookimpl
def state_finish_exit(app, cfg):
    # Write to the display at finish_exit
    try:
        finish(app, cfg, _states)
    except:
        pass

####### FAILSAFE ###############################
@pibooth.hookimpl
def state_failsafe_enter(app):
    # Write to the display 1 at failsafe_enter
    try:
        failure(app, cfg, _states)
    except:
        pass

@pibooth.hookimpl
def state_failsafe_do(app):
    # Write to the display 1 at failsafe_do
    try:
        failure(app, cfg, _states)
    except:
        pass

####### CLEANUP ###############################
@pibooth.hookimpl
def pibooth_cleanup(app):
    # Turn off OLED display 1 at pibooth close
    try:
        if hasattr(app, 'gif_thread') and app.gif_thread.is_alive():
            app.gif_thread.stop()
    except OSError:
        pass
