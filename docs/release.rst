Release for Pypi
----------------

1. Install packaging libraries:

   ::

        $ sudo pip install setuptools wheel twine

2. Update the version number in the ``pibooth-oled-display/pibooth_oled_display.py`` file.

3. Check the rendering of the README by generating the HTML page:

"Note: Before generating the HTML page for README, ensure that the package is installed on your system. The pibooth_oled_display.py script requires access to certain files that are copied to the system during the installation process. 
use ``python3 setup.py install``" to install first.

   ::

        $ python setup.py --long-description | rst2html.py > output.html

4. Clean previous packages (avoid upload of older package):

   ::

        $ rm -rf build/ dist/

5. Generate the package:

   ::

        $ python setup.py bdist_wheel

6. Check the package integrity:

   ::

        $ twine check dist/*

7. Upload the package on Pypi (replace XXXXXX by username and password of your
   Pypi account):

   ::

        $ twine upload -u XXXXXX -p XXXXXX dist/*
