import binascii
import hashlib
import os
import zlib


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


def crc32_sum(fp):
    crc = zlib.crc32(b'')
    for chunk in iter(lambda: fp.read(4096), b''):
        crc = zlib.crc32(chunk, crc)
    return "%08x" % crc


def bytes_from_str(string):
    leading_zero = "0" * (len(string) % 2)
    return binascii.unhexlify(leading_zero + string)


def expand_file(fp, size):
    fp.seek(size - 1)
    fp.write(b'\x00')


def sizeof_file(fp):
    fp.seek(0, os.SEEK_END)
    file_size = fp.tell()
    fp.seek(0)
    return file_size
