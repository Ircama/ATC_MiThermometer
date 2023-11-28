#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#############################################################################
# atc_mi_format_test.py
#############################################################################

import wx
from construct_gallery import ConstructGallery, GalleryItem
import construct_editor.core.custom as custom
from collections import OrderedDict

from . import atc_mi_construct
from .construct_module import *  # It includes setting the gallery_descriptor dictionary.


def main():
    app = wx.App(False)
    frame = wx.Frame(
        None,
        title="Xiaomi Mijia Thermometer - ATC MI Formats",
        size=(1000, 500)
    )

    ordered_samples = OrderedDict(
    # ordered_samples OrderedDict for the overall data, independent of the
    # gallery_descriptor. Notice that if a reference is used "mac_address",
    # reference_label and key_label must be set in ConstructGallery
        [
            (
                "custom",
                {
                    "binary": bytes.fromhex(
                        "12 16 1a 18 cc bb aa 38 c1 a4 6c 07 fa 13 d6 0a 52 09 "
                        "0f"),
                    "mac_address": "A4:C1:38:AA:BB:CC",
                },
            ),
            (
                "custom_enc",
                {
                    "binary": bytes.fromhex(
                        "0e 16 1a 18 bd 86 c5 3f fa b9 00 c1 51 58 59"),
                    "mac_address": "A4:C1:38:AA:BB:CC",
                },
            ),
            (
                "atc1441",
                {
                    "binary": bytes.fromhex(
                        "10 16 1a 18 a4 c1 38 aa bb cc 00 ce 33 43 0a 6e c3"),
                    "mac_address": "A4:C1:38:AA:BB:CC",
                },
            ),
            (
                "atc1441_enc",
                {
                    "binary": bytes.fromhex(
                        "0b 16 1a 18 bd e9 b7 5d b8 56 f3 03"),
                    "mac_address": "A4:C1:38:AA:BB:CC",
                },
            ),
            (
                "mi_like (temp, humidity)",
                {
                    "binary": bytes.fromhex(
                        "15 16 95 fe 50 58 5b 05 1b cc bb aa 38 c1 a4 0d 10 04 "
                        "be 00 00 02"),
                    "mac_address": "A4:C1:38:AA:BB:CC",
                },
            ),
            (
                "mi_like (batt)",
                {
                    "binary": bytes.fromhex(
                        "12 16 95 fe 50 58 5b 05 22 cc bb aa 38 c1 a4 0a 10 01 "
                        "4f"),
                    "mac_address": "A4:C1:38:AA:BB:CC",
                },
            ),
            (
                "mi_like_enc (temperature)",
                {
                    "binary": bytes.fromhex(
                        "1a 16 95 fe 58 58 5b 05 f4 cc bb aa 38 c1 a4 13 df 92 "
                        "a8 1c b3 00 00 ac c4 6f da"),
                    "mac_address": "A4:C1:38:AA:BB:CC",
                },
            ),
            (
                "mi_like_enc (humidity %)",
                {
                    "binary": bytes.fromhex(
                        "1a 16 95 fe 58 58 5b 05 95 cc bb aa 38 c1 a4 d5 25 d9 "
                        "74 ec 14 00 00 9b e1 de 3c"),
                    "mac_address": "A4:C1:38:AA:BB:CC",
                },
            ),
            (
                "mi_like_enc (battery %)",
                {
                    "binary": bytes.fromhex(
                        "19 16 95 fe 58 58 5b 05 ed cc bb aa 38 c1 a4 de 6d f0 "
                        "74 b3 00 00 f2 ef 0e 53"),
                    "mac_address": "A4:C1:38:AA:BB:CC",
                },
            ),
            (
                "bt_home v1 (temp, humidity, batt%)",
                {
                    "binary": bytes.fromhex(
                        "11 16 1c 18 02 00 56 23 02 6c 07 03 03 ff 13 02 01 "
                        "4e"),
                    "mac_address": "A4:C1:38:AA:BB:CC",
                },
            ),
            (
                "bt_home v1 (batt v, switch)",
                {
                    "binary": bytes.fromhex(
                        "0d 16 1c 18 02 00 63 02 10 01 03 0c d9 0a"),
                    "mac_address": "A4:C1:38:AA:BB:CC",
                },
            ),
            (
                "bt_home v1 (test suite)",
                {
                    "binary": bytes.fromhex(
                        "b4 16 1c 18 02 01 61 23 02 ca 09 03 03 bf 13 02 2e 23 "
                        "04 04 13 8a 01 04 05 13 8a 14 03 06 5e 1f 03 07 3e 1d "
                        "23 08 ca 06 02 09 60 04 0a 13 8a 14 04 0b 02 1b 00 03 "
                        "0c 02 0c 03 0d 12 0c 03 0e 02 1c 03 12 e2 04 03 13 33 "
                        "01 03 14 02 0c 02 2f 23 05 50 5d 39 61 64 03 51 87 56 "
                        "03 52 87 56 02 0f 01 02 10 01 02 11 00 02 15 01 02 16 "
                        "01 02 17 00 02 18 01 02 19 00 02 1a 00 02 1b 01 02 1c "
                        "01 02 1d 00 02 1e 01 02 1f 01 02 20 01 02 21 00 02 22 "
                        "01 02 23 01 02 24 00 02 25 00 02 26 01 02 27 01 02 28 "
                        "00 02 29 01 02 2a 00 02 2b 00 02 2c 01 02 2d 01 02 00 "
                        "01"),
                    "mac_address": "A4:C1:38:AA:BB:CC",
                },
            ),
            (
                "bt_home_v1_enc (temp, humidity, batt%)",
                {
                    "binary": bytes.fromhex(
                        "16 16 1e 18 83 93 db a2 55 4c d8 04 be ab 78 cf b3 00 "
                        "00 7d 6a 1c d2"),
                    "mac_address": "A4:C1:38:AA:BB:CC",
                },
            ),
            (
                "bt_home_v1_enc (batt v, switch)",
                {
                    "binary": bytes.fromhex(
                        "12 16 1e 18 12 79 94 44 eb 3a 3f e4 b3 00 00 59 62 3a "
                        "29"),
                    "mac_address": "A4:C1:38:AA:BB:CC",
                },
            ),
            (
                "bt_home_v2 (temp, humidity, batt%)",
                {
                    "binary": bytes.fromhex(
                        "0e 16 d2 fc 40 00 d6 01 50 02 80 07 03 8a 13"
                    ),
                    "mac_address": "A4:C1:38:AA:BB:CC",
                },
            ),
            (
                "bt_home_v2 (batt v, switch)",
                {
                    "binary": bytes.fromhex(
                        "0b 16 d2 fc 40 00 d9 0c d1 0a 10 00"
                    ),
                    "mac_address": "A4:C1:38:AA:BB:CC",
                },
            ),
            (
                "bt_home_v2 (test suite)",
                {
                    "binary": bytes.fromhex(
                        "e5 16 d2 fc 40 00 01 51 87 56 01 61 12 e2 04 09 60 3d "
                        "09 60 3e 2a 2c 09 60 43 4e 34 08 ca 06 40 0c 00 41 4e "
                        "00 42 4e 34 00 4d 12 13 8a 14 0a 13 8a 14 4b 13 8a 14 "
                        "4c 41 01 8a 01 52 87 56 03 bf 13 2e 23 05 13 8a 14 06 "
                        "5e 1f 07 3e 1d 14 02 0c 2f 23 0d 12 0c 0e 02 1c 0b 02 "
                        "1b 00 04 13 8a 01 54 0c 48 65 6c 6c 6f 20 57 6f 72 6c "
                        "64 21 3f 02 0c 44 4e 34 45 11 01 02 ca 09 53 0c 48 65 "
                        "6c 6c 6f 20 57 6f 72 6c 64 21 50 5d 39 61 64 13 33 01 "
                        "0c 02 0c 4a 02 0c 4e 87 56 2a 01 47 87 56 48 dc 87 49 "
                        "dc 87 46 32 4f 87 56 2a 01 15 01 16 01 17 01 18 01 19 "
                        "01 1a 01 1b 01 1c 01 1d 01 1e 01 1f 01 20 01 21 01 22 "
                        "01 23 01 24 01 25 01 26 01 27 01 28 01 29 01 2a 01 2b "
                        "01 2c 01 2d 01 3a 05 3c 01 03 3a 00 3a 01"
                    ),
                    "mac_address": "A4:C1:38:AA:BB:CC",
                },
            ),
            (
                "bt_home_v2_enc (temp, humidity, batt%)",
                {
                    "binary": bytes.fromhex(
                        "14 16 d2 fc 41 95 b0 ef da 78 9d d9 53 b0 26 00 00 "
                        "93 41 62 6f"
                    ),
                    "mac_address": "A4:C1:38:AA:BB:CC",
                },
            ),
            (
                "bt_home_v2_enc (batt v, switch)",
                {
                    "binary": bytes.fromhex(
                        "11 16 d2 fc 41 d4 6c c8 e7 74 b9 26 00 00 cb d8 4a 40"
                    ),
                    "mac_address": "A4:C1:38:AA:BB:CC",
                },
            ),
        ]
    )

    ref_key_descriptor = {  # ref_key_descriptor dictionary for the overall data
        "A4:C1:38:AA:BB:CC": {"bindkey": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}
    }


    frame.main_panel = ConstructGallery(frame,
        gallery_descriptor=gallery_descriptor,
        ordered_samples=ordered_samples,
        ref_key_descriptor=ref_key_descriptor,
        reference_label="MAC address",
        key_label="Bindkey",
        description_label="Description",
        col_name_width=200,
        col_type_width=150
    )

    frame.Show(True)
    app.MainLoop()


if __name__ == "__main__":
    main()
