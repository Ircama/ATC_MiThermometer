#############################################################################
# atc_mi_interface module
#############################################################################

import sys
import warnings

if sys.version_info.major == 2:  # with python2.7...
    warnings.warn = lambda *_: True  # remove arrow.py:28: DeprecationWarning

from .atc_mi_adv_format import atc_mi_advertising_format, service_data_dict  # only used with bleak
from .atc_mi_construct import *

try:
    from bleak.uuids import normalize_uuid_str

    for item, values in service_data_dict.items():
        if "uuid" in values:
            service_data_dict[item]["uuid_str"] = normalize_uuid_str(
                values["uuid"]
            )
except ImportError:
    pass
