# Library module used by atc_mi_construct.py

import re
import math
from itertools import chain
from construct import *  # pip3 install construct
from Crypto.Cipher import AES  # pip3 install pycryptodome

MacVendor = Switch(
    this.MAC[:9],
    {
        "A4:C1:38:": Computed("Telink Semiconductor (Taipei) Co. Ltd"),
        "54:EF:44:": Computed("Lumi United Technology Co., Ltd"),
        "E4:AA:EC:": Computed("Tianjin Hualai Tech Co, Ltd"),
    },
    default=Computed("Unknown vendor"),
)


def dict_union(*args):
    return dict(chain.from_iterable(d.items() for d in args))

def handle_decrypt_error(descr):  # can be monkey patched
    raise ValueError(descr)


class BtHomeCodec(Tunnel):
    """
    Uses "bindkey" and "mac_address" parameters in parse() and build():

        <>.parse(
            bytes,
            mac_address=b'\xaa\xbb\xcc\xdd\xee\xff',
            bindkey=b'\xaa\xaa\xaa\xaa\xaa\xaa',
        )

        <>.build(
            { ... },
            mac_address=b'\xaa\xbb\xcc\xdd\xee\xff',
            bindkey=b'\xaa\xaa\xaa\xaa\xaa\xaa',
        )
    """
    def __init__(self, subcon, bindkey=b'', mac_address=b''):
        super(Tunnel, self).__init__(subcon)
        self.default_bindkey = bindkey
        self.def_mac = mac_address

    def bindkey(self, ctx):
        try:
            return ctx._params.bindkey or self.default_bindkey
        except Exception:
            return self.default_bindkey

    def mac(self, ctx, msg="encode or decode"):
        try:
            mac = ctx._params.mac_address or self.def_mac
        except Exception:
            mac = self.def_mac
        if not mac.strip():
            return handle_decrypt_error('Missing MAC address. Cannot convert.')
        return mac.strip()

    def decrypt(self, ctx, nonce, encrypted_data, mic, update):
        bindkey = self.bindkey(ctx)
        if not bindkey:
            return handle_decrypt_error('Missing bindkey, cannot decrypt.')
        cipher = AES.new(bindkey, AES.MODE_CCM, nonce=nonce, mac_len=4)
        if update is not None:
            cipher.update(update)
        try:
            return cipher.decrypt_and_verify(encrypted_data, mic)
        except Exception as e:
            return handle_decrypt_error("Cannot decrypt: " + str(e))

    def encrypt(self, ctx, nonce, msg, update):
        bindkey = self.bindkey(ctx)
        if not bindkey:
            return handle_decrypt_error('Missing bindkey, cannot encrypt.')
        cipher = AES.new(bindkey, AES.MODE_CCM, nonce=nonce, mac_len=4)
        if update is not None:
            cipher.update(update)
        return cipher.encrypt_and_digest(msg)

    def _decode(self, obj, ctx, path):
        mac = self.mac(ctx, "decode")
        uuid = ctx._subcons.UUID.build(ctx.UUID)
        encrypted_data = obj[:-8]
        count_id = obj[-8:-4]  # Int32ul
        mic = obj[-4:]
        nonce = mac + uuid + count_id
        msg = self.decrypt(ctx, nonce, encrypted_data, mic, update=b"\x11")
        return count_id + msg

    def _encode(self, obj, ctx, path):
        mac = self.mac(ctx, "encode")
        length_count_id = 4  # first 4 bytes = 32 bits
        count_id = bytes(obj)[:length_count_id]  # Int32ul
        uuid16 = b"\x1e\x18"
        nonce = mac + uuid16 + count_id
        ciphertext, mic = self.encrypt(
            ctx, nonce, obj[length_count_id:], update=b"\x11"
        )
        return ciphertext + count_id + mic


class BtHomeV2Codec(BtHomeCodec):
    def _decode(self, obj, ctx, path):
        mac = self.mac(ctx, "decode")
        uuid = ctx._subcons.UUID.build(ctx.UUID)
        device_info = ctx._subcons.DevInfo.build(ctx.DevInfo)
        encrypted_data = obj[:-8]
        count_id = obj[-8:-4]  # Int32ul
        mic = obj[-4:]
        nonce = mac + uuid + device_info + count_id
        msg = self.decrypt(ctx, nonce, encrypted_data, mic, update=None)
        return count_id + msg

    def _encode(self, obj, ctx, path):
        mac = self.mac(ctx, "encode")
        length_count_id = 4  # first 4 bytes = 32 bits
        count_id = bytes(obj)[:length_count_id]  # Int32ul
        uuid16 = b"\xd2\xfc"
        device_info = b"\x41"
        nonce = mac + uuid16 + device_info + count_id
        ciphertext, mic = self.encrypt(
            ctx, nonce, bytes(obj)[length_count_id:], update=None,
        )
        return ciphertext + count_id + mic


class AtcMiCodec(BtHomeCodec):
    def _decode(self, obj, ctx, path):
        mac = self.mac(ctx, "decode")
        payload = bytes(obj)[1:]
        cipherpayload = payload[:-4]
        header_bytes = (
            bytearray([len(obj) + 3])
            + b'\x16'
            + ctx._subcons.UUID.build(ctx.UUID)
        )  # b'\x0e\x16\x1a\x18' (custom_enc) or b'\x0b\x16\x1a\x18' (atc1441_enc)
        nonce = mac[::-1] + header_bytes + bytearray([obj[0]])
        mic = payload[-4:]
        msg = self.decrypt(ctx, nonce, cipherpayload, mic, update=b"\x11")
        return msg

    def _encode(self, obj, ctx, path):
        mac = self.mac(ctx, "encode")
        header_bytes = (
            bytearray([len(obj) + 8])
            + b'\x16'
            + ctx._subcons.UUID.build(ctx.UUID)
        ) + b'\xbd'  # b'\x0e\x16\x1a\x18\xbd' (custom_enc) or b'\x0b\x16\x1a\x18\xbd' (atc1441_enc)
        nonce = mac[::-1] + header_bytes
        ciphertext, mic = self.encrypt(ctx, nonce, obj, update=b"\x11")
        return b'\xbd' + ciphertext + mic


class MiLikeCodec(BtHomeCodec):
    def _decode(self, obj, ctx, path):
        cipherpayload = obj[:-7]
        mac = self.mac(ctx, "decode")
        dev_id = ctx._subcons.device_id.build(ctx.device_id)  # pid, PRODUCT_ID
        cnt = ctx._subcons.counter.build(ctx.counter)
        count_id = obj[-7:-4]  # Int24ul
        nonce = mac[::-1] + dev_id + cnt + count_id
        mic = obj[-4:]
        msg = self.decrypt(ctx, nonce, cipherpayload, mic, update=b"\x11")
        return count_id + msg

    def _encode(self, obj, ctx, path):
        mac = self.mac(ctx, "encode")
        dev_id = ctx._subcons.device_id.build(ctx.device_id)  # pid, PRODUCT_ID
        cnt = ctx._subcons.counter.build(ctx.counter)
        length_count_id = 3  # first 3 bytes = 24 bits
        count_id = bytes(obj)[:length_count_id]  # Int24ul
        nonce = mac[::-1] + dev_id + cnt + count_id
        ciphertext, mic = self.encrypt(
            ctx, nonce, obj[length_count_id:], update=b"\x11"
        )
        return ciphertext + count_id + mic


class DecimalNumber(Adapter):
    def __init__(self, subcon, decimal):
        self.decimal = decimal
        super(Adapter, self).__init__(subcon)
        self._decode = lambda obj, ctx, path: float(obj) / self.decimal
        self._encode = lambda obj, ctx, path: int(float(obj) * self.decimal)


class ByteAdapter(Adapter):
    def __init__(self, nbytes=6, separator=':', reverse=False):
        Adapter.__init__(self, Byte[nbytes])
        self._decode = lambda obj, ctx, path: separator.join(
            "%02x" % b for b in obj[::-1 if reverse else 1]
        ).upper()
        self._encode = lambda obj, ctx, path: bytearray.fromhex(
            re.sub(r'[.:\- ]', '', obj)
        )[::-1 if reverse else 1]


MacAddress = ByteAdapter()
ReversedMacAddress = ByteAdapter(reverse=True)


def normalize_report(report):
    report = re.sub(r"\n\s*Container:\n?", "\n", report, flags=re.DOTALL)
    report = re.sub(r"\n\s*version =[^\n]*\n", "\n", report, flags=re.DOTALL)
    report = re.sub(r" = Container:\s*\n", ":\n", report, flags=re.DOTALL)
    report = re.sub(r" = ListContainer:\s*\n", ":\n", report, flags=re.DOTALL)
    report = re.sub(r" = u'", " = '", report, flags=re.DOTALL)
    report = re.sub(r"\n\s*\n", "\n", report, flags=re.DOTALL)
    report = re.sub(
        r'hexundump\("""\n(.*)\n"""\)\n', "\g<1>", report, flags=re.DOTALL)
    report = re.sub(r"unhexlify\('([A-Fa-f0-9]*)'\)",
        lambda m: "    %s" % m.group(1).upper(), report, flags=re.DOTALL
    )
    return report


def absolute_humidity(temp_celsius, relative_humidity):
    """
    Calculate the absolute humidity in g/m³.

    Parameters:
    temp_celsius (float): Temperature in degrees Celsius.
    relative_humidity (float): Relative humidity in percentage (0-100).

    Returns:
    float: Absolute humidity in g/m³.
    """
    return (
        2.1674 * 6.112 * math.exp(
            (17.67 * temp_celsius) / (temp_celsius + 243.5)
        ) * relative_humidity
    ) / (temp_celsius + 273.15)


def dew_point(temp_celsius, relative_humidity):
    """
    Calculate the dew point in degrees Celsius: The temperature at which the
    air reaches 100% relative humidity.

    Parameters:
    temp_celsius (float): Temperature in degrees Celsius.
    relative_humidity (float): Relative humidity in percentage (0-100).

    Returns:
    float: dew point in °C.
    """
    alpha = (
        math.log(relative_humidity / 100)
        + (17.67 * temp_celsius) / (243.5 + temp_celsius)
    )
    dew_point = (243.5 * alpha) / (17.67 - alpha)
    return dew_point
