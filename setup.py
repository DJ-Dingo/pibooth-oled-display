#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from io import open
import os.path as osp
from setuptools import setup
from setuptools.command.install import install
import shutil
import os

HERE = osp.abspath(osp.dirname(__file__))
sys.path.insert(0, HERE)
from pibooth_oled_display import pibooth_oled_display as plugin

class CustomInstallCommand(install):
    def run(self):
        install.run(self)

        # Custom file copying script
        source_dir = os.path.join(HERE, 'pibooth_oled_display')
        destination_dir = os.path.expanduser('~/.config/pibooth/')

        print("Source directory: ", source_dir)
        print("Destination directory: ", destination_dir)

        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)

        for root, dirs, files in os.walk(source_dir):
            for file_name in files:
                source_path = os.path.join(root, file_name)
                destination_path = source_path.replace(source_dir, destination_dir)

                print("Copying: ", source_path, " to ", destination_path)
                
                os.makedirs(os.path.dirname(destination_path), exist_ok=True)
                shutil.copy(source_path, destination_path)


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
            'luma.oled',
            'oled'
        ],
        python_requires=">=3.6",
        install_requires=[
            'pibooth>=2.0.3',
            'luma.oled>=3.12.0'
        ],




        
        include_package_data=True,
        packages=['pibooth_oled_display', 'pibooth_oled_display.oled_display'],
package_data={
    'pibooth_oled_display': ['*.json', '*.txt'],
    'pibooth_oled_display.oled_display': ['logo/*', 'fonts/*', '*.py',
                                          'states/capture/*', 
                                          'states/choose/*', 
                                          'states/failure/*', 
                                          'states/finished/*', 
                                          'states/layout/*', 
                                          'states/preview/*', 
                                          'states/printer/*', 
                                          'states/processing/*',
                                          'states/capture/origin/*', 
                                          'states/choose/origin/*', 
                                          'states/failure/origin/*', 
                                          'states/finished/origin/*', 
                                          'states/layout/origin/*', 
                                          'states/preview/origin/*', 
                                          'states/printer/origin/*', 
                                          'states/processing/origin/*']
},
        options={
            'bdist_wheel':
                {'universal': True}
        },
        zip_safe=False,
        entry_points={'pibooth': ["pibooth_oled_display = pibooth_oled_display.pibooth_oled_display"]},
        cmdclass={
            'install': CustomInstallCommand,
        },
    )

if __name__ == '__main__':
    main()
