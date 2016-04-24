import binascii


from .base import Parser, Record, Applicator, AdjustsFilesize
from .. import util


class UPSParser(Parser):

    EXTENSION = 'ups'
    MAGIC = b'UPS1'

    def __init__(self, _file):
        super().__init__(_file)

        self.patch_size = util.sizeof_file(self._file)

    def parse_file_sizes(self):
        self.source_size = self.parse_int()
        self.modified_size = self.parse_int()

    def parse_checksums(self):
        self.source_checksum = self._parse_checksum()
        self.modified_checksum = self._parse_checksum()
        self.patch_checksum = self._parse_checksum()

    def _parse_checksum(self):
        checksum = b''
        checksum_size = 4
        while checksum_size:
            checksum = self.read(1) + checksum
            checksum_size -= 1
        return binascii.hexlify(checksum).decode()

    def parse_record(self):
        relative_offset = self.parse_int()
        data = b''
        for data_byte in iter(lambda: self.read(1), b'\x00'):
            data += data_byte
        return UPSRecord(relative_offset, data)

    def parse_records(self):
        while self._file.tell() != self.patch_size - 12:
            record = self.parse_record()
            yield record

    def parse_int(self):
        return self._parse_int_iter()

    def _parse_int_iter(self, accumulator=0, shift=1):
        unmasked_byte = util.int_from_bytes(self.read(1))
        accumulator += (unmasked_byte & 0x7f) * shift
        if (unmasked_byte & 0x80):
            return accumulator
        else:
            shift <<= 7
            return self._parse_int_iter(accumulator + shift, shift)


class UPSRecord(Record):

    def __init__(self, relative_offset, data):
        self.relative_offset = relative_offset
        self.data = data


class UPSApplicator(Applicator, AdjustsFilesize):

    def apply(self):
        # check crc32 of input
        # copy source to modified
        # expand/truncate if necessary
        # apply records
        # check crc32 of output
        pass

    def validate_source(self):
        # raise WrongSource
        pass

    def validate_modified(self):
        pass

    def load_patch(self):
        self.patch = UPSParser(self.patch_fp)
