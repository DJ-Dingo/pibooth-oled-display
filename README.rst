====================
pibooth-oled-display
====================

|PythonVersions| |PypiPackage| |Downloads|

``pibooth-oled-display`` is a plugin for the `pibooth`_ application.

.. image:: https://github.com/DJ-Dingo/pibooth-oled-i2c-spi/blob/master/templates/main_oled.png
   :align: center
   :alt: OLED screens

| Add an small **COOL** OLED (monochrome or color) display through **I2c** or **SPI**. 
(parallel mode will not be suported). 

It can show up to 3 x **Text**, plus the **Counters** with numbers of **Photos Taken**, **Printed Photos**, **Forgotten Photos**, **Remaining Duplicates**, and it can also show **Date-Time** or **Text_Only**.

Or show an image with your Own **Logo**, like **Pibooth Logo**, and/or the images for each `states`_

.Examples: (look at the picture above)

* Show pibooth counters like **"Photos 418"**, **"Wedding Party Photos 481"**.
* Show some free texts like **"pibooth!"**, **"Welcome!"**, **"Take a Photo"**.
* **Text_Only** in one line an a **Counter** of any choice in the next line.

.. Note:: | Text / Counter size can be changed, Centered, or moved to the Right to match the display.

**All changes needed can be made in the Pibooth menu, or in pibooth.cfg**

--------------------------------------------------------------------------------

.. contents::

Requirements
------------

Hardware
^^^^^^^^

* 1 x Raspberry Pi 3 Model B (or higher)
* 1 x I2c safe Logic Level Converter, (**Only needed if you are using a 5v display**).  
* 1 x OLED-display, with **I2c** or **SPI** (SH1106 or SSD1306 etc.) witch are the Most common choice.

.. image:: https://github.com/DJ-Dingo/pibooth-oled-display/blob/master/templates/128x64.png
   :align: center
   :alt: OLED screen

Testet OLED Devices
^^^^^^^^^^^^^^^^^^^

=============== ========================== =========== ===== =====
OLED devices     Display Pixels              TESTET     SPI   I2C
=============== ========================== =========== ===== =====
- sh1106        128x64                     **Working**     X     X
- ssd1306       128x32, 128x64             **Working**     X     X
- ssd1309                                  not testet
- ssd1322                                  not testet
- ssd1325                                  not testet
- ssd1327                                  not testet
- ssd1331                                  not testet
- ssd1362                                  not testet
=============== ========================== =========== ===== =====

| **SPI** are a little faster than **I2c**, but also uses more wires to the raspberry pi.
| Personally I use **I2c** 3v3 displays, since it is only 4 wires to the Pi. 

Most common OLED displays are these 3 (I prefer size 1.3″)

* **ssd1306 128x32** 0.91″ 128X32 white Display
* **ssd1306 128x64** 0.96″ 128X64 white Display
* **sh1106  128x64** 1.3″  128X64 white Display



Install
-------
::

    $ sudo apt-get update
    $ Add the file **pibooth_oled_display.py** to the config.cfg
    $ Instal the OLED driver: **pip3 install luma.oled**
    $ You allso need to download the Oled_Display folder with all folders and files, then place the **oled_display** folder with subfolders in /home/pi/.config/pibooth/
    $ https://github.com/DJ-Dingo/pibooth-oled-display/tree/master/templates/oled_display


I2c Configuration
-----------------

Enabling The I2c Interface - Raspberry Pi
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| **The I2C peripheral is not turned on by default.**
There are two methods to enable I2c.
 

| (**Be aware that newer Raspberry PI OS systems can have a defferent way to turn on I2c**).
I recommend checking the `official Raspberry Pi documentation`_ or the latest resources provided by the Raspberry Pi community. They will provide the most accurate instructions for configuring the I2C interface on your specific version of the Raspberry Pi.



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

The system will reboot. when it comes back up, log in and enter the following command in terminal

``ls /dev/*i2c*``   
 
The Pi should respond with

``/dev/i2c-1``        
 
Which represents the user-mode I2C interface.


How to find your I2c addresss
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You need to know the address of your I2c. You can find it on the command line using the **"sudo i2cdetect -y 1"** command. If you dont know how to wire your display, go down to `Circuit diagram and wiring i2c display`_
 
In this case the address of the display is **0x3C**.


.. image:: https://github.com/DJ-Dingo/pibooth-oled-display/blob/master/templates/i2cdetect-y1.png
   :align: center
   :alt: I2C Address

How to change I2c address
^^^^^^^^^^^^^^^^^^^^^^^^^

| Only if needed: Most OLED devices have 2 options of a port address change.
| Some can be changed by Soldering (short circuit) 1 wire on the back of the OLED device.
And on some OLED displays, there is a resister you need to solder from one location to another.

(**check the manual of your device, or search the internet**)


SPI Configuration
-----------------

Enabling The SPI Interface - Raspberry Pi
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| **The SPI peripheral is not turned on by default.**
There are two methods to adjust the settings.

| (**Be aware that newer Raspberry PI OS systems can have a defferent way to turn on SPI**).
I recommend checking the `official Raspberry Pi documentation`_ or the latest resources provided by the Raspberry Pi community. They will provide the most accurate instructions for configuring the SPI interface on your specific version of the Raspberry Pi.


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

The system will reboot. when it comes back up, log in and enter the following command in terminal.

``ls /dev/spidev*``

| This command lists the SPI devices available in the /dev directory.
| If SPI is enabled, you should see output similar to 
``/dev/spidev0.0`` 
``/dev/spidev0.1``
If SPI is not enabled, you will see an error message or no output.


OLED Display - (setup) in Pibooth Menu
--------------------------------------
| At the first run, a configuration file is generated in ~/.config/pibooth/pibooth.cfg
which permits to configure the behavior of the plugin.

.. image:: https://github.com/DJ-Dingo/pibooth-oled-display/blob/master/templates/menu_oled_display_setup_1.png
   :align: center
   :alt: OLED Display Setup



OLED Display - (modify) in Pibooth Menu
---------------------------------------
| At the first run, a configuration file is generated in ~/.config/pibooth/pibooth.cfg
which permits to configure the behavior of the plugin.

.. image:: https://github.com/DJ-Dingo/pibooth-oled-display/blob/master/templates/menu_oled_display_text_1.png
   :align: center
   :alt: OLED Display Text


How to setup in config.cfg
--------------------------

| Options are also available by editing the configuration file.
(But it is easier to use the options in the "pibooth menu" under **Oled display - (setup)** and **Oled display - (modify)**)

Edit config.cfg by using the command line

::

   $ pibooth --config
   

OLED DISPLAY - (SETUP) options in config.cfg
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**[OLED DISPLAY - (SETUP)]**

* # Choose OLED device - **(ssd1306=Default)**, **ssd1309**, **ssd1322**, **ssd1325**, **ssd1327**, **ssd1331*, **ssd1362**, **sh1106**

* oled_devices = **ssd1306**

* # I2c or SPI display connection

* oled_i2c_or_spi = **I2c**

* # **I2c ONLY** - Change Port Address 0x3C(Default) 

* oled_port_address = **0x3C**

* # Change SPI device number 0, 1, 2 - (Default = 0)

* oled_spi_device_number = **0**

* # Change the I2c or SPI port number 0, 1 or 2 - (SPI = 0,1,2 - I2c = 1)

* oled_port = **1**

* # **SPI only** GPIO DC PIN (24) - Can be changed to any free GPIO PIN

* oled_spi_gpio_dc_pin = **24**

* # SPI only GPIO RST PIN (25) - Can be changed to any free GPIO PIN

* oled_spi_gpio_rst_pin = **25**

* # Change screen WIDTH, 32, 48, 64, 80, 96, 128(Default), 160, 256]

* oled_width = **128**

* # Change screen HEIGHT 32, 48, 64(Default), 80, 96, 128, 160, 256

* oled_height = **64**

* # Color mode - (Default **monochrome** = 1) RGB, RGBA

* oled_color_mode = **1**

* # Rotate screen - (Normal mode = 0 or 2)

* oled_rotate = **0**

------------------------------------------


OLED DISPLAY - (modify) options in config.cfg
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**[OLED DISPLAY - (modify)]**

* # Choose a logo instead of text on the display (**WILL TEMPORARILY OVERWRITE TEXT ON SCREEN**).
* # (Also see `How to make your own logo and show instead of text or counters`_)

* oled_showlogo = **Yes**

* # Pictures/Logo path

* oled_logo_path = **/home/pi/.config/pibooth/oled_display/logo/**

* # Choose what picture/logo file to show on the screen

* oled_logos = **pibooth_logo_64.png**

.. _States: README.rst#States-pictures-on-OLED
States pictures on OLED
^^^^^^^^^^^^^^^^^^^^^^^

* # Show state pictures (Yes / No), (Show a images for each state when taking photos)

* oled_states_pictures = **Yes**

* # State picture path

* oled_state_picture_path = /home/pi/.config/pibooth/oled_display/states/


.. image:: https://github.com/DJ-Dingo/pibooth-oled-display/blob/master/templates/state_photos.png
   :align: center
   :alt:  OLED State pictures


* # Text-1 Counter, Date-Time - Could be either numbers of **Taken_Photo**, **Printed**, **Forgotten**, **Remaining_Duplicates**, **Date-Time**, **Empty** or **Text_Only**
* # (Also see `How to change the Date-Time format`_, when using **Date-Time**)
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


How to make your own Logo and show instead of text or counters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| You can provide your own logo to the Display. (Default is the Pibooth logo in 128x32 or 128x64). 
| If you are using an OLED display with other dimension you need to make a new image and put it in the OLED logo folder.
| You can find logo folder at this path **~/.config/pibooth/oled_display/logo/**

| You can allso convert pictures with Gimp or online services like `this_page <https://online-converting.com/image/>`_
| If you have an 128x64 display, you can convert a image to that size and in 8-bit mode, (or make you owm image). 
| Or you can use some of the XCF_files (`Download Here <https://github.com/DJ-Dingo/pibooth-oled-display/tree/master/templates/xcf_files>`_), that i used to make the pibooth logo´s and state images, and change them using the free `GIMP <https://www.gimp.org/>`_


How to change the Date-Time format
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| See all the Date-Time format codes in the following `page <https://github.com/DJ-Dingo/pibooth-oled-display/blob/master/Date-Time_Format_Codes.rst>`_ 
or see the file **Date-Time_Format_Codes.rst** in your local pibooth config folder **~/.config/pibooth/**

| # Choose Date_Time in the menu - (If you leave the text field empty, the Default will be used = **%H:%M:%S**).
| Or use semething like this **%d/%m - %H:%M:%S** in the text field to display the date and time.
| Remember to set the size of the text to match the display, after you set your Date-Time format codes.


States description
------------------

.. image:: https://github.com/DJ-Dingo/pibooth-oled-display/blob/master/templates/state-sequence-oled-i2c.png
   :align: center
   :alt:  State sequence


----------------------------------------------------

.. _Circuit diagram and wiring i2c display: README.rst#Circuit-diagram-and-wiring---I2c-display
Circuit diagram and wiring - I2c display
----------------------------------------


I2C displays without an Logic Level Converter (ONLY with 3v3 display) 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Here is the diagram for hardware connections **without** an Logic Level Converter.
**IMPORTANT** **use ONLY 3v3** The Vcc and GND on the OLED displays are not always the same, so it is verry important that you check Vcc and GND is set correctly.

.. image:: https://github.com/DJ-Dingo/pibooth-oled-display/blob/master/templates/Pibooth%20OLED-I2c%203V_Sketch2_bb.png
   :align: center
   :alt:  OLED Electronic sketch


Wire I2C OLED display without an Logic Level Converter (ONLY with 3v3 display)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
3v3 only. **IMPORTANT CHECK YOUR DISPLAY FOR THE RIGHT CONNECTION**

======== ============ ========== =============== ==================================================
  Pins   Remarks      RPi-PIN    RPi GPIO        Info
======== ============ ========== =============== ==================================================
VCC 3v3  Power Pin    PIN 1 etc. 3V3 ONLY        Power
GND      Ground       PIN 6 etc. GND             Ground pin of the module
SCL      Clock        PIN 5                      Acts as the clock pin.
SDA      MOSI         PIN 3                      Data pin of the module.
======== ============ ========== =============== ==================================================


----------------------------------------------------



I2C displays with a Logic Level Converter (for use with 5v display)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Here is the diagram for hardware connections **with** and Logic Level Converter.
**IMPORTANT** The Vcc and GND on the OLED display are not always the same, so it is verry important that you check Vcc and GND is set correctly.

.. image:: https://github.com/DJ-Dingo/pibooth-oled-display/blob/master/templates/Pibooth_OLED-I2c_Sketch_bb_1.png
   :align: center
   :alt:  OLED Electronic sketch

Wire I2C display with a Logic Level Converter (for use with 5v display)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**ONLY If YOU USE 5v to power the OLED display** some OLEDs can also run on 3v3, check your manual.

Since the Raspberry Pi GPIO only handle 3.3v, it will therefore be a good idea to use a **I2C Logic Level Converter** when using 5v to power the display, so you don't fryed your pi.

.. image:: https://github.com/DJ-Dingo/pibooth-oled-display/blob/master/templates/level_converter.png
   :align: center
   :alt: 4-channel I2C-safe Bi-directional Logic Level converter


How to connect a Level Converter to your OLED and the Raspberry Pi
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Connect the OLED-I2c to **HV** (High Level) on the Level Converter.  

**IMPORTANT CHECK YOUR DISPLAY FOR THE RIGHT CONNECTION**

- GND: Pin GND (GND) **MAKE SURE GND IS SET TO GROUND**
- VCC: Pin HV  (HV ) (5v) - Also connect **5v** from the Raspberry Pi Pin 2, to **HV** on the Level Converter
- SCL: Pin HV2 (HV2) **CHECK YOU USE THE SAME NUMBER LV as HV on the SCL**
- SDA: Pin HV1 (HV1) **CHECK YOU USE THE SAME NUMBER LV as HV on the SDA**

Connect the Raspberry Pi (**BOARD numbering scheme**) to **LV** (Low Level) on the Level Converter. 

- GND:  Pin 6 (GND) GROUND on the pi
- 3.3v: Pin 1 (LV ) 3v3 on the pi
- SCL:  Pin 5 (LV2) **CHECK YOU USE THE SAME NUMBER LV as HV on the SCL**
- SDA:  Pin 3 (LV1) **CHECK YOU USE THE SAME NUMBER LV as HV on the SDA**


----------------------------------------------------


Wiring and Circuit diagram for SPI display
------------------------------------------

Circuit diagram SPI display without an Logic Level Converter ONLY with 3v3 display)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Here is the diagram for hardware connections **without** and **Logic Level Converter**. 

If your OLED display use 5v instead of 3v3, it demands an 8 Channel Logic Level Converter, you should get one or you risk frye your pi.

**IMPORTANT** The Vcc and GND on an OLED display are not always the same, so it is **verry important** that you check Vcc and GND is set correctly.

.. image:: https://github.com/DJ-Dingo/pibooth-oled-display/blob/master/templates/Pibooth_OLED-SPI_1.png
   :align: center
   :alt:  OLED Electronic sketch



SPI OLED display wire setup without and Logic Level Converter
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
If you have a 8 pins OLED display with **Vin** connect 3v3 to Vin and leave VCC empty. 
(or check the internet for more info on how to setup your display)

======== ============ ========== =============== ============================================================
7 Pins   Remarks      RPi-PIN    RPi GPIO        Info
======== ============ ========== =============== ============================================================
VCC      Power Pin    PIN 1 or 2 3V3             3V3 tolerable - CHECK YOUR DISPLAY
GND      Ground       PIN 6      GND             Ground pin of the module
D0, SCL  Clock        PIN 23     GPIO 11 (SCLK)  Acts as the clock pin.
D1, SDA  MOSI         PIN 19     GPIO 10 (MOSI)  Data pin of the module.
RST      Reset        PIN 22     GPIO 25         Resets the module, useful during SPI
DC, A0   Data/Command PIN 18     GPIO 24         Data Command pin. Used for SPI protocol
CS       Chip Select  PIN 24     GPIO 8 (CE0)    Useful when more than one module is used under SPI protocol
                      PIN 26     GPIO 7 (CE1)    Useful when more than one module is used under SPI protocol
======== ============ ========== =============== ============================================================

----------------------------------------------------


SPI displays with a Logic Level Converter (for use with 5v display)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You will need a 8 channel Logic Level Converter to use SPI with 5v. Or you can use 2 x 4 channels Logic Level Converters.

| It is the same princip as `I2c displays with a logic level converter (for use with 5v display)`_ 
| You take the needed GPIO PINs from the Raspberry Pi, and wire them to the LV side of the Logic Level Converters.
| The same goes for 3v3 wire, that goes to the LV side of the level converters. 
| You also need to wire the 5v from the Raspberry Pi to the HV side of the level converter. 
And last you need GND (Ground) from the Raspberry Pi to GND one or both sides of the level converters.

----------------------------------------------------

Tips & Tricks
-------------

How to use 2 x OLED displays at the same time
---------------------------------------------

Setup 2 x I2c OLED displays - Showing seperate things on each display
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-- You will need 2 x I2c OLED devices with different I2c addresses. defaults are 0x3C on display 1, and 0x3D on display 2.
   On most displays you can change the I2c address on the back of you OLED device with some soldering.
   
-- Or you can get an **8 Channel I2C Muti-Channel Expansion Development Board** to convert the default address to an new address and then use up 8 x I2c devices at the same time.

Setup 2 x SPI OLED displays - Showing seperate things on each display
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| -- I dont know if it work, as i have not testet it yet. But it should work. 
*And if it work, it will only work if you have the CS PIN on the displays*.

| -- Both the displays uses the same PINs/GPIOs, except the CS (Chip Select) PIN
| -- On display 1. Put a wire from the CS PIN to GPIO 8 (pin24) to choose CE0.
| -- On display 2. Put a wire from the CS PIN to GPIO 7 (pin26) to choose CS1. 
*Check online for more info about your devices on how to set them up*.

| -- According to LUMA driver documentation, you should choose **port 0** for display 1 and **port 1** for display 2.
You can do that in the pibooth menu. An maybe also change the SPI device number to 0,1 or 2 to make it work.

Can i use SPI1, or SPI and SPI1 togheter on the pi
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
| -- The short answer is no, i tryed but with no luck. I dont think it is suported by the luma.oled drivers
So only SPI / SPI0 can be used.


How to install the Display 2 plugin "pibooth_oled_display_2.py"
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| -- The extra plugin for display 2 **"pibooth_oled_display_2.py"** is allredy in the folder **~/.config/pibooth/**
| -- You can activate the plugin by adding the path to the file, to custom plugins in the config.cfg under [GENERAL].
::

   # Path to custom plugin(s) not installed with pip (list of quoted paths accepted)
   plugins = '~/.config/pibooth/pibooth_oled_display_2.py'

| Now you will have an extra plugin option in pibooth settings, with **Oled display 2 - (Setup)** and **Oled display 2 - (modify)** 
| Go to the menu and setup your new display 2. If you are using I2c, you new display 2 need its own I2c addresses (**standard 0x3d**). 
If you use SPI, you need to have 2 displays with the CS (**Chip Select**) option (this funktion has not yet been tested, but should work).


.. image:: https://github.com/DJ-Dingo/pibooth-oled-display/blob/master/templates/add_extra_oled_display_2.png
   :align: center
   :alt:  Add an extra OLED settings


Setup 2 x OLED displays - Showing the same things on each display
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| If you want to show the exact same things on 2 or more displays, you dont need the second plugin.
| On the I2c displays, you just use the same port address (0x3c etc.), and wire them to the same GPIO PINs.
| On the SPI displays, you just use the same CS port address (CE0 etc.), and wire them to the same GPIO PINs.

----------------------------------------------------


How to use the OLED displays with only 6 pins I2c/SPI
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| **SPI** Most 6 PINs displays works out of the box, but unfortunately you can only use one display, 
as there is no CS pin on the display.

| **I2c** can be used with some soldering tricks on the back of the displays, and with extra component. 
| And it also works with 2 displays.

 



.. --- Links ------------------------------------------------------------------

.. _`pibooth`: https://pypi.org/project/pibooth
.. _`pibooth_oled_display`: 
.. _`official Raspberry Pi documentation`: https://www.raspberrypi.com/documentation/


.. |PythonVersions| image:: https://img.shields.io/badge/python-3.6+-red.svg
   :target: https://www.python.org/downloads
   :alt: Python 3.6+

.. |PypiPackage| image:: 
   :target: 
   :alt: PyPi package

.. |Downloads| image:: 
   :target: 
   :alt: PyPi downloads
