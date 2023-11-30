#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#############################################################################
# atc_mi_interface module setup [name: atc-mi-interface]
#############################################################################

"""
# Publishing instructions
# =======================

cd python-interface
pip3 install pyyaml python-daemon setuptools wheel twine flake8
python3 -m flake8 setup.py --count --select=E9,F63,F7,F72,F82 --show-source --statistics

# Build a binary wheel and a source tarball
python3 setup.py sdist bdist_wheel

#python3 -m build --sdist --wheel --outdir dist/ .

# This will publish the /dist directory
python3 -m twine upload --repository testpypi dist/*
python3 -m twine upload --repository pypi dist/*

End user publishing page:

https://test.pypi.org/project/atc-mi-interface/
https://pypi.org/project/atc-mi-interface/

Removing directories
del /f/s/q build dist atc_mi_interface.egg-info
"""

from setuptools import setup
import re

DESCRIPTION = (
    'Python tools and API to process BLE advertisements of BLE devices'
    'and sensors, also including the "atc1441" and "pvvx" Xiaomi Mijia'
    ' Thermometer custom firmware'
)

PACKAGE_NAME = "atc-mi-interface"

VERSIONFILE = "atc_mi_interface/__version__.py"

LONG_DESCRIPTION = '''
# atc-mi-interface

__Tools and API to process BLE advertisements of BLE devices and sensors__

Python data model, Python API and tools to receive, decode, show and edit
the BLE advertisements produced by the following sensors:

- Xiaomi Mijia devices
- BT Home DIY sensors implementing BTHome v1 and v2 protocols
- Xiaomi Mijia Thermometer with custom
firmware (ATC_MiThermometer) developed by
[atc1441](https://github.com/atc1441/ATC_MiThermometer)
and [pvvx](https://github.com/pvvx/ATC_MiThermometer).

The following apps are included:

- a configuration tool which can be used with the latest releases of the "pvvx"
  firmware to browse and update the internal configuration parameters; it can
  be run either via command-line interface or through its GUI, and it also
  provides an API;
- the "BLE Advertisement Browser for Home Sensors" app (atc_mi_advertising),
  consisting of a ready-to-use, cross-platform GUI allowing to receive, decode,  
  browse, edit and build BLE advertisements for all supported protocols; this
  app can also be used to easily integrate new BLE devices;
- the atc_mi_format_test GUI app, collecting test suites of BLE advertising
  samples.

Installation of the API without GUI:

```
pip install [ -i https://test.pypi.org/simple/ ] atc-mi-interface
```

Installation of GUI apps and API:

```
pip install [ -i https://test.pypi.org/simple/ ] atc-mi-interface[gui]
```

Full information, installation notes, API reference and usage details at the
[pvvx/ATC_MiThermometer/python-interface repository](https://github.com/pvvx/ATC_MiThermometer/tree/master/python-interface#python-interfacing-methods-and-data-representation-model).
'''

###########################################################################

verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))

setup(
    name=PACKAGE_NAME,
    version=verstr,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    classifiers=[
        "License :: OSI Approved :: The Unlicense (Unlicense)",
        "Topic :: Software Development :: Libraries :: Python Modules",
        'Programming Language :: Python :: 3 :: Only',
        "Programming Language :: Python :: Implementation :: CPython",
        "Development Status :: 5 - Production/Stable",
        "Typing :: Typed",
        "Intended Audience :: Developers",
    ],
    author="Ircama",
    url="https://github.com/pvvx/ATC_MiThermometer/tree/master/python-interface",
    license='https://unlicense.org',
    packages=["atc_mi_interface"],
    entry_points={
        "console_scripts": [
            "atc_mi_config=atc_mi_interface.atc_mi_config:main",
            "atc_mi_advertising=atc_mi_interface.atc_mi_advertising:main",
            "atc_mi_format_test=atc_mi_interface.atc_mi_format_test:main"
        ]
    },
    include_package_data=True,
    install_requires=[
        'construct',
        'bleak',
        'pycryptodome',
        'arrow'
    ],
    extras_require={
        'gui': [
            "wxPython",
            "construct-gallery>=1.4.0",
            "construct-editor"
        ]
    },
    keywords=[
        PACKAGE_NAME,
        "Xiaomi",
        "Mijia",
        "Thermometer",
        "firmware",
        "wxpython",
        "editor",
        "construct",
        "bleak",
        "BLE",
        "bluetooth",
        "LYWSD03MMC",
    ],
    python_requires=">=3.8",
)
