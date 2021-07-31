====================
pibooth-oled-display
====================

|PythonVersions| |PypiPackage| |Downloads|

``pibooth-oled-display`` is a plugin for the `pibooth`_ application.

.. image:: https://github.com/DJ-Dingo/pibooth-oled-i2c-spi/blob/master/templates/main_oled.png
   :align: center
   :alt: OLED screens

Add a **COOL** small OLED monochrome or color screen through **I2c** or **SPI**. (parallel mode will not be suported)

The OLED device showing here is the 4 pin I2c **OLED sh1106  128x64** 1.3″

**SPI displays are supportet, but not testet yet** but many SPI displays allso have I2c, you can by making some hardware changes.


It can show numbers of **Photos Taken**, **Printed Photos**, **Forgotten Photos**, **Remaining Duplicates**, **Date-Time**.

It can show an image like your own **Logo**.

It also have 4 x **Free-Text** where you can write your own text or put in front of a **counter** and move around on the screen.

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
* 1 OLED-screens I2c or SPI (sh1106, ssd1306) are the most commom monochrome, with size **128x32 or 128x64**
* See the list of Testet OLED Devices under

.. image:: https://github.com/DJ-Dingo/pibooth-oled-display/blob/master/templates/128x64.png
   :align: center
   :alt: OLED screen

Testet OLED Devices
^^^^^^^^^^^^^^^^^^^

=============== ========================== =========== ===== =====
OLED devices     Display Pixels              TESTET     SPI   I2C
=============== ========================== =========== ===== =====
- sh1106        128x64 (I2c)               **Working**         X
- ssd1306       128x32, 128x64 (I2c)       **Working**         X
- ssd1309                                  not testet
- ssd1322                                  not testet
- ssd1325                                  not testet
- ssd1327                                  not testet
- ssd1331                                  not testet
- ssd1362                                  not testet
=============== ========================== =========== ===== =====


Install
-------
::

    $ sudo apt-get update
    $ setup not ready, add **pibooth_oled_display.py** to the config.cfg instead
    $ Also instal the OLED driver: **pip3 install luma.oled**
    $ You allso need to download the Oled_Display folder with all folders and files, then place the **oled_display** folder with subfolders in /home/pi/.config/pibooth/
    $ https://github.com/DJ-Dingo/pibooth-oled-display/tree/master/templates/oled_display


Most commom OLEDs I2c, SPI or I2c-SPI on the same device
--------------------------------------------------------

* OLED displays, don't use backlight, self-illumination.
* The display performance is better than the traditional LCD display, also lower consumption.
* SPI OLEDs are faster than I2c OLEDs, but use more wires to the raspberry pi.

You need to provide the name of the screen that you use. The most common OLED devices are these 3. 

Either the 4pins-I2c (as shown at the picture) or the 7pins-I2c-SPI devices.

* **ssd1306 128x32** 0.91″ OLED 128X32 white Display Module IIC I2C
* **ssd1306 128x64** 0.96″ I2C IIC SPI Serial 128X64 OLED
* **sh1106  128x64** 1.3″ SPI I2C Serial 128X64 OLED LCD Display Module


.. image:: https://github.com/DJ-Dingo/pibooth-oled-display/blob/master/templates/3-oled.png
   :align: center
   :alt: 3 OLED I2C screens


**I2c Configuration**
---------------------

Enabling The **I2c** Interface - Raspberry Pi
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The I2C peripheral is not turned on by default.

There are two methods to adjust the settings. To enable it, do the following.


**Raspberry Pi Configuration via Desktop GUI**  
 
* You can use the Desktop GUI by heading to the Pi **Start Menu > Preferences > Raspberry Pi Configuration**.
* A window will pop up with different tabs to adjust settings. What we are interested is the **Interfaces** tab.
* Click on the tab and select **Enable** for I2C. Click on the **OK** button to **save**.
* We recommend restarting your Pi to ensure that the changes to take effect.
* Click on the Pi Start Menu > Preferences > Shutdown. Since we just need to restart, click on the Restart button.

 
**raspi-config Tool via Terminal**

Again, we can use raspi-config to enable it.

* Run **sudo raspi-config**
* Use the down arrow to select **5 Interfacing Options**
* Arrow down to **P5 I2C**
* Select **yes** when it asks you to enable **I2C**
* Also select **yes** if it asks about automatically loading the kernel module.
* Use the right arrow to select the **<Finish>** button.
* Select **yes** when it asks to reboot.

The system will reboot. when it comes back up, log in and enter the following command

``>ls /dev/*i2c*``   
 
The Pi should respond with

``/dev/i2c-1``        
 
Which represents the user-mode I2C interface.


How to find your **I2c addresss**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You need to know the address of your I2c. You can find it on the command line using the **"sudo i2cdetect -y 1"** command.  
 
In this case the address of the display is **0x3C**.


.. image:: https://github.com/DJ-Dingo/pibooth-oled-display/blob/master/templates/i2cdetect-y1.png
   :align: center
   :alt: I2C Address

How to **change I2c address**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Only if needed: Most OLED devices have 2 options of a port address change.

Some can be changed by Soldering (short circuit) 1 wire on the back of the OLED device.

And some OLED, there is a resister you need to solder from one location to another.

(**check the manual of your device, or search the internet**)


**SPI Configuration**
---------------------

Enabling The **SPI** Interface - Raspberry Pi
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The **SPI** peripheral is not turned on by default.

There are two methods to adjust the settings. To enable it, do one of the following.

**Raspberry Pi Configuration via Desktop GUI**

* You can use the Desktop GUI by heading to the Pi **Start Menu > Preferences > Raspberry Pi Configuration**.
* A window will pop up with different tabs to adjust settings. What we are interested is the **Interfaces tab**.
* Click on the tab and select **Enable** for **SPI**. Click on the **OK** button to save.
* We recommend restarting your Pi to ensure that the changes to take effect.
* Click on the Pi **Start Menu > Preferences > Shutdown**. Since we just need to **restart**, click on the Restart button.

**raspi-config Tool via Terminal**

Again, we can use raspi-config to enable it.

* Run **sudo raspi-config**
* Use the down arrow to select **3 Interfacing Options**
* Arrow down to **P4 SPI**
* Select yes when it asks you to enable **SPI**
* Also select **yes** if it asks about automatically loading the kernel module.
* Use the right arrow to select the **<Finish>** button.
* Select **yes** when it asks to reboot.

The system will reboot. when it comes back up, log in and enter the following command.


**OLED Display Setup** in Pibooth Menu
--------------------------------------
At the first run, a configuration file is generated in ~/.config/pibooth/pibooth.cfg which permits to configure the behavior of the plugin.

.. image:: https://github.com/DJ-Dingo/pibooth-oled-display/blob/master/templates/menu_oled_display_setup.png
   :align: center
   :alt: OLED Display Setup



**OLED Display Text** in Pibooth Menu
-------------------------------------
At the first run, a configuration file is generated in ~/.config/pibooth/pibooth.cfg which permits to configure the behavior of the plugin.

.. image:: https://github.com/DJ-Dingo/pibooth-oled-display/blob/master/templates/menu_oled_display_text.png
   :align: center
   :alt: OLED Display Text


How to **setup** in config.cfg
------------------------------

Options are available by editing the configuration file. (Or use the option in pibooth menu under **Oled display setup** and **Oled display text**)

using the command line

::

   $ pibooth --config
   

**OLED_I2C_SPI** options in **config.cfg**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**[OLED DISPLAY SETUP]**

* # Choose OLED device-chip - **sh1106**, **ssd1306**, **ssd1309**, **ssd1322**, **ssd1325**, **ssd1327**, **ssd1331**, **ssd1362**

* oled_devices = **sh1106**

* # I2c or SPI display connection

* oled_i2c_or_spi = **I2c**

* # **SPI ONLY** - GPIO DC PIN

* oled_spi_gpio_dc_pin = **24**

* # **SPI ONLY** - GPIO RST PIN

* oled_spi_gpio_rst_pin = **25**

* # **I2c ONLY** - Change Port Address 0x3C(Default) 

* oled_port_address = **0x3C**

* # Change the I2c or SPI port number 0, 1 or 2 - (SPI = 0 - I2c = 1)

* oled_port = **1**

* # Change screen WIDTH 128(Default)

* oled_width = **128**

* # Change screen HEIGHT 32, 64(Default)

* oled_height = **64**

* # Color mode 1 (Default = 1 **monochrome**), RGB, RGBA

* oled_color_mode = **1**

* # Rotate screen up/down (Default = 0), 1,2,3

* oled_rotate = **0**

Show a **Logo** instead of text or counter
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can provide your own logo to the screen. Default is the Pibooth logo in 128x32 or 128x64. 
If you are using an OLED screen with other dimention you need to make a new photo and put it in the OLED logo folder.
You can allso convert pictures with Gimp or online services like `this_page <https://online-converting.com/image/>`_
If you have an 128x64, you convert a picture to that size in 8-bit mode, or make som tests. Or you can use some of the `XCF_files Here <https://github.com/DJ-Dingo/pibooth-oled-display/tree/master/templates/xcf_files>`_ and change them.


[OLED DISPLAY TEXT]

* # Choose a logo instead of text on the display (**WILL TEMPORARILY OVERWRITE TEXT ON SCREEN**)

* oled_showlogo = **Yes**

* # Pictures/Logo path

* oled_logo_path = **/home/pi/.config/pibooth/oled_display/logo/**

* # Choose what picture/logo file to show on the screen

* oled_logos = **pibooth_logo_64.png**


States pictures on OLED
^^^^^^^^^^^^^^^^^^^^^^^

* # Show state pictures (Yes / No), (Show a images for each state when taking photos)

* oled_states_pictures = **Yes**

* # State picture path

* oled_state_picture_path = /home/pi/.config/pibooth/oled_display/states/


.. image:: https://github.com/DJ-Dingo/pibooth-oled-display/blob/master/templates/state_photos.png
   :align: center
   :alt:  OLED State pictures


Write your own **Text** 1,2,3,4 and / or choose a **Counter type** to show on the display
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
 
* # Text-1 Counter, Date-Time - Could be either numbers of **Taken_Photo**, **Printed**, **Forgotten**, **Remaining_Duplicates**, **Date-Time**, **Empty** or **Text_Only**

* oled_counter_type1 = **Taken_Photo**

* # fonts path

* oled_fonts_path = **/home/pi/.config/pibooth/oled_display/fonts/**

* # Text-1 font 

* oled_font_1 = **DejaVuSans-Bold.ttf**

* # Text-1 color - use HTML color "name". On monochrome displays colors will be converted to **"white"**)

* oled_text1_color = **white**

* # Text-1

* oled_text_1 = **"Photos  "**

* # Text-1 size

* oled_size_1 = **19**

* # Text-1 - Move text-1 to the **right** on the screen

* oled_text1_right = **0**

* # Text-1 Move text-1 **down** on the screen

* oled_text1_down = **0**

------------------------------------

* # Text-2 Counter, Date-Time - Could be either numbers of **Taken_Photo**, **Printed**, **Forgotten**, **Remaining_Duplicates**, **Date-Time**, **Empty** or **Text_Only**

* oled_counter_type2 = **Printed**

* # Text-2 font

* oled_font_2 = **DejaVuSans-Bold.ttf**

* # Text-2 color - use HTML color "name". On monochrome displays colors will be converted to **"white"**)

* oled_text2_color = **white**

* # Text-2

* oled_text_2 = **"Printed "**

* # Text-2 size

* oled_size_2 = **19**

* # Text-2 Move text-2 to the **right** on the screen

* oled_text2_right = **0**

* # Text-2 Move text-2 **down** on the screen

* oled_text2_down = **23**

----------------------------------------------------

* # Text-3 Counter, Date-Time - Could be either numbers of **Taken_Photo**, **Printed**, **Forgotten**, **Remaining_Duplicates**, **Date-Time**, **Empty** or **Text_Only**

* oled_counter_type3 = **Remaining_Duplicates**

* # Text-3 font

* oled_font_3 = **DejaVuSans-Bold.ttf**

* # Text-3 color - use HTML color "name". On monochrome displays colors will be converted to **"white"**)

* oled_text3_color = **white**

* # Text-3

* oled_text_3 = **"Remain "**

* # Text-3 size

* oled_size_3 = **19**

* # Text-3 Move text-3 to the **right** on the screen

* oled_text3_right = **0**

* # Text-3 Move text-3 **down** on the screen

* oled_text3_down = **46**

----------------------------------------------------

* # Text-4 Counter, Date-Time - Could be either numbers of **Taken_Photo**, **Printed**, **Forgotten**, **Remaining_Duplicates**, **Date-Time**, **Empty** or **Text_Only**

* oled_counter_type4 = **Empty**

* # Text-4 font

* oled_font_4 = **DejaVuSans-Bold.ttf**

* # Text-4 color - use HTML color "name". On monochrome displays colors will be converted to **"white"**)

* oled_text4_color = **white**

* # Text-4

* oled_text_4 = **"Text 4"**

* # Text-4 size

* oled_size_4 = **19**

* # Text-4 Move text-4 to the **right** on the screen

* oled_text4_right = **0**

* # Text-4 Move text-4 **down** on the screen

* oled_text4_down = **0**


States description
------------------

.. image:: https://github.com/DJ-Dingo/pibooth-oled-display/blob/master/templates/state-sequence-oled-i2c.png
   :align: center
   :alt:  State sequence

Circuit diagram I2c devices
---------------------------

Here is the diagram for hardware connections with and Logic Level Converter.
**IMPORTANT** The Vcc and GND on the OLED screens are not always the same, so it is verry important that you check Vcc and GND is set correctly.

.. image:: https://github.com/DJ-Dingo/pibooth-oled-display/blob/master/templates/Pibooth%20OLED-I2c%20Sketch_bb.png
   :align: center
   :alt:  OLED Electronic sketch

Wiring I2c devices
------------------

I2C-safe Bi-directional **Logic Level Converter**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**ONLY If YOU USE 5v to the OLED SCREEN** some OLEDs can also run on 3v3, check your manual.

Since the Raspberry Pi GPIO only handle 3.3v, it will therefore be a good idea to use a **I2C-safe Bi-directional Logic Level Converter** so you don't fryed your pi.

.. image:: https://github.com/DJ-Dingo/pibooth-oled-display/blob/master/templates/level_converter.png
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



Circuit diagram SPI devices
---------------------------

Here is the diagram for hardware connections without and Logic Level Converter. 

If your OLED device demands a I2C-safe Bi-directional Logic Level Converter, you should get one.

**IMPORTANT** The Vcc and GND on the OLED screens are not always the same, so it is **verry important** that you check Vcc and GND is set correctly.

.. image:: https://github.com/DJ-Dingo/pibooth-oled-display/blob/master/templates/Pibooth%20oled-i2c-spi%20sketch_bb.png
   :align: center
   :alt:  OLED Electronic sketch


Wiring SPI devices
------------------

**SPI** OLED devices **wire** setup
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
If you have a 8 pins OLED device with **Vin** connect 5v to Vin and leave VCC empty. 
(or check the internet for more info on your device)

======== ============ ========== =============== ============================================================
7 Pins   Remarks      RPi-PIN    RPi GPIO        Info
======== ============ ========== =============== ============================================================
VCC      Power Pin    PIN 1 or 2 3V3 or 5V       3-5V tolerable - CHECK YOUR DEVICE
GND      Ground       PIN 6      GND             Ground pin of the module
D0, SCL  Clock        PIN 23     GPIO 11 (SCLK)  Acts as the clock pin. Used for both I2C and SPI
D1, SDA  MOSI         PIN 19     GPIO 10 (MOSI)  Data pin of the module. Used for both IIC and SPI
RST      Reset        PIN 22     GPIO 25         Resets the module, useful during SPI
DC, A0   Data/Command PIN 18     GPIO 24         Data Command pin. Used for SPI protocol
CS       Chip Select  PIN 24     GPIO 8 (CE0)    Useful when more than one module is used under SPI protocol
======== ============ ========== =============== ============================================================

.. --- Links ------------------------------------------------------------------

.. _`pibooth`: https://pypi.org/project/pibooth
.. _`pibooth_oled_display`: 

.. |PythonVersions| image:: https://img.shields.io/badge/python-3.6+-red.svg
   :target: https://www.python.org/downloads
   :alt: Python 3.6+

.. |PypiPackage| image:: 
   :target: 
   :alt: PyPi package

.. |Downloads| image:: 
   :target: 
   :alt: PyPi downloads

