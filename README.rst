THE README FILE IS STILL UNDER DEVELOPMENT

====================
pibooth-oled-i2c
====================

|PythonVersions| |PypiPackage| |Downloads|

``pibooth-oled-i2c`` is a plugin for the `pibooth`_ application.

.. image:: https://raw.githubusercontent.com/DJ-Dingo/pibooth-oled-i2c/
   :align: center
   :alt: OLED screen


Add a small **COOL** OLED-screen etc, 128x32 or 120x64 connected Through I2c.

It can show numbers of **Photos Taken**, **Printed Photos**, **Forgotten Photos**, **Remaining Duplicates**.

It can show an image like your own logo.

It also have 2 x **Free-Text** where you can write your own text and move around on the screen.

Examples:

* Show pibooth counters like "Taken Photos 197" or "Today Photos 197"
* Show some free texts like "pibooth!" "Welcome!" "Take a Photo"

.. note:: Maximum text or counter size can be changed and moved around to match the screen.

Supported OLED devices are **sh1106**, **(ssd1306 default)**, **ssd1309**, **ssd1322**, **ssd1325**, **ssd1327**, **ssd1331**, **ssd1351**, **ssd1362**

* I2c port address (**Default 0x3C**)

**All changes can be made in the pibooth.cfg, and most of the allso in the pibooth menu**

--------------------------------------------------------------------------------

.. contents::

Requirements
------------

Hardware
^^^^^^^^

* 1 Raspberry Pi 3 Model B (or higher)
* 1 I2c safe Bi-directional Logic Level Converter
* 1 OLED-screens with I2c (sh1106, ssd1306) are most commom with size **128x32 or 128x64**
* See the list of Testet Devices under 
.. image:: https://github.com/DJ-Dingo/pibooth-oled-i2c/blob/master/templates/128x64.png
   :align: center
   :alt: OLED screen

Testet Devices
^^^^^^^^^^^^^^

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
- ssd1351                                  not testet
- ssd1362                                  not testet
=============== ========================== ===========


Install
-------
::

    $ setup not ready, add the plugin to the config.cfg instead


Configuration
-------------

Menu settings
^^^^^^^^^^^^^
At the first run, a configuration file is generated in ~/.config/pibooth/pibooth.cfg which permits to configure the behavior of the application.

.. image:: https://github.com/DJ-Dingo/pibooth-oled-i2c/blob/master/templates/menu-settings.png
   :align: center
   :alt: OLED menu settings

Turn I2C on - Raspberry Pi
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The I2C peripheral is not turned on by default.

There are two methods to adjust the settings. To enable it, do the following.

**Raspberry Pi Configuration via Desktop GUI**  
 
You can use the Desktop GUI by heading to the Pi Start Menu > Preferences > Raspberry Pi Configuration.

A window will pop up with different tabs to adjust settings. What we are interested is the Interfaces tab. 

Click on the tab and select Enable for I2C. Click on the OK button to save.    

We recommend restarting your Pi to ensure that the changes to take effect.  

Click on the Pi Start Menu > Preferences > Shutdown. Since we just need to restart, click on the Restart button.

**raspi-config Tool via Terminal**

I2C is not turned on by default. Again, we can use raspi-config to enable it.

* Run sudo raspi-config.
* Use the down arrow to select 5 Interfacing Options
* Arrow down to P5 I2C.
* Select yes when it asks you to enable I2C
* Also select yes if it asks about automatically loading the kernel module.
* Use the right arrow to select the <Finish> button.
* Select yes when it asks to reboot.

The system will reboot. when it comes back up, log in and enter the following command

``>ls /dev/*i2c*``   
 
The Pi should respond with

``/dev/i2c-1``        
 
Which represents the user-mode I2C interface.


Most commom OLED I2c screens are sh1106 or ssd1306
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You need to provide the name of the screen that you use.  
 
but most common are the sh1106 or ssd1306
  
The OLED devices on this photo are the **sh1106 128x64**, **ssd1306 128x64** and the small **ssd1306 128x32**. 

How to find your I2c addresss
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You need to know the address of your I2c. You can find it on the command line using the **"sudo i2cdetect -y 1"** command.  
 
In this case the address of the display is **0x3C**.  


.. image:: https://github.com/DJ-Dingo/pibooth-oled-i2c/blob/master/templates/i2cdetect-y1.png
   :align: center
   :alt: I2C Address

How to change address on the I2c
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Only if needed most OLED devices have 2 options of a port address change.

Some can be changed by Soldering (short circuit) 1 wire on the back of the OLED device.

And some OLED, there is a resister you need to solder from one location to another.

(**check the manual of your device, or search the internet**)


Circuit diagram
---------------

Here is the diagram for hardware connections.

.. image:: https://github.com/DJ-Dingo/pibooth-oled-i2c/blob/master/templates/Pibooth%20OLED-I2c%20Sketch_bb.png
   :align: center
   :alt:  OLED Electronic sketch




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

