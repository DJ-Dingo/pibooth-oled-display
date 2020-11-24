================
pibooth-oled-i2c
================

|PythonVersions| |PypiPackage| |Downloads|

``pibooth-oled-i2c`` is a plugin for the `pibooth`_ application.

.. image:: https://raw.githubusercontent.com/DJ-Dingo/pibooth-oled-i2c/
   :align: center
   :alt: OLED screen

THE README FILE IS STILL UNDER DEVELOPMENT!!!!!

**SPI displays not supportet in this version yet** but some SPI displays can allso use I2c.

Add an **COOL** small OLED-screen etc, 128x32 or 120x64 connected Through I2c.

It can show numbers of **Photos Taken**, **Printed Photos**, **Forgotten Photos**, **Remaining Duplicates**.

It can show an image like your own **Logo**.

It also have 2 x **Free-Text** where you can write your own text and move around on the screen.

Examples:

* Show pibooth counters like "Taken Photos 197" or "Today Photos 197"
* Show some free texts like "pibooth!" "Welcome!" "Take a Photo"

.. note:: Maximum text or counter size can be changed and text moved around to match the screen.

**All changes can be made in the pibooth.cfg, and most of them in the pibooth menu**

--------------------------------------------------------------------------------

.. contents::

Requirements
------------

Hardware
^^^^^^^^

* 1 Raspberry Pi 3 Model B (or higher)
* 1 I2c safe Bi-directional Logic Level Converter  **Only needed if you are using 5v**
* 1 OLED-screens with I2c (sh1106, ssd1306) are most commom with size **128x32 or 128x64**
* See the list of Testet OLED Devices under

.. image:: https://github.com/DJ-Dingo/pibooth-oled-i2c/blob/master/templates/128x64.png
   :align: center
   :alt: OLED screen

Testet OLED Devices
^^^^^^^^^^^^^^^^^^^

=============== ========================== ===========
OLED devices        Screen size testet       TESTET
=============== ========================== ===========
- sh1106        128x64                     **Working**
- ssd1306       128x32, 128x64             **Working**
- ssd1309                                  not testet
- ssd1322                                  not testet
- ssd1325                                  not testet
- ssd1327                                  not testet
- ssd1331                                  not testet
- ssd1362                                  not testet
=============== ========================== ===========


Install
-------
::

    $ setup not ready, add the plugin to the config.cfg instead


Configuration
-------------

Turn I2C on - Raspberry Pi
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The I2C peripheral is not turned on by default.

There are two methods to adjust the settings. To enable it, do the following.



**Raspberry Pi Configuration via Desktop GUI**  
 
You can use the Desktop GUI by heading to the Pi Start Menu > Preferences > Raspberry Pi Configuration.

A window will pop up with different tabs to adjust settings. What we are interested is the Interfaces tab. 

Click on the tab and select **Enable** for I2C. Click on the **OK** button to **save**.    

We recommend restarting your Pi to ensure that the changes to take effect.  

Click on the Pi Start Menu > Preferences > Shutdown. Since we just need to restart, click on the Restart button.



**raspi-config Tool via Terminal**

I2C is not turned on by default. Again, we can use raspi-config to enable it.

* Run **sudo raspi-config**
* Use the down arrow to select **5 Interfacing Options**
* Arrow down to **P5 I2C**
* Select **yes** when it asks you to enable **I2C**
* Also select **yes** if it asks about automatically loading the kernel module.
* Use the right arrow to select the **<Finish>** button.
* Select yes when it asks to reboot.

The system will reboot. when it comes back up, log in and enter the following command

``>ls /dev/*i2c*``   
 
The Pi should respond with

``/dev/i2c-1``        
 
Which represents the user-mode I2C interface.


Most commom OLED I2c screens
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You need to provide the name of the screen that you use.  
 
The most common OLED devices are these 3 **sh1106 128x64**, **ssd1306 128x64** and the small **ssd1306 128x32**.


.. image:: https://github.com/DJ-Dingo/pibooth-oled-i2c/blob/master/templates/oled_3.png
   :align: center
   :alt: 3 OLED I2C screens

How to find your I2c addresss
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You need to know the address of your I2c. You can find it on the command line using the **"sudo i2cdetect -y 1"** command.  
 
In this case the address of the display is **0x3C**.  


.. image:: https://github.com/DJ-Dingo/pibooth-oled-i2c/blob/master/templates/i2cdetect-y1.png
   :align: center
   :alt: I2C Address

How to change address on the I2c
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Only if needed: Most OLED devices have 2 options of a port address change.

Some can be changed by Soldering (short circuit) 1 wire on the back of the OLED device.

And some OLED, there is a resister you need to solder from one location to another.

(**check the manual of your device, or search the internet**)


Menu settings in Pibooth
^^^^^^^^^^^^^^^^^^^^^^^^
At the first run, a configuration file is generated in ~/.config/pibooth/pibooth.cfg which permits to configure the behavior of the plugin.

.. image:: https://github.com/DJ-Dingo/pibooth-oled-i2c/blob/master/templates/menu_settings.png
   :align: center
   :alt: OLED menu settings


How to setup the screen
-----------------------

Options are available by editing the configuration file. (Or use the option in pibooth menu under **Oled_i2c**)

using the command line

::

   $ pibooth --config
   

How to setup Oled_I2C in config.cfg 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

[OLED_I2C] 

# Choose OLED device-chip - **sh1106**, **ssd1306**, **ssd1309**, **ssd1322**, **ssd1325**, **ssd1327**, **ssd1331**, **ssd1362**

oled_devices = **sh1106**

# Change Port Address 0x3C(Default) 

oled_port_address = **0x3C**

# Change the I2C port number 0, 1 or 2 - (Default = 1) 

oled_port = **1**

# Change screen WIDTH 128(Default)

oled_width = **128**

# Change screen HEIGHT 32, 64(Default)

oled_height = **64**

# Color mode 1 (Default = 1), RGB, RGBA

oled_color_mode = **1**

# Rotate screen up/down (Default = 0), 2

oled_rotate = **0**

Show a logo instead of text or counter
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can provide your own logo to the screen. Default is the Pibooth logo in 128x32 or 128x64

If you are using OLED screens with other dimention you need to make a new photo and put in the OLED logo folder.
"/home/pi/.config/pibooth/logo"

# Choose a logo instead of text on the display (**WILL TEMPORARILY OVERWRITE TEXT ON SCREEN**) Default = No

oled_showlogo = **Yes**

# Pictures/Logo path

oled_logo_path = **/home/pi/.config/pibooth/logo/**

# Choose what picture/logo file to show on the screen

oled_logos = **pibooth_logo_64.png**

# Show state pictures (Yes / NO), (Show an images for each state when taking photos)

oled_states_pictures = **Yes**

------------------------------------

Write your own text 1-2 and / or choose a counter type to show on the display
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
 
# fonts path

oled_fonts_path = **/home/pi/.config/pibooth/oled_fonts/**

# Text-1 font 

oled_font_1 = **DejaVuSans-Bold.ttf**

# Text-1 counter type - Could be either numbers of **Taken_Photo**, **Printed**, **Forgotten**, **Remaining_Duplicates** or **Text_Only**

oled_counter_type1 = **Text_Only**

# Text-1

oled_text_1 = **" Pibooth"**

# Text-1 size

oled_size_1 = **"26"**

# Text-1 - Move text-1 to the **right** on the screen

oled_text1_right = **0**

# Text-1 Move text-1 **down** on the screen

oled_text1_down = **"0"**

------------------------------------

# Text-2 font

oled_font_2 = **DejaVuSans-Bold.ttf***

# Text-2 counter type - Could be either numbers of **Taken_Photo**, **Printed**, **Forgotten**, **Remaining_Duplicates** or **Text_Only**

oled_counter_type2 = **Text_Only**

# Text-2

oled_text_2 = **"Photos"**

# Text-2 size

oled_size_2 = **28**

# Text-2 Move text-2 to the **right** on the screen

oled_text2_right = **16**

# Text-2 Move text-2 **down** on the screen

oled_text2_down = **"28"**


States description
------------------

.. image:: https://github.com/DJ-Dingo/pibooth-oled-i2c/blob/master/templates/state-sequence-oled-i2c.png
   :align: center
   :alt:  State sequence


Circuit diagram
---------------

Here is the diagram for hardware connections with and Logic Level Converter.
**IMPORTANT** The Vcc and GND on the OLED screens are not always the same, so it is verry important that you check Vcc and GND is set correctly.

.. image:: https://github.com/DJ-Dingo/pibooth-oled-i2c/blob/master/templates/Pibooth%20OLED-I2c%20Sketch_bb.png
   :align: center
   :alt:  OLED Electronic sketch

Wiring
------

I2C-safe Bi-directional Logic Level Converter 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**ONLY If YOU USE 5v to the OLED SCREEN** some OLEDs can also run on 3v3, check your manual.

Since the Raspberry Pi GPIO only handle 3.3v, it will therefore be a good idea to use a **I2C-safe Bi-directional Logic Level Converter** so you don't fryed your pi.

.. image:: https://raw.githubusercontent.com/DJ-Dingo/pibooth-lcd-i2c/master/templates/level_converter.png
   :align: center
   :alt: 4-channel I2C-safe Bi-directional Logic Level converter


How to connect a **Level Converter** to your **OLED** and the **Raspberry Pi**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Connect the OLED-I2c to **HV** (High Level) on the Level Converter.  

**IMPORTANT CHECK YOUR OLED FOR THE RIGHT CONNECTION**

- GND: Pin GND (GND) **MAKE SURE GND IS SET TO GROUND**
- VCC: Pin HV  (HV ) (5v) - Also connect **5v** from the Raspberry Pi Pin 2, to **HV** on the Level Converter
- SCL: Pin HV2 (HV2) **CHECK YOU USE THE SAME NUMBER LV as HV on the SCL**
- SDA: Pin HV1 (HV1) **CHECK YOU USE THE SAME NUMBER LV as HV on the SDA**

Connect the Raspberry Pi (**BOARD numbering scheme**) to **LV** (Low Level) on the Level Converter. 

- GND:  Pin 6 (GND) GROUND on the pi
- 3.3v: Pin 1 (LV ) 3v3 on the pi
- SCL:  Pin 5 (LV2) **CHECK YOU USE THE SAME NUMBER LV as HV on the SCL**
- SDA:  Pin 3 (LV1) **CHECK YOU USE THE SAME NUMBER LV as HV on the SDA**

.. --- Links ------------------------------------------------------------------

.. _`pibooth`: https://pypi.org/project/pibooth
.. _`pibooth_oled_i2c`: https://pypi.org/project/pibooth-lcd-i2c/

.. |PythonVersions| image:: https://img.shields.io/badge/python-3.6+-red.svg
   :target: https://www.python.org/downloads
   :alt: Python 3.6+

.. |PypiPackage| image:: 
   :target: 
   :alt: PyPi package

.. |Downloads| image:: 
   :target: 
   :alt: PyPi downloads

