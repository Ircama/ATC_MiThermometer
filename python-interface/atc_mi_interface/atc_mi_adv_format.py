#############################################################################
# atc_mi_adv_format module (only used with bleak)
#############################################################################

# On each item, "service_data_dict" accepts either "uuid" (like "uuid": 'fcd2')
# or "uuid_str" (like "uuid_str": '0000fcd2-0000-1000-8000-00805f9b34fb');
# if the "uuid" string is defined, the related "uuid_str" string is generated
# by "__init__.py".

service_data_dict = {
    "atc1441": {
        "uuid": '181a',  # Environmental Sensing
        "length": 13,
    },
    "custom": {
        "uuid": '181a',
        "length": 15,
    },
    "custom_enc": {
        "uuid": '181a',
        "length": 11,
    },
    "atc1441_enc": {
        "uuid": '181a',
        "length": 8,
    },
    "mi_like": {
        "uuid": 'fe95',  # Xiaomi Inc.
        "length": None,
    },
    "bt_home": {
        "uuid": '181c',  # SERVICE_UUID_USER_DATA, HA_BLE, no security
        "length": None,
    },
    "bt_home_enc": {
        "uuid": '181e',
        "length": None,
    },
    "bt_home_v2": {
        "uuid": 'fcd2',
        "length": None,
    }
}

def atc_mi_advertising_format(advertisement_data):
    if not advertisement_data.service_data:
        return "", ""
    invalid_length = None
    for t in service_data_dict.keys():
        svc_data_t = service_data_dict[t]
        if svc_data_t["uuid_str"] in advertisement_data.service_data:
            payload = advertisement_data.service_data[svc_data_t["uuid_str"]]
            if svc_data_t["length"] and len(payload) != svc_data_t["length"]:
                invalid_length = len(payload)
                continue
            return t, bytes.fromhex(svc_data_t["uuid"])[::-1] + payload
    if invalid_length is not None:
        return "Unknown-length-" + str(invalid_length), ""
    return "Unknown", ""
