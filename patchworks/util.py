import binascii
import hashlib


def zero_padded_bytes_to_string(bytestring):
    return bytestring.decode('utf-8').strip('\x00')


def int_from_bytes(bytestring, endian='little'):
    accumulator = 0
    offsets = range(0, len(bytestring))
    if endian == 'big':
        offsets = reversed(offsets)
    for offset, i in zip(offsets, bytearray(bytestring)):
        accumulator |= i << (offset * 8)
    return accumulator


def md5_sum(fp):
    m = hashlib.md5()
    for chunk in iter(lambda: fp.read(4096), b''):
        m.update(chunk)
    return m.hexdigest()


def bytes_from_str(string):
    leading_zero = "0" * (len(string) % 2)
    return binascii.unhexlify(leading_zero + string)
