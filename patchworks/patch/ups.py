import binascii
import os

from patchworks import exc
from patchworks import util
from patchworks.format.base import Patch, AdjustsFilesize, CopiesSource


class UPSPatch(Patch, CopiesSource, AdjustsFilesize):

    EXTENSION = 'ups'
    MAGIC = b'UPS1'

    def read_file_sizes(self):
        self.source_size = self.read_int()
        self.modified_size = self.read_int()

    def read_checksums(self):
        self.source_checksum = self._read_checksum()
        self.modified_checksum = self._read_checksum()
        self.patch_checksum = self._read_checksum()

    def _read_checksum(self):
        checksum = b''
        checksum_size = 4
        while checksum_size:
            checksum = self.fp.read(1) + checksum
            checksum_size -= 1
        return binascii.hexlify(checksum).decode()

    def read_record(self):
        relative_offset = self.read_int()
        data = b''
        for data_byte in iter(lambda: self.fp.read(1), b'\x00'):
            data += data_byte
        return (relative_offset, data)

    def read_records(self):
        patch_size = os.path.getsize(self.fp.name)
        while patch_size != self.fp.tell() + 12:
            record = self.read_record()
            yield record

    def read_int(self):
        return self._read_int_iter()

    def _read_int_iter(self, accumulator=0, shift=1):
        unmasked_byte = util.int_from_bytes(self.fp.read(1))
        accumulator += (unmasked_byte & 0x7f) * shift
        if (unmasked_byte & 0x80):
            return accumulator
        else:
            shift <<= 7
            return self._read_int_iter(accumulator + shift, shift)

    def apply_records(self, source_fp, target_fp):
        pass

    def apply(self, source_fp, target_fp):
        self.validate_file(self.source_checksum, source_fp)
        self.copy_source_to_modified(source_fp, target_fp)
        self.expand_or_truncate(source_fp, target_fp)
        self.apply_records(source_fp, target_fp)
        self.validate_file(self.modified_checksum, target_fp)

    def validate_file(self, checksum, fp):
        if checksum != util.crc32_sum(fp):
            raise exc.InvalidChecksum()
