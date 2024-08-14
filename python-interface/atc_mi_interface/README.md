# Classification of the components

## Core:

Core processing of format build and parse
compatible with Python 2 and Python 3.

- atc_mi_construct_adapters.py
- atc_mi_construct.py
- __init__.py (without from bleak.uuids ... and for item, values ...)
- __version__.py

## Bleak:

Building and parsing Bleak advertising.
Not required if BLE is processed with libraries different than Bleak.
Only tested with Python 3.

- atc_mi_adv_format.py
- __init__.py

## User interface:

Elements requiring wxpython.
Only required if Bleak is used and if the 3 UI apps
(atc_mi_advertising, atc_mi_config and atc_mi_format_test) are needed.
Only tested with Python 3.

- atc_mi_advertising.py
- atc_mi_config.py
- atc_mi_format_test.py
- construct_module.py
- __main__.py
