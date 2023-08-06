#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from io import open
import os.path as osp
from setuptools import setup
from setuptools.command.install import install

HERE = osp.abspath(osp.dirname(__file__))
sys.path.insert(0, HERE)
from pibooth_oled_display import pibooth_oled_display as plugin

def main():
    setup(
        name="pibooth_oled_display",
        version=plugin.__version__,
        description=plugin.__doc__,
        long_description=open(osp.join(HERE, 'README.rst'), encoding='utf-8').read(),
        long_description_content_type='text/x-rst',
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Environment :: Plugins',
            'Intended Audience :: Developers',
            'Intended Audience :: End Users/Desktop',
            'License :: OSI Approved :: GNU Affero General Public License v3',
            'Natural Language :: English',
            'Operating System :: POSIX :: Linux',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Topic :: Multimedia :: Graphics :: Capture :: Digital Camera',
        ],
        author="Kenneth Nicholas Jørgensen",
        url="https://github.com/DJ-Dingo/pibooth-oled-display",
        download_url="https://github.com/DJ-Dingo/pibooth-oled-display/archive/{}.tar.gz".format(plugin.__version__),
        license='GPLv3',
        platforms=['unix', 'linux'],
        keywords=[
            'raspberry pi',
            'camera',
            'raspberry pi camera',
            'photobooth',
            'selfiecam',
            'pygame',
            'pil',
            'pillow',
            'pibooth',
            'pibooth plugin',
            'oled display',
            'luma.oled',
            'oled'
        ],
        python_requires=">=3.6",
        install_requires=[
            'pibooth>=2.0.3',
            'luma.oled>=3.12.0',
            'setuptools'
        ],
        include_package_data=True,
        packages=['pibooth_oled_display', 'pibooth_oled_display.oled_display'],
        package_data={
            'pibooth_oled_display.oled_display': ['logo/*', 'fonts/*', 'default/*', '*.py', '*.rst',
                                                  'states/capture/*', 
                                                  'states/choose/*', 
                                                  'states/failure/*', 
                                                  'states/finished/*', 
                                                  'states/layout/*', 
                                                  'states/preview/*', 
                                                  'states/printer/*', 
                                                  'states/processing/*']
        },
        options={
            'bdist_wheel': {'universal': True}
        },
        zip_safe=False,
        entry_points={'pibooth': ["pibooth_oled_display = pibooth_oled_display.pibooth_oled_display"]},
    )

if __name__ == '__main__':
    main()
