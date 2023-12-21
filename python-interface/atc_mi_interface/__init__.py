#############################################################################
# atc_mi_interface module
#############################################################################

from .atc_mi_construct import *
from .atc_mi_adv_format import atc_mi_advertising_format, service_data_dict
from bleak.uuids import normalize_uuid_str

for item, values in service_data_dict.items():
    if "uuid" in values:
        service_data_dict[item]["uuid_str"] = normalize_uuid_str(values["uuid"])
