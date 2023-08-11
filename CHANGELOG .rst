Changelog
=========

Version 2.0.3 (??/??/2023)
--------------------------
- Improvement: Version comparison between package and local files in /.config/pibooth/oled_display/ folder. Then do an 'AutoUpdate' of files like Date-Time_Format_Codes.rst and pibooth_oled_display_2.py installed in the local config folder if they are older than packages version.
- Removed: 'clear()' in pibooth_cleanup, as it sometimes gave an wierd error in terminal when        closing Pibooth. It´s not a bug, but anooring
- Added: DESCRIPTION for use with Pypi.

Version 2.0.2 (05/08/2023)
--------------------------
- Stable release: Tested for every imaginable situation, and user challenges.
- Improvement: New way of using user files. If missing user fonts or logo files (named in confin.cfg), default logo or font will be used. Loggin to terminal to inform user about missing files.
- Removed: gimp files under install, can be downloaded on github
- Moved: Default font, logo, states files from user folders to packages folder
- Bug Fix: Making instal more smooth

Version 2.0.1 (30/07/2023)
--------------------------
- Feature: Displaying Animated gif, Center text option, Center Images/States automatic.
- Improvement: Making Font/Logo/Animated Gif database, to prevent re-loading dir everytime you enter menu. User fonts as standard. Made states 'static images' for most display resolutions to fit display setup, E,g. 128x64, 64x128 etc. So filename with display height x width tell what state picture to use.
- Removed: Rpi OS fonts as standard, Unused cfg-adds
- Bug Fix: Making userfonts to work properly

Version 2.0.0 (17/07/2023)
----------------------------
- Feature: Added support for 2 x displays an Center text on display.
- Improvement: Make the plugin more stable when running 2 displays.
- Remove: text option 4, to prevent too long a config.cfg file
- Bug Fix: Jumping text and counters on display

Version 1.0.0 (02/08/2021)
----------------------------
- Feature Logo, Time, States: Added new funktions to the display menu.

Version 0.0.1 (31/07/2021)
----------------------------
- First release: Showing only counter pictures taken.

...
