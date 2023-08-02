====================
pibooth-oled-display
====================

|PythonVersions|

``pibooth-oled-display`` is a plugin for the `pibooth`_ application.

.. image:: https://raw.githubusercontent.com/DJ-Dingo/pibooth-oled-display/master/templates/Pibooth_OLED-I2c_3V_Sketch5_bb.png
   :align: center
   :alt: I2c 3v3 OLED display simple setup x 2

| Add a small OLED display (**Monochrome or Color**) through **I2c** or **SPI**. 

(parallel mode will not be suported). 

| **Features**
| It can show up to 3 lines of **Text**, with or without **Counters**, with numbers of 
| ``Photos Taken``, ``Printed Photos``, ``Forgotten Photos``, ``Remaining Duplicates``, 

Or ``Date-Time``, ``Text_Only`` or an ``Empty`` line.

.. image:: https://raw.githubusercontent.com/DJ-Dingo/pibooth-oled-display/master/templates/main_oled.png
   :align: center
   :alt: OLED display examples

| And Image or Animated Gif with your own **Logo**, like **Pibooth Logo**, 

and a option for images for each `States`_

.. Note:: Text / Counters can be ``Sized``, ``Centered``, or moved ``Right`` or ``Down``, to match the display. Changes can be made in the `Pibooth Menu`_ or in the `config.cfg`_ file.

**Don't be scared by this long manual, it´s there to cover all the different OLED displays on the marked. If you only have an 3v3 I2c 
OLED display all you need is 4 wires to your Pi, and installing the plugin.**

-----------------------------------------------------------

.. contents::

---------------------

Requirements
------------

Hardware
^^^^^^^^

* 1 x Raspberry Pi 3 Model B (or higher).
* 1 x I2c safe Logic Level Converter (**If you are using 5v displays**).  
* 1 x OLED-display, with **I2c** or **SPI** (See the list of `Testet OLED Displays`_).

.. image:: https://raw.githubusercontent.com/DJ-Dingo/pibooth-oled-display/master/templates/128x64.png
   :align: center
   :alt: OLED display

Testet OLED Displays
^^^^^^^^^^^^^^^^^^^^
* supported displays

=============== ========================== =========== ===== =====
OLED displays    Display Resolutions         TESTET     SPI   I2C
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

Most common OLED displays are these 3 (I prefer size 0.96, 1.3 or higher″)

* **ssd1306 128x32** 0.91″ 128X32 white Display
* **ssd1306 128x64** 0.96″ 128X64 white Display
* **sh1106  128x64** 1.3″  128X64 white Display

--------------------------------------

Install
-------
::

   New version comming soon, dont install before this install info is updated


--------------------------------------

I2c Configuration
-----------------

Enabling I2c interface on the Raspberry Pi
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| **The I2C peripheral is not turned on by default.**

There are two methods to enable I2c.
 

| (**Be aware that newer Raspberry PI OS systems can have a different way to turn on I2c**).

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

| **You need to know the address of your I2c.**

You can find it writing this command in the command line:

``sudo i2cdetect -y 1``
 
In this case the address of the display is **0x3C**.


.. image:: https://raw.githubusercontent.com/DJ-Dingo/pibooth-oled-display/master/templates/i2cdetect-y1.png
   :align: center
   :alt: Detect I2C Address

How to change I2c address
^^^^^^^^^^^^^^^^^^^^^^^^^

| **Only if needed**:

* On most displays you can solder a (short circuit) on the back of the OLED display, to change the address.

(**check the manual of your display, or search the internet**)

--------------------------------------

SPI Configuration
-----------------

Enabling SPI interface on the Raspberry Pi
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| **The SPI peripheral is not turned on by default.**

There are two methods to adjust the settings.

| (**Be aware that newer Raspberry PI OS systems can have a different way to turn on SPI**).

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

--------------------------------------

I2c Circuit diagram and wiring - (ONLY with 3v3 displays)
---------------------------------------------------------

I2c Circuit diagram - (ONLY with 3v3 displays) 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| Here is the diagram for hardware connections **without** an Logic Level Converter.

**IMPORTANT** **use ONLY 3v3** 

The Vcc and GND on the OLED displays are not always the same, so it is verry important that you check Vcc and GND is set correctly.

.. image:: https://raw.githubusercontent.com/DJ-Dingo/pibooth-oled-display/master/templates/Pibooth%20OLED-I2c%203V_Sketch2_bb.png
   :align: center
   :alt:  OLED I2c Circuit diagram - (ONLY with 3v3 displays)


I2c Wire - (ONLY with 3v3 displays)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

3v3 only. **IMPORTANT CHECK YOUR DISPLAY FOR THE RIGHT CONNECTION**


============ ======== ========================
Display Pins RPi-PINs Info                      
============ ======== ========================
VCC 3v3      PIN 1    3v3 ONLY
GND (Ground) PIN 6    Ground pin of the module
SCL (Clock)  PIN 5    Acts as the clock pin.
SDA (Data)   PIN 3    Data pin of the module.
============ ======== ========================

----------------------------------------------------

I2c Circuit diagram - (5v displays) with an Logic Level Converter
-----------------------------------------------------------------

I2C circuit diagram - (5v displays)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Here is the diagram for hardware connections **with** and Logic Level Converter.
**IMPORTANT** The Vcc and GND on the OLED display are not always the same, so it is verry important that you check Vcc and GND is set correctly.

.. image:: https://raw.githubusercontent.com/DJ-Dingo/pibooth-oled-display/master/templates/Pibooth_OLED-I2c_Sketch_bb_1.png
   :align: center
   :alt:  I2C circuit diagram - (5v displays)

I2c wire - (5v displays)
^^^^^^^^^^^^^^^^^^^^^^^^

**IMPORTENT**: If you use 5v to power the OLED display 
*most OLEDs can also run on 3v3, check your manual.*

Since the Raspberry Pi GPIO only handle 3.3v, it will therefore be a good idea to use a **Logic Level Converter** when using 5v to power the display, so you don't fryed your pi.

.. image:: https://raw.githubusercontent.com/DJ-Dingo/pibooth-oled-display/master/templates/level_converter.png
   :align: center
   :alt: I2c wire - (5v displays) 4-channel Logic Level converter


**IMPORTANT CHECK YOUR DISPLAY FOR THE RIGHT CONNECTION**

| OLED-I2c to the **HV** (High Level) side, on the Level Converter HV.  

*(Display >> level converter HV side)*

============ =============== =========================================
Display Pins Level converter Info                      
============ =============== =========================================
GND          GND             **Dsplay GND to the level converter GND**
VCC          HV  (HV )       **Display VC to the level converter HV**
SCL (Clock)  HV2 (HV2)       **SCL <> HV2  on the Level Converter**
SDA (Data)   HV1 (HV1)       **SDA <> HV1 on the Level Converter**
============ =============== =========================================

| RPi (**BOARD numbering scheme**) to **LV** (Low Level) side, on the Level Converter. 

*(Raspberry Pi >> Level converter LV side)*

===== ===== =============== ==========================================
 RPi  Pins  Level converter Info                      
===== ===== =============== ==========================================
GND   Pin 6 GND             **RPi GND to GND on the level converter**
3.3v  Pin 1 LV  (LV )       **RPi (3v3) to LV on the Level Converter**
5v    Pin 2 HV  (HV )       **RPi (5v) to HV on the Level Converter**
SCL   Pin 5 LV2 (LV2)       **SCL <> LV2 on the Level Converter**
SDA   Pin 3 LV1 (LV1)       **SDA <> LV1 on the Level Converter**
===== ===== =============== ==========================================

----------------------------------------------------


SPI Circuit diagram and Wiring 
------------------------------

SPI circuit diagram (ONLY with 3v3 displays)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Here is the diagram for hardware connections **without** and **Logic Level Converter**. 

If your OLED display use 5v instead of 3v3, it demands an 8 Channel Logic Level Converter, you should get one or you risk frye your pi.

**IMPORTANT** The Vcc and GND on an OLED display are not always the same, so it is **verry important** that you check Vcc and GND is set correctly.

.. image:: https://raw.githubusercontent.com/DJ-Dingo/pibooth-oled-display/master/templates/Pibooth_OLED-SPI_1.png
   :align: center
   :alt:  SPI circuit diagram (ONLY with 3v3 displays)



SPI wire setup - (ONLY with 3v3 displays)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

======== ============ ========== ============== ============================================================
7 Pins   Remarks      RPi-PIN    RPi GPIO       Info
======== ============ ========== ============== ============================================================
VCC      Power Pin    PIN 1      3V3            3V3 ONLY - CHECK YOUR DISPLAY
GND      Ground       PIN 6      GND            Ground pin of the module
D0, SCL  Clock        PIN 23     GPIO 11 (SCLK) Acts as the clock pin.
D1, SDA  MOSI         PIN 19     GPIO 10 (MOSI) Data pin of the module.
RST      Reset        PIN 22     GPIO 25        Resets the module, useful during SPI
DC, A0   Data/Command PIN 18     GPIO 24        Data Command pin. Used for SPI protocol
CS       Chip Select  PIN 24     GPIO 8 (CE0)   Useful when more than one module is used under SPI protocol
                      PIN 26     GPIO 7 (CE1)   Useful when more than one module is used under SPI protocol
======== ============ ========== ============== ============================================================

**If you have a 8 pins OLED display with "Vin" connect 3v3 to Vin and leave VCC empty.** *(or check the internet for more info on how to setup your display)*

----------------------------------------------------


SPI wire - (5v display) with a Logic Level Converter 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You will need a 8 channel Logic Level Converter to use SPI with 5v. Or you can use 2 x 4 channels Logic Level Converters.

| Same princip as `I2c Circuit diagram - (5v displays) with an Logic Level Converter`_ 

* You take the needed GPIO PINs from the Raspberry Pi, and wire them to the LV side of the Logic Level Converters.
* The same goes for 3v3 wire, that goes to the LV side of the level converters. 
* You also need to wire the 5v from the Raspberry Pi to the HV side of the level converter. 
* And last you need GND (Ground) from the Raspberry Pi to GND one or both sides of the level converters.

----------------------------------------------------

States
------

States images
^^^^^^^^^^^^^
.. image:: https://raw.githubusercontent.com/DJ-Dingo/pibooth-oled-display/master/templates/state_photos.png
   :align: center
   :alt:  OLED State pictures

| If you need to change states images or add missing resolutions to fit your display

Look at `How to show your own Logo and States images`_.

| These states are showing on the display, if **Show state pictures** is activated

| ``´choose´`` ``´chosen´`` ``´preview´`` ``´capture´``

``´processing´`` ``´print´`` ``´finish´`` ``´failsafe´``


States description
^^^^^^^^^^^^^^^^^^
.. image:: https://raw.githubusercontent.com/DJ-Dingo/pibooth-oled-display/master/templates/state-sequence-oled-i2c.png
   :align: center
   :alt:  State sequence

----------------------------------------------------

Setup in Pibooth Menu
---------------------

OLED Display - (SETUP) - Pibooth Menu
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| You enter the menu by using Esc on your keyboard. 

Be aware that this plugin can sometimes make the reaction to enter the menu slow (2-3 sec).

| At the first time you make changes in the Menu, a configuration file is generated in ``'~/.config/pibooth/pibooth.cfg'``

which permits to configure the behavior of the plugin.

.. image:: https://raw.githubusercontent.com/DJ-Dingo/pibooth-oled-display/master/templates/menu_oled_display_setup_1.png
   :align: center
   :alt: OLED Display - (Setup) - Pibooth Menu



OLED Display - (MODIFY) - Pibooth Menu
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| You enter the menu by using Esc on you keyboard. 

Be aware that this plugin can sometimes make the reaction to enter the menu slow (2-3 sec).

| At the first time you make changes in the Menu, a configuration file is generated in ``'~/.config/pibooth/pibooth.cfg'``

which permits to configure the behavior of the plugin.

.. image:: https://raw.githubusercontent.com/DJ-Dingo/pibooth-oled-display/master/templates/menu_oled_display_modify.png
   :align: center
   :alt: OLED Display - (Modify) - Pibooth Menu


--------------------------------------

Setup in config.cfg
-------------------

| Options are also available by editing the configuration file.
| But it is easier to `Setup in Pibooth Menu`_ 

under **Oled display - (setup)** and **Oled display - (modify)**

Edit config.cfg by using the command line or a text editor

::

   $ pibooth --config
   

OLED DISPLAY - (SETUP) - config.cfg
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``config.cfg``

| [OLED DISPLAY - (SETUP)]
| # Choose OLED device - ``'ssd1306 (Default)', 'ssd1309', 'ssd1322', 'ssd1325', 'ssd1327', 'ssd1331', 'ssd1362', 'sh1106'``
| # Required by 'oled_display' plugin

oled_devices = ``ssd1306``

| # Display connection ``'I2c' or 'SPI'``
| # Required by 'oled_display' plugin

oled_i2c_or_spi = ``I2c``

| # I2c address ``(Default=0x3c)``
| # Required by 'oled_display' plugin

oled_port_address = ``0x3c``

| # Change SPI device number ``'0', '1' or '2' (Default = 0)``
| # Required by 'oled_display' plugin

oled_spi_device_number = ``0``

| # Change the I2c or SPI port number - ``(I2c = '1' - SPI = '0', '1', '2')``
| # Required by 'oled_display' plugin

oled_port = ``1``

| # SPI only GPIO DC PIN ``(Default=24)``
| # Required by 'oled_display' plugin

oled_spi_gpio_dc_pin = ``24``

| # SPI only GPIO RST PIN ``(Default=25)``
| # Required by 'oled_display' plugin

oled_spi_gpio_rst_pin = ``25``

| # Change screen WIDTH - ``'32', '48', '64', '80', '96', '128(Default)', '160', '240', '256', '320'``
| # Required by 'oled_display' plugin

oled_width = ``128``

| # Change screen HEIGHT - ``'32', '48', '64(Default)', '80', '96', '128', '160', '240', '256', '320'``
| # Required by 'oled_display' plugin

oled_height = ``64``

| # Color mode - ``'1 = Monochrome (Default)', 'RGB', 'RGBA'``
| # Required by 'oled_display' plugin

oled_color_mode = ``1``

| # Rotate screen - ``'0 (Default)', '1', '2', '3'``
| # Required by 'oled_display' plugin

oled_rotate = ``0``


------------------------------------------


OLED DISPLAY - (MODIFY) - config.cfg
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| [OLED DISPLAY - (MODIFY)]
| # Show state pictures - ``'Yes' or 'No'``
| # Required by 'oled_display' plugin - (See `States`_ for more info on how it works)

oled_states_pictures = ``Yes``

| # Show Logo or Animated Gif (instead of text) - ``'Yes' or 'No'``
| # Required by 'oled_display' plugin - (Also see `How to add Animated Gif`_ )

oled_showlogo = ``No``

| # Logo or Animated Gif in the folder ``'~/.config/pibooth/oled_display/logo/'``
| # Required by 'oled_display' plugin

oled_logos = ``128x64_Pibooth_2.gif``

| # FPS (Frames Per Second) speed for Animated Gif
| # Required by 'oled_display' plugin

oled_animated_fps = ``15``

------------------------------------

| # Text-1 - Counters, Text, Date-Time - Could be either ``'Taken_Photo', 'Printed', 'Forgotten', 'Remaining_Duplicates', 'Date-Time', 'Empty', 'Text_Only'``
| # Required by 'oled_display' plugin - (Also see `How to change the Date-Time format`_, when using **Date-Time**)

oled_counter_type1 = ``Taken_Photo``

| # Text-1 Font - You can add more fonts 'Truetype(.ttf)' or 'Opentype(.otf)', in the folder ``'~/.config/pibooth/oled_display/fonts/'``
| # Required by 'oled_display' plugin

oled_font_1 = ``DejaVuSerif-Bold.ttf``

| # Text-1 Color - uses HTML color names. E.g. ``'White', 'Red', 'Cyan', 'Silver', 'Blue', 'Grey', 'DarkBlue', 'Black', 'LightBlue', 'Orange', 'Purple', 'Brown', 'Yellow', 'Maroon', 'Lime', 'Green', 'Magenta', 'Olive'.`` 
| *(On Monochrome displays colors will be converted to 'White')*
| # Required by 'oled_display' plugin

oled_text1_color = ``white``

| # Text-1 - Text with space after to use with counter, or leave empty for counter only
| # Required by 'oled_display' plugin

oled_text_1 = ``"Photos  "``

| # Text-1 - Center text on display ``'Yes' or 'No'``
| # Required by 'oled_display' plugin

oled_text_1_center = ``No``

| # Text-1 Size - 19 is default if 3 x text/counters are used on the display at the same time
| # Required by 'oled_display' plugin

oled_size_1 = ``19``

| # Text-1 - Move text 'Right' on display
| # Required by 'oled_display' plugin

oled_text1_right = ``0``

| # Text-1 - Move text 'Down' on display
| # Required by 'oled_display' plugin

oled_text1_down = ``0``

------------------------------------

| # Text-2 - Counters, Text, Date-Time - Could be either ``'Taken_Photo', 'Printed', 'Forgotten', 'Remaining_Duplicates', 'Date-Time', 'Empty', 'Text_Only'``
| # Required by 'oled_display' plugin - (Also see `How to change the Date-Time format`_, when using **Date-Time**)

oled_counter_type2 = ``Printed``

| # Text-2 Font - You can add more fonts 'Truetype(.ttf)' or 'Opentype(.otf)', in the folder ``'~/.config/pibooth/oled_display/fonts/'``
| # Required by 'oled_display' plugin

oled_font_2 = ``DejaVuSerif-Bold.ttf``

| # Text-2 Color - uses HTML color names. E.g. ``'White', 'Red', 'Cyan', 'Silver', 'Blue', 'Grey', 'DarkBlue', 'Black', 'LightBlue', 'Orange', 'Purple', 'Brown', 'Yellow', 'Maroon', 'Lime', 'Green', 'Magenta', 'Olive'.`` 
| *(On Monochrome displays colors will be converted to 'White')*
| # Required by 'oled_display' plugin

oled_text2_color = ``white``

| # Text-2 - Text with space after to use with counter, or leave empty for counter only
| # Required by 'oled_display' plugin

oled_text_2 = ``"Printed "``

| # Text-2 - Center text on display ``'Yes' or 'No'``
| # Required by 'oled_display' plugin

oled_text_2_center = ``No``

| # Text-2 Size - 19 is default if 3 x text/counters are used on the display at the same time
| # Required by 'oled_display' plugin

oled_size_2 = ``19``

| # Text-2 - Move text 'Right' on display
| # Required by 'oled_display' plugin

oled_text2_right = ``0``

| # Text-2 - Move text 'Down' on display
| # Required by 'oled_display' plugin

oled_text2_down = ``23``


----------------------------------------------------

| # Text-3, Counter, Date-Time - Could be either ``'Taken_Photo', 'Printed', 'Forgotten', 'Remaining_Duplicates', 'Date-Time', 'Empty', 'Text_Only'``
| # Required by 'oled_display' plugin - (Also see `How to change the Date-Time format`_, when using **Date-Time**)

oled_counter_type3 = ``Remaining_Duplicates``

| # Text-3 Font - You can add more fonts 'Truetype(.ttf)' or 'Opentype(.otf)', in the folder ``'~/.config/pibooth/oled_display/fonts/'``
| # Required by 'oled_display' plugin

oled_font_3 = ``DejaVuSerif-Bold.ttf``

| # Text-3 Color - uses HTML color names. E.g. ``'White', 'Red', 'Cyan', 'Silver', 'Blue', 'Grey', 'DarkBlue', 'Black', 'LightBlue', 'Orange', 'Purple', 'Brown', 'Yellow', 'Maroon', 'Lime', 'Green', 'Magenta', 'Olive'.``
| *(On Monochrome displays colors will be converted to 'White')*
| # Required by 'oled_display' plugin

oled_text3_color = ``white``

| # Text-3 - Text with space after to use with counter, or leave empty for counter only
| # Required by 'oled_display' plugin

oled_text_3 = ``"Remain "``

| # Text-3 - Center text on display ``'Yes' or 'No'``
| # Required by 'oled_display' plugin

oled_text_3_center = ``No``

| # Text-3 Size - 19 is default if 3 x text/counters are used on the display at the same time
| # Required by 'oled_display' plugin

oled_size_3 = ``19``

| # Text-3 - Move text 'Right' on display
| # Required by 'oled_display' plugin

oled_text3_right = ``0``

| # Text-3 - Move text 'Down' on display
| # Required by 'oled_display' plugin

oled_text3_down = ``46``


----------------------------------------------------

How to use date-time / logo / Animated Gif
------------------------------------------

How to change the Date-Time format
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| See all the Date-Time format codes in the following file 

`Date-Time_Format_Codes.rst`_ 

You can also find the file **Date-Time_Format_Codes.rst** in your local pibooth config folder ``~/.config/pibooth/oled_display/``

* Choose Date_Time in the menu - (If you leave the text field empty, the Default will be used = **%H:%M:%S**).
* Or use semething like this **%d/%m - %H:%M:%S** in the text field to display the date and time.

Remember to set the size of the text to match the display, after you set your Date-Time format codes.

----------------------------------------------------

How to show your own Logo and States images
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| **LOGO** - choose **Yes** in the Pibooth Menu under **Logo instead of text** 
| *(Default Logo is the Pibooth logo in resolutions 128x32 or 128x64).* 

Also look at `How to add Animated Gif`_ as logo.

| Add a new Logo or Animated gif, same resolution as your display ( or lower).

* Logo path = ``~/.config/pibooth/oled_display/logo/``

| (pibooth-oled-display support many different image type extensions)

If you add an images with the same name and File extension(s) as some of the default images, only the user images will be showing.


| **STATES** - choose **Yes** in the Pibooth Menu under **Show state pictures** 
| *(Default States images are already provided with these display resolutions):*
| ``128 x 32 pixels`` ``128 x 64 pixels`` ``128 x 128 pixels``
| ``160 x 128 pixels`` ``192 x 64 pixels`` ``256 x 64 pixels``

``256 x 128 pixels`` ``256 x 256 pixels`` ``320 x 240 pixels``

| Add new ``.png`` States images, same resolution as your display, to each folders.

* States path = ``~/.config/pibooth/oled_display/states/``

**When adding a new states images, it will automatic be used instead of default.**

There are 8 folders, and you need 11 ``.png`` images with the static names "folder and resolution".
Here is an examble on how you should name your states images if you have an display with resolution 128 x 64. 
You should make images with the same resolution as you display and use the static names with resolution as below, and put them in every folder under each states. 

Examples : 128x32 = ``processing_128x32.png`` 128x64 = ``processing_128x64.png``

| List of file names for a display with 128x64 resolution
| `states/capture/ <https://github.com/DJ-Dingo/pibooth-oled-display/tree/master/pibooth_oled_display/oled_display/states/capture>`_  ``capture_128x64.png``
| `states/choose/ <https://github.com/DJ-Dingo/pibooth-oled-display/tree/master/pibooth_oled_display/oled_display/states/choose>`_ ``choose_128x128.png``
| `states/failure/ <https://github.com/DJ-Dingo/pibooth-oled-display/tree/master/pibooth_oled_display/oled_display/states/failure>`_ ``failure_128x64.png``
| `states/finished/ <https://github.com/DJ-Dingo/pibooth-oled-display/tree/master/pibooth_oled_display/oled_display/states/finished>`_ ``finished_128x64.png``
| **layout needs 4 ``.png`` images named like this**
| `states/layout/ <https://github.com/DJ-Dingo/pibooth-oled-display/tree/master/pibooth_oled_display/oled_display/states/layout>`_ ``layout1_128x64.png``, ``layout2_128x64.png``, ``layout3_128x64.png``, ``layout4_128x64.png``
| `states/preview/ <https://github.com/DJ-Dingo/pibooth-oled-display/tree/master/pibooth_oled_display/oled_display/states/preview>`_ ``preview_128x64.png``
| `states/printer/ <https://github.com/DJ-Dingo/pibooth-oled-display/tree/master/pibooth_oled_display/oled_display/states/printer>`_ ``printer_128x64.png``
`states/processing/ <https://github.com/DJ-Dingo/pibooth-oled-display/tree/master/pibooth_oled_display/oled_display/states/processing>`_ ``processing_128x64.png``

| You can see the origial gimp files in the **origin** folder `Here <https://github.com/DJ-Dingo/pibooth-oled-display/tree/master/pibooth_oled_display/oled_display/states>`_ under each folder.
| `states/capture/origin/ <https://github.com/DJ-Dingo/pibooth-oled-display/tree/master/pibooth_oled_display/oled_display/states/capture/origin>`_ ``capture_128x64.xcf``
| `states/choose/origin/ <https://github.com/DJ-Dingo/pibooth-oled-display/tree/master/pibooth_oled_display/oled_display/states/choose/origin>`_ ``choose_128x64.xcf``
| `states/failure/origin/ <https://github.com/DJ-Dingo/pibooth-oled-display/tree/master/pibooth_oled_display/oled_display/states/failure/origin>`_ ``failure_128x64.xcf``
| `states/finished/origin/ <https://github.com/DJ-Dingo/pibooth-oled-display/tree/master/pibooth_oled_display/oled_display/states/finished/origin>`_ ``finished_128x64.xcf``
| **Layout has 4 ``.xcf`` files, inside each folder for your resolution** 
| `states/layout/origin/ <https://github.com/DJ-Dingo/pibooth-oled-display/tree/master/pibooth_oled_display/oled_display/states/layout/origin>`_ ``layout1_128x64.xcf`` ``layout2_128x64.xcf`` ``layout3_128x64.xcf`` ``layout4_128x64.xcf``
| `states/preview/origin/ <https://github.com/DJ-Dingo/pibooth-oled-display/tree/master/pibooth_oled_display/oled_display/states/preview/origin>`_ ``preview_128x64.xcf``
| `states/printer/origin/ <https://github.com/DJ-Dingo/pibooth-oled-display/tree/master/pibooth_oled_display/oled_display/states/printer/origin>`_ ``printer_128x64.xcf``
`states/processing/origin/ <https://github.com/DJ-Dingo/pibooth-oled-display/tree/master/pibooth_oled_display/oled_display/states/processing/origin>`_ ``processing_128x64.xcf``

| If you are using an OLED display with other resolution than already supplied,
you need to make a new images and put it in each states folder or display will be empty if states is activated.

| You can convert images with the free `GIMP`_ or online services like (`this page`_).

If you have an monochrome display with the resolution 128x64, you can convert or make an image to that resolution (in 8-bit mode). 

----------------------------------------------------

How to add Animated Gif
^^^^^^^^^^^^^^^^^^^^^^^

| You can add Animated Gif in the folder ``~/.config/pibooth/oled_display/logo/``

An choose **Yes** in **Logo instead of text** in the Pibooth Menu

On Monochrome displays (black & white) you need the Animated Gif to have a Black bagground. The reason for that is that the luma.oled drivers converts transperent to white color, when using ``color mode 1``.

| Some Animated Gifs with transperent bagground work, but in general they don´t.
| So do some test with Animated Gif´s in the same resolution or less as your display. 

All images will be centered automatic on the display. 

| ?. Can i use an Animated Gif with colors on an Monochrome display = **Yes**

But they are not always showing correct, as they will be converted to Black and White or grayscale.

----------------------------------------------------


Tips & Tricks
-------------

How to use 2 x OLED displays at the same time
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

How to install the second display plugin "pibooth_oled_display_2.py"
====================================================================

* The extra plugin for display 2 **"pibooth_oled_display_2.py"** is already in the folder ``~/.config/pibooth/oled_display/``
* You can activate the plugin by adding path to the file, to custom plugins in the config.cfg file under [GENERAL].

Open the config.cfg with this command, and find the line "plugins ="
::

   $ pibooth --config

| # Path to custom plugin(s) not installed with pip (list of quoted paths accepted)

``plugins = '~/.config/pibooth/oled_display/pibooth_oled_display_2.py'``

| Now you will have an extra plugin option in pibooth settings, with 

**Oled display 2 - (Setup)** and **Oled display 2 - (modify)**

* Go to the menu and setup your new second display. If you are using I2c, you new display 2 need its own I2c addresses (**standard 0x3d**). 
* If you use SPI, you need to have 2 displays with the CS (**Chip Select**) option (this funktion has not yet been tested, but should work).


.. image:: https://raw.githubusercontent.com/DJ-Dingo/pibooth-oled-display/master/templates/add_extra_oled_display_2.png
   :align: center
   :alt:  Add an extra OLED display settings


Setup 2 x I2c OLED displays - (Showing seperate things on each display)
=======================================================================

* You will need 2 x I2c OLED displays with different I2c addresses. defaults are ``0x3c`` on display 1, and ``0x3d`` on display 2. 
* On most displays you can change the I2c address on the back of your OLED display with some soldering.
   
* Or you can get an **8 Channel I2C Muti-Channel Expansion Development Board** to convert the default address to an new address and then use up 8 x I2c displays at the same time.

Setup 2 x SPI OLED displays - (Showing seperate things on each display)
=======================================================================

| **I dont know if it work, as i have not testet it yet. But it should work.** 

*And if it work, it will only work if you have the CS PIN on the displays*.

* Both the displays uses the same PINs/GPIOs, except the CS (Chip Select) PIN
* On display 1. Put a wire from the CS PIN to GPIO 8 (pin24) to choose CE0.
* On display 2. Put a wire from the CS PIN to GPIO 7 (pin26) to choose CS1. 

**Check online for more info about your displays on how to set them up.**

* According to LUMA.oled driver documentation, you should choose **port 0** for display 1 and **port 1** for display 2.
* You can do that in the pibooth menu. An maybe also try change the SPI device number to 0,1 or 2 to make it work.

Can i use SPI1 ? (e.g.SPI and SPI1 together on the pi)
======================================================

| **The short answer is no. I tryed, but with no luck**

*I dont think it is suported by the luma.oled drivers.*

* So only SPI (SPI0) can be used.

Setup 2 x OLED displays - (Showing the same things on each display)
===================================================================

| If you want to show the exact same things on 2 or more displays, you dont need the second plugin.

* On the I2c displays, you just use the same port address (0x3c etc.), and wire them to the same GPIO PINs.
* On the SPI displays, you just use the same CS port address (CE0 etc.), and wire them to the same GPIO PINs.

----------------------------------------------------

How to use a OLED displays with only 6 pins I2c/SPI
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| **SPI** Most 6 PINs displays works out of the box with SPI. 

* but unfortunately you can only use one display in pibooth, as there is no CS pin on the display.

| **I2c** Can be used with some soldering tricks on the back of the displays, and some extra component.

* It also works when using 2 displays in pibooth.

.. image:: https://raw.githubusercontent.com/DJ-Dingo/pibooth-oled-display/master/templates/6PIN_SPI_I2C.png
   :align: center
   :alt:  Change 6PIN SPI to I2c

| To choose I2c port address, you need to solder a wire from

* DC >> VCC = for I2C address 0x3c
* DC >> GND = for I2C address 0x3d

| You will also need to make a "pull-up and reset circuit" or "reset pull-up circuit."

So you need a 10k resistor, and a 47nf or 100nf capacitor (Ceramic or Electrolytic)

* Reset pin >> 10k resistor >> VCC
* Reset pin >> 47nF or 100nF capacitor (condensator) >> GND (Ground)

.. image:: https://raw.githubusercontent.com/DJ-Dingo/pibooth-oled-display/master/templates/Reset_pull-up_circuit.jpg
   :align: center
   :alt:  Reset pull-up circuit

The purpose of this circuit is to provide a stable voltage level and proper reset functionality for the Reset pin of the OLED display. The 10k resistor connected between the Reset pin and VCC is the pull-up resistor, which ensures that the Reset pin remains at a high logic level when it is not actively driven low.

The 47nF or 100nF capacitor connected between the Reset pin and ground serves to stabilize the reset signal by filtering out any noise or voltage fluctuations. It helps ensure that the reset signal is clean and reliable, preventing false triggering or erratic behavior.

By using this pull-up and reset circuit, you are ensuring that the OLED display receives a proper reset signal and is able to turn on reliably. It is a common practice to include these components to ensure the correct functioning of cheap displays with reset pins.



.. --- Links ------------------------------------------------------------------

.. _`pibooth`: https://pypi.org/project/pibooth
.. _`pibooth_oled_display`: 
.. _`official Raspberry Pi documentation`: https://www.raspberrypi.com/documentation/
.. _`Date-Time_Format_Codes.rst`: https://github.com/DJ-Dingo/pibooth-oled-display/blob/master/pibooth_oled_display/oled_display/Date-Time_Format_Codes.rst
.. _`this page`: https://online-converting.com/image/
.. _`Download Here`: https://github.com/DJ-Dingo/pibooth-oled-display/tree/master/templates/xcf_files
.. _`GIMP`: https://www.gimp.org/
.. _`Pibooth Menu`: #oled-display-modify-pibooth-menu
.. _`config.cfg`: #oled-display-modify-config-cfg

.. |PythonVersions| image:: https://img.shields.io/badge/python-3.6+-red.svg
   :target: https://www.python.org/downloads
   :alt: Python 3.6+

