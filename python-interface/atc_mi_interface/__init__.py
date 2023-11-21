#############################################################################
# atc_mi_interface module
#############################################################################

from .atc_mi_construct import *
from .atc_mi_adv_format import atc_mi_advertising_format, gatt_dict
from bleak.uuids import normalize_uuid_str

for item, values in gatt_dict.items():
    if "uuid" in values:
        gatt_dict[item]["gatt"] = normalize_uuid_str(values["uuid"])
